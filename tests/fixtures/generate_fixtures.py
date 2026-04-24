"""Generate test fixture PDFs for the pdf_text_replace test suite.

Run this script whenever fixture PDFs need to be regenerated:
    .venv/bin/python tests/fixtures/generate_fixtures.py
"""
import os
import fitz

FIXTURES = os.path.dirname(os.path.abspath(__file__))


def generate_example_pdf():
    doc = fitz.open()

    # Page 1: standard named-replacement use case
    page = doc.new_page()
    page.insert_text((72, 100), "JOHN SMITH", fontsize=12)
    page.insert_text((72, 120), "Acme Co", fontsize=12)

    # Page 2: tight-spacing edge case — Times-Roman (tiro) has ascender ~1.053x,
    # so search_for rects extend beyond the line height and can overlap adjacent
    # lines at small font sizes. The adjacent line must survive unreplaced.
    page = doc.new_page()
    fontsize = 8.8
    page.insert_text((72, 100), "SPRINGFIELD PLANT", fontname="tiro", fontsize=fontsize)
    page.insert_text((72, 100 + fontsize), "SECTOR 7-G", fontname="tiro", fontsize=fontsize)

    doc.save(os.path.join(FIXTURES, "example.pdf"))
    doc.close()


if __name__ == "__main__":
    generate_example_pdf()
    print("Generated example.pdf")
