# pdf_text_replace

Replace text strings in a PDF while preserving the original font, size, and color.

## Usage

```
python pdf_text_replace.py --input <file.pdf> --replace "OLD => NEW" [--replace "..."] [--output <output.pdf>]
python pdf_text_replace.py --input <file.pdf> --replacements-file <replacements.txt> [--output <output.pdf>]
```

At least one of `--replace` or `--replacements-file` is required. Both can be combined.

| Flag | Description |
|---|---|
| `--input` | Input PDF file (required) |
| `--replace` | A single replacement string `OLD => NEW` (repeatable) |
| `--replacements-file` | File of replacements (see format below) |
| `--output` | Output PDF path (default: `<input>_replaced.pdf`) |

## Replacements file format

Each line specifies one substitution using `=>` as the separator. Blank lines and lines starting with `#` are ignored.

```
JOHN SMITH => JANE DOE
Acme Co => Theta Co
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, running tests, and venv usage.

## Examples

```
# Single inline replacement
python pdf_text_replace.py --input statement.pdf --replace "JOHN SMITH => JANE DOE"

# Multiple inline replacements
python pdf_text_replace.py --input statement.pdf --replace "JOHN SMITH => JANE DOE" --replace "Acme Co => Theta Co"

# From a replacements file
python pdf_text_replace.py --input statement.pdf --replacements-file replacements.txt

# Explicit output path
python pdf_text_replace.py --input statement.pdf --replacements-file replacements.txt --output redacted.pdf
```

## Running from another directory

Activate the venv once, then invoke the script by its full path. Your `--input`, `--replacements-file`, and `--output` paths can be relative to wherever you are.

```
source ~/pdf_text_replace/.venv/bin/activate
python ~/pdf_text_replace/pdf_text_replace.py --input ./input.pdf --replacements-file ./replacements.txt --output ./output.pdf
```
