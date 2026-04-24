.PHONY: test generate-fixtures mcp-install mcp-remove

test:
	pytest tests/ -v

generate-fixtures:
	python3 tests/fixtures/generate_fixtures.py

mcp-install: .venv
	claude mcp add --scope user pdf_text_replace $(CURDIR)/.venv/bin/python $(CURDIR)/mcp_server.py

mcp-remove:
	claude mcp remove --scope user pdf_text_replace
