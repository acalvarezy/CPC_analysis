"""
Combine two faceted line-profile PDFs (p-H2A and p-H3 vs. Inter-KT-distance,
each faceted by time point x {Relaxed, Tensed}) into a single figure that
overlays both traces per panel, keeping the original panel arrangement.

How it works
------------
The source PDFs are vector graphics (produced by ggplot/matplotlib), so
instead of rasterizing and cropping pixels, this script reads the actual
vector drawing commands with PyMuPDF:
  - each panel's plot-area rectangle (white background "re" objects) gives
    the pixel->data mapping for the x-axis (x0 -> 0 µm, x1 -> 1.3 µm,
    confirmed to have zero padding in the source plots),
  - the small tick-mark line segments to the left of the first panel give
    the pixel->data mapping for the (shared) y-axis,
  - the actual curve is the polyline drawn in the trace's distinctive color
    (red for p-H2A, orange for p-H3).
Coordinates are converted back to real data (µm / µM) and re-plotted with
matplotlib using a twin y-axis per panel (red = p-H2A on the left, orange =
p-H3 on the right), so the combined plot is a faithful, crisp vector
redraw rather than a rasterized composite.

Requirements: pip install pymupdf numpy matplotlib

Usage:
    python make_combined_line_profiles.py
"""

import fitz  # PyMuPDF
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# 1. Inputs — point these at your two source PDFs
# ---------------------------------------------------------------------------
P2A_PDF = "pH2A_line_profile_all_timepoints.pdf"
P3_PDF = "pH3_line_profile_all_timepoints.pdf"
OUTPUT_PATH = "combined_line_profiles.png"

# Trace colors as they appear in the source PDFs (RGB, 0-1)
RED = (0.7568627595901489, 0.10980392247438431, 0.03921568766236305)   # p-H2A
ORANGE = (0.9490196108818054, 0.5960784554481506, 0.06666667014360428)  # p-H3

# Facet labels, in left-to-right / top order as they appear in the sources
TIMES = ["0", "0.2", "2", "4", "5", "6", "8"]
SUBS = ["Relaxed", "Tensed"]

# y-axis calibration: the tick VALUES in the same top->bottom pixel order as
# the tick marks found on the page. Re-measure these if your source scale
# changes (e.g. a different max concentration).
Y_VALUES_2A = [35, 30, 25, 20, 15, 10, 5, 0]
Y_VALUES_3 = [100, 80, 60, 40, 20, 0]

X_DATA_MAX = 1.3  # µm, matches the "0 .. 1.3" x-axis in the source plots


# ---------------------------------------------------------------------------
# 2. Vector extraction helpers
# ---------------------------------------------------------------------------
def get_panels(page):
    """Return each panel's plot-area rectangle, sorted left to right."""
    drawings = page.get_drawings()
    rects = []
    for d in drawings:
        if len(d["items"]) == 1 and d["items"][0][0] == "re":
            r = d["items"][0][1]
            if r.width < 3000:  # exclude the full-page background rect
                rects.append(r)
    seen, uniq = set(), []
    for r in rects:
        key = (round(r.x0, 2), round(r.y0, 2), round(r.x1, 2), round(r.y1, 2))
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    uniq.sort(key=lambda r: r.x0)
    return uniq


def get_y_ticks(page, x_thresh=380):
    """Pixel y-positions of the shared y-axis tick marks (left of panel 0)."""
    drawings = page.get_drawings()
    ticks = []
    for d in drawings:
        if len(d["items"]) == 1 and d["items"][0][0] == "l":
            p1, p2 = d["items"][0][1], d["items"][0][2]
            if abs(p1.y - p2.y) < 0.01 and p1.x < x_thresh and p2.x < x_thresh:
                ticks.append(p1.y)
    return sorted(set(round(t, 3) for t in ticks))


def get_curve_paths(page, color, tol=0.02):
    """All polylines drawn in the given RGB color."""
    drawings = page.get_drawings()
    paths = []
    for d in drawings:
        c = d["color"]
        if c is None or not all(abs(c[i] - color[i]) < tol for i in range(3)):
            continue
        items = d["items"]
        if not items or items[0][0] != "l":
            continue
        pts = [items[0][1]] + [it[2] for it in items]
        paths.append([(p.x, p.y) for p in pts])
    return paths


def assign_to_panels(curves, panels):
    """Match each extracted curve to the panel it falls inside (by x-range)."""
    out = [None] * len(panels)
    for curve in curves:
        cx = sum(p[0] for p in curve) / len(curve)
        for i, r in enumerate(panels):
            if r.x0 - 1 <= cx <= r.x1 + 1:
                out[i] = curve
                break
    return out


def to_data(curve, panel, y_ticks, y_values):
    """Convert one curve's PDF-pixel points to (x, y) data coordinates."""
    y_bottom, y_top = y_ticks[-1], y_ticks[0]      # pixel y for value 0 / max
    v_bottom, v_top = y_values[-1], y_values[0]    # 0 / max
    xs = np.array([p[0] for p in curve])
    ys = np.array([p[1] for p in curve])
    x_data = (xs - panel.x0) / (panel.x1 - panel.x0) * X_DATA_MAX
    y_data = v_bottom + (y_bottom - ys) / (y_bottom - y_top) * (v_top - v_bottom)
    order = np.argsort(x_data)
    return x_data[order], y_data[order]


def extract(pdf_path, color, y_values):
    doc = fitz.open(pdf_path)
    page = doc[0]
    panels = get_panels(page)
    y_ticks = get_y_ticks(page)
    curves_raw = get_curve_paths(page, color)
    curves = assign_to_panels(curves_raw, panels)
    assert all(c is not None for c in curves), (
        f"Could not match every panel to a curve in {pdf_path} — "
        "check the color tolerance or panel detection."
    )
    return [to_data(curves[i], panels[i], y_ticks, y_values) for i in range(len(panels))]


# ---------------------------------------------------------------------------
# 3. Build the combined figure
# ---------------------------------------------------------------------------
def main():
    data_2a = extract(P2A_PDF, RED, Y_VALUES_2A)
    data_3 = extract(P3_PDF, ORANGE, Y_VALUES_3)

    n_panels = len(data_2a)
    assert n_panels == len(data_3) == len(TIMES) * len(SUBS)

    fig = plt.figure(figsize=(21, 4.6))
    gs = gridspec.GridSpec(
        1, n_panels, figure=fig, wspace=0.10,
        left=0.045, right=0.96, top=0.80, bottom=0.24,
    )

    # Both traces are already in the same unit (µM), so they share one
    # y-axis sized to fit the larger of the two (p-H3 tops out at 100).
    y_max = max(max(Y_VALUES_2A), max(Y_VALUES_3))
    y_ticks = sorted(set(Y_VALUES_3))  # coarser tick set (0,20,...,100)

    axes = []
    for i in range(n_panels):
        ax = fig.add_subplot(gs[0, i])
        x2a, y2a = data_2a[i]
        ax.plot(x2a, y2a, color=RED, linewidth=2.2, label="p-H2A")
        x3, y3 = data_3[i]
        ax.plot(x3, y3, color=ORANGE, linewidth=2.2, label="p-H3")

        ax.set_xlim(0, X_DATA_MAX)
        ax.set_ylim(0, y_max)
        ax.set_xticks([0, X_DATA_MAX / 2, X_DATA_MAX])
        ax.set_xticklabels(["0", f"{X_DATA_MAX/2:g}", f"{X_DATA_MAX:g}"],
                            fontsize=7, rotation=45)

        if i == 0:
            ax.set_yticks(y_ticks)
            ax.tick_params(axis="y", labelsize=7.5)
            ax.set_ylabel("Concentration (µM)", fontsize=9)
        else:
            ax.set_yticks([])

        ax.set_title(SUBS[i % 2], fontsize=8.5, pad=4, color="#333333")
        axes.append(ax)

    fig.canvas.draw()
    n_pairs = n_panels // 2
    for pair in range(n_pairs):
        ax_l = axes[pair * 2]
        ax_r = axes[pair * 2 + 1]
        bbox_l = ax_l.get_position()
        bbox_r = ax_r.get_position()
        xc = (bbox_l.x0 + bbox_r.x1) / 2
        yc = bbox_l.y1 + 0.06
        fig.text(xc, yc, f"t = {TIMES[pair]} m", ha="center", va="bottom",
                  fontsize=13, fontweight="bold")

    fig.text(0.5, 0.10, "Inter-KT-distance (µm)", ha="center", va="top", fontsize=10)

    legend_elems = [
        Line2D([0], [0], color=RED, lw=2.2, label="p-H2A"),
        Line2D([0], [0], color=ORANGE, lw=2.2, label="p-H3"),
    ]
    fig.legend(handles=legend_elems, loc="upper center", ncol=2, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, 1.0))

    fig.savefig(OUTPUT_PATH, dpi=220)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()