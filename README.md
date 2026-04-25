# pdf_text_replace

Replace text strings in a PDF while preserving the original font, size, and color.

## Example

Imagine a PDF exists in the world named `f15314.pdf` and you could get it on your machine via `wget https://www.irs.gov/pub/irs-pdf/f15314.pdf`.

When you open up this form, you see it has text with "Form 15314" and "April 2026" in it like so:

![before](docs/before.png)

Imagine you want to change `April 2026` to `May 2026` and that form number `15314` to `26425`.

With pdf_text_replace you can run:

```
pdf_text_replace.py \
  --input f15314.pdf \
  --replace "April 2026 => May 2026" \
  --replace "15314 => 26425"
```

And you'd see the following output:

```
 'April 2026' => 'May 2026'
 '15314' => '26425'
  Page 1: 'April 2026' => 'May 2026' (1x)
  Page 1: '15314' => '26425' (2x)
Created: f15314_replaced.pdf
```

And when you open the newly created PDF you'd get:

![after](docs/after.png)

This style of invocation uses two `--replace` arguments.

You could also put all of the replacements you wanted to make in a file and direct the script to use that file with `--replacements`:

```
# Comments Allowed
A => ONE
B => TWO
C => THREE
D => FOUR
```

## MCP Example

This project also provides an MCP Server that you can register (claude code used below) so you could ask an agent like so:

```
❯ Can you please replace some text in the pdf @f15314.pdf? Change the
  date "April 2026" to "May 2026", and the form number 15314 to 26425
  ⎿  Read f15314.pdf (64.6KB)

⏺ I'll load the PDF text replace tool schema first.

⏺ Now I'll make both replacements in one call.

  Called pdf_text_replace (ctrl+o to expand)

⏺ I'll save to a new file instead, then we can rename if needed.

  Called pdf_text_replace (ctrl+o to expand)

⏺ Done. Both replacements were applied and the result is saved as
  f26425.pdf (renaming the file to match the new form number seemed
  appropriate). The original f15314.pdf is unchanged.
```

## Exhaustive Usage

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

The [mcp aspect](mcp_server.py) of this project can be managed with `make mcp-install` and `make mcp-remove`

## Running Locally

See [VENV.md](VENV.md) for virtual environment setup (including optional direnv integration)

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for running tests and installing/removing the MCP server.
