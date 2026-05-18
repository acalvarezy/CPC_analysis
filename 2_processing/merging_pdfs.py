#Merging plots in different pfds
from pypdf import PdfWriter
import os

os.chdir('/Users/catalinaalvarez/Documents/CPC_plots_2026/figures/lineplot_across_sims/')

def merge_pdfs(output_filename, input_pdfs):
    # Initialize the writer
    merger = PdfWriter()

    for pdf in input_pdfs:
        # Append the entire PDF file to the writer
        merger.append(pdf)

    # Save the result
    merger.write(output_filename)
    merger.close()

# Example usage
plots = ["Comparison arms _0%_kt_bg_500s.pdf",
        "Comparison arms _5%_kt_bg_500s.pdf",
        "Comparison arms _10%_kt_bg_500s.pdf",
        "Comparison arms _15%_kt_bg_500s.pdf",
        "Comparison arms _20%_kt_bg_500s.pdf",
        "Comparison arms _25%_kt_bg_500s.pdf",
        "Comparison arms _30%_kt_bg_500s.pdf",
        "Comparison arms _35%_kt_bg_500s.pdf",
        "Comparison arms _40%_kt_bg_500s.pdf",
        "Comparison arms _45%_kt_bg_500s.pdf",
        "Comparison arms _50%_kt_bg_500s.pdf",
        "Comparison arms _55%_kt_bg_500s.pdf",
        "Comparison arms _60%_kt_bg_500s.pdf",
        "Comparison arms _65%_kt_bg_500s.pdf",
        "Comparison arms _70%_kt_bg_500s.pdf",
        "Comparison arms _75%_kt_bg_500s.pdf",
        "Comparison arms _80%_kt_bg_500s.pdf",
        "Comparison arms _85%_kt_bg_500s.pdf",
        "Comparison arms _90%_kt_bg_500s.pdf",
        "Comparison arms _95%_kt_bg_500s.pdf",
        "Comparison arms _100%_kt_bg_500s.pdf"
         ]
merge_pdfs("combined_plots_kt.pdf", plots)
