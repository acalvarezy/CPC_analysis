"""
Build a single combined heatmap figure from the two original faceted-heatmap
images (Metacentric Tensed and Metacentric Relaxed models).

For each time point, the Relaxed panel is placed directly next to the Tensed
panel, sharing one time axis and one colorbar.

Usage:
    python make_combined_plot.py

Just make sure TENSED_IMG_PATH and RELAXED_IMG_PATH below point to your two
source PNGs, then run the script. It writes "combined_intercalated.png".
"""

from PIL import Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.colorbar
import matplotlib.colors as mcolors

# ---------------------------------------------------------------------------
# 1. Inputs — point these at your two original figures
# ---------------------------------------------------------------------------
TENSED_IMG_PATH = "Metacentric_Tensed_Model.png"
RELAXED_IMG_PATH = "Metacentric_Relaxed_Model.png"
OUTPUT_PATH = "combined_intercalated.png"

# Pixel bounding boxes of the 7 heatmap panels (t = 0, 0.2, 2, 4, 5, 6, 8)
# and of the plotted region's vertical extent, measured on the *original*
# 3000x1500 px renders. If you regenerate the source figures at a different
# resolution/layout, these will need to be re-measured.
PANEL_X_RANGES = [
    (267, 595),   # t = 0
    (650, 977),   # t = 0.2
    (1033, 1360), # t = 2
    (1415, 1743), # t = 4
    (1798, 2125), # t = 5
    (2180, 2508), # t = 6
    (2563, 2890), # t = 8
]
TIMES = ["0", "0.2", "2", "4", "5", "6", "8"]
PANEL_Y_TOP, PANEL_Y_BOTTOM = 203, 1048

# Axis extents shown in the source plots
X_EXTENT = (0, 1.3)   # µm
Y_EXTENT = (0, 3.4)   # µm
X_TICKS = [0, 0.7, 1.3]
Y_TICKS = [0, 1.7, 3.4]

# Colorbar scale used in the source plots
CBAR_MIN, CBAR_MAX = 0, 11
CBAR_TICKS = [0, 2.75, 5.5, 8.25, 11]
CBAR_LABEL = "[all bound CPC] (µM)"


def flatten_to_white(path):
    """Composite an RGBA PNG onto a white background (removes transparency)."""
    im = Image.open(path).convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[3])
    return bg


def get_tile(img, x_range):
    a, b = x_range
    return np.array(img.crop((a, PANEL_Y_TOP, b, PANEL_Y_BOTTOM)))


def main():
    flat_tensed = flatten_to_white(TENSED_IMG_PATH)
    flat_relaxed = flatten_to_white(RELAXED_IMG_PATH)

    tensed_tiles = [get_tile(flat_tensed, xr) for xr in PANEL_X_RANGES]
    relaxed_tiles = [get_tile(flat_relaxed, xr) for xr in PANEL_X_RANGES]

    n = len(TIMES)

    # Two columns per time point (Relaxed, Tensed) + a thin spacer column
    # between consecutive time points.
    width_ratios = []
    for i in range(n):
        width_ratios += [1, 1]
        if i != n - 1:
            width_ratios += [0.28]

    fig = plt.figure(figsize=(21, 6.6))
    gs = gridspec.GridSpec(
        1, len(width_ratios), figure=fig, wspace=0.12,
        width_ratios=width_ratios,
        left=0.035, right=0.995, top=0.80, bottom=0.30,
    )

    # Map each time-point index to its (left, right) column indices in gs
    col_positions = []
    c = 0
    for i in range(n):
        col_positions.append((c, c + 1))
        c += 2
        if i != n - 1:
            c += 1

    axes_pairs = []
    for i in range(n):
        cl, _ = col_positions[i]
        pair_axes = []
        for j, (tile, letter) in enumerate(
            [(relaxed_tiles[i], "R"), (tensed_tiles[i], "T")]
        ):
            ax = fig.add_subplot(gs[0, cl + j])
            ax.imshow(
                tile,
                extent=[X_EXTENT[0], X_EXTENT[1], Y_EXTENT[0], Y_EXTENT[1]],
                aspect="auto",
            )
            ax.set_xticks(X_TICKS)
            ax.set_xticklabels([str(t) for t in X_TICKS], fontsize=7.5, rotation=45)

            if i == 0 and j == 0:
                ax.set_yticks(Y_TICKS)
                ax.tick_params(axis="y", labelsize=8.5)
                ax.set_ylabel("Y (µm)", fontsize=10)
            else:
                ax.set_yticks([])

            # Model-identity marker, top-left corner, plain white
            ax.text(
                0.06, 0.975, letter, transform=ax.transAxes,
                fontsize=13, fontweight="bold", color="white",
                ha="left", va="top",
            )
            pair_axes.append(ax)
        axes_pairs.append(pair_axes)

    fig.canvas.draw()

    # Time-point labels, centered over each Relaxed/Tensed pair
    for i in range(n):
        ax_l, ax_r = axes_pairs[i]
        bbox_l = ax_l.get_position()
        bbox_r = ax_r.get_position()
        xc = (bbox_l.x0 + bbox_r.x1) / 2
        yc = bbox_l.y1 + 0.018
        fig.text(xc, yc, f"{TIMES[i]} min", ha="center", va="bottom", fontsize=16)

    # Shared x-axis caption
    fig.text(0.5, 0.145, "X (µm)", ha="center", va="top", fontsize=10)

    # Shared colorbar
    cbar_ax = fig.add_axes([0.38, 0.05, 0.24, 0.028])
    norm = mcolors.Normalize(vmin=CBAR_MIN, vmax=CBAR_MAX)
    cb = matplotlib.colorbar.ColorbarBase(
        cbar_ax, cmap="viridis", norm=norm, orientation="horizontal",
        ticks=CBAR_TICKS,
    )
    cb.ax.tick_params(labelsize=7.5, rotation=0)
    cb.set_label(CBAR_LABEL, fontsize=8.5, labelpad=2)

    fig.suptitle(
        "Metacentric model: Relaxed vs Tensed bound CPC per time point",
        fontsize=13, y=0.99,
    )

    fig.savefig(OUTPUT_PATH, dpi=220)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()