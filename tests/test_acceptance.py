import os
import subprocess
import sys
import tempfile

import fitz
import pytest

from pdf_text_replace import parse_replacements, replace_text_in_pdf

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def make_pdf(text_per_page):
    """Create a temporary PDF with known text on each page. Returns file path."""
    doc = fitz.open()
    for text in text_per_page:
        page = doc.new_page()
        page.insert_text((72, 72), text, fontsize=12)
    f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    doc.save(f.name)
    doc.close()
    f.close()
    return f.name


def full_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text


class TestBasicReplacement:
    def test_replaces_matching_text(self, tmp_path):
        input_path = make_pdf(["Hello World"])
        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(input_path, [("Hello", "Goodbye")], output_path)
        result = full_text(output_path)
        assert "Goodbye" in result
        assert "Hello" not in result

    def test_multiple_replacements(self, tmp_path):
        input_path = make_pdf(["Alpha Beta"])
        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(input_path, [("Alpha", "One"), ("Beta", "Two")], output_path)
        result = full_text(output_path)
        assert "One" in result
        assert "Two" in result
        assert "Alpha" not in result
        assert "Beta" not in result

    def test_multipage(self, tmp_path):
        input_path = make_pdf(["Page One Text", "Page Two Text"])
        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(input_path, [("One", "1"), ("Two", "2")], output_path)
        result = full_text(output_path)
        assert "1" in result
        assert "2" in result
        assert "One" not in result
        assert "Two" not in result

    def test_no_match_creates_valid_output(self, tmp_path):
        input_path = make_pdf(["Some content here"])
        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(input_path, [("NOMATCH", "anything")], output_path)
        assert os.path.exists(output_path)
        doc = fitz.open(output_path)
        assert doc.page_count == 1
        doc.close()

    def test_replacement_uses_original_font_size(self, tmp_path):
        # make_pdf inserts text at fontsize=12; the replacement should match.
        input_path = make_pdf(["Hello World"])
        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(input_path, [("Hello", "Goodbye")], output_path)
        doc = fitz.open(output_path)
        page = doc[0]
        found = False
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if "Goodbye" in span["text"]:
                        assert abs(span["size"] - 12) < 0.5
                        found = True
        assert found, "replacement text not found in output"
        doc.close()

    def test_adjacent_lines_not_erased_with_tight_spacing(self, tmp_path):
        # Times-Roman (tiro) has ascender=1.053, so at fontsize=8.8 span bboxes
        # extend ~9.27pt above baseline. With lines spaced only 8.8pt apart the
        # bboxes overlap by ~2.9pt, and a naive rect-based redaction would erase
        # the adjacent line. Verify that only the target line is replaced.
        fontsize = 8.8
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 100), "ACME CORPORATION", fontname="tiro", fontsize=fontsize)
        page.insert_text((72, 100 + fontsize), "123 MAIN STREET", fontname="tiro", fontsize=fontsize)
        f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        doc.save(f.name)
        doc.close()
        f.close()

        output_path = str(tmp_path / "out.pdf")
        replace_text_in_pdf(f.name, [("ACME CORPORATION", "GLOBEX CORPORATION")], output_path)
        result = full_text(output_path)
        assert "GLOBEX CORPORATION" in result
        assert "ACME CORPORATION" not in result
        assert "123 MAIN STREET" in result


class TestReplaceFlag:
    def test_single_replace_arg(self, tmp_path):
        input_path = make_pdf(["Hello World"])
        output_path = str(tmp_path / "out.pdf")
        script = os.path.join(os.path.dirname(__file__), "..", "pdf_text_replace.py")
        subprocess.run(
            [sys.executable, script, "--input", input_path, "--replace", "Hello => Goodbye", "--output", output_path],
            check=True,
        )
        result = full_text(output_path)
        assert "Goodbye" in result
        assert "Hello" not in result

    def test_multiple_replace_args(self, tmp_path):
        input_path = make_pdf(["Alpha Beta"])
        output_path = str(tmp_path / "out.pdf")
        script = os.path.join(os.path.dirname(__file__), "..", "pdf_text_replace.py")
        subprocess.run(
            [sys.executable, script, "--input", input_path,
             "--replace", "Alpha => One", "--replace", "Beta => Two",
             "--output", output_path],
            check=True,
        )
        result = full_text(output_path)
        assert "One" in result
        assert "Two" in result

    def test_neither_flag_exits_nonzero(self, tmp_path):
        input_path = make_pdf(["Hello World"])
        script = os.path.join(os.path.dirname(__file__), "..", "pdf_text_replace.py")
        result = subprocess.run(
            [sys.executable, script, "--input", input_path],
            capture_output=True,
        )
        assert result.returncode != 0


class TestExamplePdf:
    @pytest.fixture
    def replaced_pdf(self, tmp_path):
        input_path = os.path.join(FIXTURES, "example.pdf")
        output_path = str(tmp_path / "example_replaced.pdf")
        replacements_path = os.path.join(FIXTURES, "example_replacements.txt")
        replacements = parse_replacements(replacements_path)
        replace_text_in_pdf(input_path, replacements, output_path)
        return output_path

    def test_named_replacements(self, replaced_pdf):
        assert os.path.exists(replaced_pdf)
        result = full_text(replaced_pdf)
        assert "JANE DOE" in result
        assert "Theta Co" in result
        assert "JOHN SMITH" not in result
        assert "Acme Co" not in result

    def test_tight_spacing_adjacent_line_preserved(self, replaced_pdf):
        result = full_text(replaced_pdf)
        assert "SPRINGFIELD NUCLEAR" in result
        assert "SPRINGFIELD PLANT" not in result
        assert "SECTOR 7-G" in result
