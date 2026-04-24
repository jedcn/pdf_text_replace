# pdf_text_replace

Replace text strings in a PDF while preserving the original font, size, and color.

## Usage

```
pdf_text_replace.py --input <file.pdf> --replace "OLD => NEW" [--replace "..."] [--output <output.pdf>]
pdf_text_replace.py --input <file.pdf> --replacements-file <replacements.txt> [--output <output.pdf>]
```

* At least one of `--replace` or `--replacements-file` is required. Both can be combined.
* If `--output` is not specified, the word `_replaced` is appended to the input file

| Flag | Description |
|---|---|
| `--input` | Input PDF file (required) |
| `--replace` | A single replacement string `OLD => NEW` (repeatable) |
| `--replacements-file` | File of replacements (see format below) |
| `--output` | Output PDF path (default: `<input>_replaced.pdf`) |

## Replacements file format

Each line specifies one substitution using `=>` as the separator.

Blank lines and lines starting with `#` are ignored.

```
OLD => NEW
Taco Bell => Del Taco
```

This project also comes with an [mcp_server.py](mcp_server.py).

The mcp portion can be managed with `make mcp-install` and `make mcp-remove`

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, running tests, and installing/removing the mcp.
