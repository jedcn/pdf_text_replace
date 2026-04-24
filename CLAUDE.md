# pdf_text_replace

## Environment

Always use the venv. Never invoke bare `python` or `pytest`.

```
make install   # creates .venv/ if it doesn't exist
make test      # runs the full test suite via .venv/bin/pytest
```

To run pytest directly: `.venv/bin/pytest tests/ -v`
To run the script directly: `.venv/bin/python pdf_text_replace.py`

## Project notes

- The main script is `pdf_text_replace.py`, importable as `pdf_text_replace`.
- Dependencies are PyMuPDF (`import fitz`) and pytest. Don't introduce other PDF libraries.

## Tests

New code should have tests. There are two test modules:

- `tests/test_unit.py` — unit tests for parsing and path helpers
- `tests/test_acceptance.py` — end-to-end tests that create real PDFs and verify replacement output
