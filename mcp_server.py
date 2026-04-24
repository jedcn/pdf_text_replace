#!/usr/bin/env python3
"""MCP server exposing pdf_text_replace as a tool."""

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

from pdf_text_replace import output_path_for, parse_replacement_line, replace_text_in_pdf

server = Server("pdf_text_replace")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="replace_text_in_pdf",
            description=(
                "Replace text strings in a PDF file while preserving the original "
                "font, size, and color. Provide either inline replacements, a "
                "replacements file, or both."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Absolute path to the input PDF file.",
                    },
                    "replacements": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "List of replacement strings in 'OLD => NEW' format."
                        ),
                    },
                    "replacements_file": {
                        "type": "string",
                        "description": (
                            "Absolute path to a replacements file "
                            "(one 'OLD => NEW' entry per line; # lines are comments)."
                        ),
                    },
                    "output_path": {
                        "type": "string",
                        "description": (
                            "Absolute path for the output PDF. "
                            "Defaults to <input>_replaced.pdf."
                        ),
                    },
                },
                "required": ["input_path"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name != "replace_text_in_pdf":
        raise ValueError(f"Unknown tool: {name}")

    input_path = arguments["input_path"]
    inline = arguments.get("replacements") or []
    replacements_file = arguments.get("replacements_file")
    output_path = arguments.get("output_path") or output_path_for(input_path)

    if not inline and not replacements_file:
        raise ValueError("Provide at least one of 'replacements' or 'replacements_file'.")

    pairs = [parse_replacement_line(r) for r in inline]
    if replacements_file:
        from pdf_text_replace import parse_replacements
        pairs += parse_replacements(replacements_file)

    replace_text_in_pdf(input_path, pairs, output_path)
    return [types.TextContent(type="text", text=f"Created: {output_path}")]


async def main():
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
