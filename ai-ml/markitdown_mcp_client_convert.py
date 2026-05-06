# markitdown_mcp_client_convert.py
"""
Purpose: A Python CLI wrapper function to use markdown mcp server for experiment.
Author: Sherry
Coding Assistant: Codex
Date: 4/20/2026
"""

from __future__ import annotations

import argparse
import sys
from datetime import timedelta
from pathlib import Path

import anyio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


def to_uri(value: str) -> str:
    # If user already provided a URI (file:/http:/https:/data:), pass through.
    lowered = value.lower()
    if lowered.startswith(("file:", "http:", "https:", "data:")):
        return value

    path = Path(value).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    return path.as_uri()


async def run_convert(server_command: str, uri: str, timeout_seconds: int) -> str:
    server = StdioServerParameters(command=server_command)

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                "convert_to_markdown",
                {"uri": uri},
                read_timeout_seconds=timedelta(seconds=timeout_seconds),
            )

            if getattr(result, "isError", False):
                raise RuntimeError(f"Tool returned isError=True: {result}")

            # MCP tool results return a list of typed content blocks.
            # markitdown-mcp returns text.
            for item in result.content:
                if getattr(item, "type", None) == "text":
                    return item.text

            raise RuntimeError(
                f"Unexpected tool result content: {result.content}"
            )


async def run_list_tools(server_command: str) -> list[tuple[str, str]]:
    server = StdioServerParameters(command=server_command)

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()

            return [
                (tool.name, getattr(tool, "description", "") or "")
                for tool in tools.tools
            ]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Call the markitdown-mcp server to convert a PDF "
            "(or URI) to Markdown."
        )
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Path to a local file or a URI (file:/http:/https:/data:)",
    )

    parser.add_argument(
        "--server",
        default=str(
            Path(r"C:/Users/x794471/RAVA/.venv/Scripts/markitdown-mcp.exe")
        ),
        help="Path to the markitdown-mcp server executable (STDIO transport).",
    )

    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List registered tools exposed by the MCP server and exit.",
    )

    parser.add_argument(
        "--out",
        default=None,
        help="Output .md file path. If omitted, prints to stdout.",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Tool call timeout (seconds).",
    )

    args = parser.parse_args(argv)

    try:
        if args.list_tools:
            tools = anyio.run(run_list_tools, args.server)

            if not tools:
                print("No tools returned by server.")
                return 0

            print("Registered MCP tools:")
            for name, desc in tools:
                if desc:
                    print(f"- {name}: {desc}")
                else:
                    print(f"- {name}")

            return 0

        if not args.input:
            parser.error(
                "the following arguments are required: "
                "input (unless --list-tools is used)"
            )

        uri = to_uri(args.input)
        md = anyio.run(run_convert, args.server, uri, args.timeout)

        if args.out:
            out_path = Path(args.out).expanduser().resolve()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8")
            print(f"Wrote: {out_path}")
        else:
            sys.stdout.write(md)

        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))