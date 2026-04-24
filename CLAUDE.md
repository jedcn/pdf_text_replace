# pdf_text_replace

## Environment

Dependencies (PyMuPDF and pytest) are installed globally via Homebrew.

```
make test      # runs the full test suite
```

To run pytest directly: `pytest tests/ -v`
To run the script directly: `./pdf_text_replace.py`

## Project notes

- The main script is `pdf_text_replace.py`, importable as `pdf_text_replace`.
- Dependencies are PyMuPDF (`import fitz`) and pytest. Don't introduce other PDF libraries.

## Tests

New code should have tests. There are two test modules:

- `tests/test_unit.py` — unit tests for parsing and path helpers
- `tests/test_acceptance.py` — end-to-end tests that create real PDFs and verify replacement output
