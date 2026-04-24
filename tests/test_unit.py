import os
import tempfile

import pytest

from pdf_text_replace import output_path_for, parse_replacement_line, parse_replacements


def write_replacements(content):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


class TestParseReplacements:
    def test_single_line(self):
        path = write_replacements("Hello => World\n")
        assert parse_replacements(path) == [("Hello", "World")]

    def test_multiple_lines(self):
        path = write_replacements("Hello => World\nFoo => Bar\n")
        assert parse_replacements(path) == [("Hello", "World"), ("Foo", "Bar")]

    def test_blank_lines_skipped(self):
        path = write_replacements("\nHello => World\n\n")
        assert parse_replacements(path) == [("Hello", "World")]

    def test_value_containing_arrow(self):
        path = write_replacements("A => B => C\n")
        assert parse_replacements(path) == [("A", "B => C")]

    def test_strips_whitespace(self):
        path = write_replacements("  Hello  =>  World  \n")
        assert parse_replacements(path) == [("Hello", "World")]

    def test_comment_lines_skipped(self):
        path = write_replacements("# this is a comment\nHello => World\n")
        assert parse_replacements(path) == [("Hello", "World")]


class TestParseReplacementLine:
    def test_basic(self):
        assert parse_replacement_line("Hello => World") == ("Hello", "World")

    def test_strips_whitespace(self):
        assert parse_replacement_line("  Hello  =>  World  ") == ("Hello", "World")

    def test_arrow_in_new_text(self):
        assert parse_replacement_line("A => B => C") == ("A", "B => C")

    def test_missing_arrow_raises(self):
        with pytest.raises(ValueError):
            parse_replacement_line("no arrow here")


class TestOutputPathFor:
    def test_simple(self):
        assert output_path_for("example.pdf") == "example_replaced.pdf"

    def test_with_directory(self):
        assert output_path_for("dir/foo.pdf") == "dir/foo_replaced.pdf"

    def test_uppercase_extension(self):
        assert output_path_for("file.PDF") == "file_replaced.PDF"
