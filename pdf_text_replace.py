#!/usr/bin/env python3
import argparse
import os

import fitz

# Maps font name keywords to base-14 PDF font families
_SERIF_KEYWORDS = {"serif", "times", "georgia", "palatino", "garamond", "liberation serif"}
_MONO_KEYWORDS = {"mono", "courier", "code", "consolas", "menlo", "inconsolata"}


def _normalize_font(font_name):
    lower = font_name.lower()
    bold = "bold" in lower
    italic = "italic" in lower or "oblique" in lower
    is_serif = any(k in lower for k in _SERIF_KEYWORDS)
    is_mono = any(k in lower for k in _MONO_KEYWORDS)

    if is_mono:
        if bold and italic:
            return "Courier-BoldOblique"
        if bold:
            return "Courier-Bold"
        if italic:
            return "Courier-Oblique"
        return "Courier"
    if is_serif:
        if bold and italic:
            return "Times-BoldItalic"
        if bold:
            return "Times-Bold"
        if italic:
            return "Times-Italic"
        return "Times-Roman"
    if bold and italic:
        return "Helvetica-BoldOblique"
    if bold:
        return "Helvetica-Bold"
    if italic:
        return "Helvetica-Oblique"
    return "Helvetica"


def _page_spans(page):
    spans = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                color = span["color"]
                rgb = (((color >> 16) & 0xFF) / 255, ((color >> 8) & 0xFF) / 255, (color & 0xFF) / 255)
                spans.append((
                    fitz.Rect(span["bbox"]),
                    span["font"],
                    span["size"],
                    fitz.Point(span["origin"]),
                    rgb,
                    span["ascender"],
                    span["descender"],
                ))
    return spans


def _span_for_rect(spans, rect):
    best_area = 0
    best = ("Helvetica", 11, None, (0, 0, 0), 0.8, -0.2)
    for span_rect, font, size, origin, color, ascender, descender in spans:
        overlap = rect & span_rect
        if not overlap.is_empty:
            area = overlap.width * overlap.height
            if area > best_area:
                best_area = area
                best = (_normalize_font(font), size, origin, color, ascender, descender)
    return best


def _trim_rect_to_line(search_rect, match_origin_y, all_spans):
    """Trim a search_for rect to the space between adjacent overlapping spans.

    Large font ascender/descender values can make search_for return a rect
    taller than the visual line, causing apply_redactions() to erase adjacent
    content. This trims the rect to stop at the boundary of any span above or
    below that the rect is incorrectly overlapping.
    """
    top = search_rect.y0
    bottom = search_rect.y1
    for span_rect, _, _, origin, *_ in all_spans:
        if origin is None or abs(origin.y - match_origin_y) < 1.0:
            continue  # same line as the match, skip
        overlap = search_rect & span_rect
        if overlap.is_empty:
            continue
        if origin.y < match_origin_y:  # span is above the match
            top = max(top, span_rect.y1)
        else:  # span is below the match
            bottom = min(bottom, span_rect.y0)
    if top >= bottom:  # degenerate case: use a 2pt slice at the baseline
        top = match_origin_y - 1
        bottom = match_origin_y + 1
    return fitz.Rect(search_rect.x0, top, search_rect.x1, bottom)


def parse_replacement_line(line):
    if "=>" not in line:
        raise ValueError(f"Invalid replacement (expected 'OLD => NEW'): {line!r}")
    old, new = line.split("=>", 1)
    return (old.strip(), new.strip())


def parse_replacements(file_path):
    replacements = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=>" in line:
                replacements.append(parse_replacement_line(line))
    return replacements


def output_path_for(input_path):
    base, ext = os.path.splitext(input_path)
    return f"{base}_replaced{ext}"


def replace_text_in_pdf(input_path, replacements, output_path):
    doc = fitz.open(input_path)
    for page in doc:
        spans = _page_spans(page)
        insertions = []
        for old_text, new_text in replacements:
            rects = page.search_for(old_text)
            if rects:
                print(f"  Page {page.number + 1}: {old_text!r} => {new_text!r} ({len(rects)}x)")
            for rect in rects:
                fontname, fontsize, origin, color, ascender, descender = _span_for_rect(spans, rect)
                match_origin_y = origin.y if origin else (rect.y0 + rect.y1) / 2
                redact_rect = _trim_rect_to_line(rect, match_origin_y, spans)
                page.add_redact_annot(redact_rect, fill=(1, 1, 1))
                baseline = fitz.Point(rect.x0, origin.y if origin else rect.y1)
                insertions.append((baseline, new_text, fontname, fontsize, color))
        page.apply_redactions()
        for point, text, fontname, fontsize, color in insertions:
            page.insert_text(point, text, fontname=fontname, fontsize=fontsize, color=color)
    doc.save(output_path)
    doc.close()


def main():
    parser = argparse.ArgumentParser(description="Replace text strings in a PDF file.")
    parser.add_argument("--input", required=True, help="Input PDF file")
    parser.add_argument("--replace", action="append", metavar="OLD => NEW",
                        help="A single replacement (repeatable)")
    parser.add_argument("--replacements-file", metavar="FILE",
                        help="File of replacements (format: Old => New, one per line)")
    parser.add_argument("--output", help="Output PDF path (default: <input>_replaced.pdf)")
    args = parser.parse_args()

    if not args.replace and not args.replacements_file:
        parser.error("at least one of --replace or --replacements-file is required")

    replacements = [parse_replacement_line(r) for r in (args.replace or [])]
    if args.replacements_file:
        replacements += parse_replacements(args.replacements_file)

    for old, new in replacements:
        print(f"  {old!r} => {new!r}")
    output_path = args.output if args.output else output_path_for(args.input)
    replace_text_in_pdf(args.input, replacements, output_path)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
