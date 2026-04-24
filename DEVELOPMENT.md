# Development

## Setup

Create a virtual environment and install dependencies:

```
make install
```

This creates `.venv/` and installs the packages listed in `requirements.txt` ([PyMuPDF](https://pymupdf.readthedocs.io/), pytest).

To set up manually without Make:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running tests

```
make test
```

Or directly via pytest inside the activated venv:

```
source .venv/bin/activate
pytest tests/ -v
```

There are two test modules:

- `tests/test_unit.py` — unit tests for `parse_replacements` and `output_path_for`
- `tests/test_acceptance.py` — end-to-end tests that create real PDFs and verify text replacement

## MCP server

`mcp_server.py` exposes `replace_text_in_pdf` as an MCP tool so other Claude Code sessions on this machine can call it directly.

It uses stdio transport — Claude Code spawns the process on demand, so no background server is needed.

### Registering with Claude Code

Register the server globally (available in all projects):

```
make mcp-install
```

The `replace_text_in_pdf` tool will then be available in any session. Verify with `claude mcp list`.

To unregister:

```
make mcp-remove
```

## Cleanup

Remove the virtual environment:

```
make clean
```
