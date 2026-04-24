.PHONY: install clean test generate-fixtures mcp-install mcp-remove

.venv:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt -q

install: .venv

clean:
	rm -rf .venv

test: .venv
	.venv/bin/pytest tests/ -v

generate-fixtures: .venv
	.venv/bin/python tests/fixtures/generate_fixtures.py

mcp-install: .venv
	claude mcp add --scope user pdf_text_replace $(CURDIR)/.venv/bin/python $(CURDIR)/mcp_server.py

mcp-remove:
	claude mcp remove --scope user pdf_text_replace
