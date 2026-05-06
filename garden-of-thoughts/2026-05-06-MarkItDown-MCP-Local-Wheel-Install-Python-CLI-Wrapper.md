# MarkItDown MCP: Local Wheel Install + Minimal Python CLI Wrapper

A compact pattern for converting PDFs (or any URI-supported input) to Markdown using a local `markitdown-mcp` server binary and an MCP client wrapper.
---

> **Series note**
>
> This writeup is **Part 1** in a small exploration of using **MarkItDown MCP** in practical workflows.
>
> - **Part 1**: *MarkItDown MCP: Local Wheel Install + Minimal Python CLI Wrapper*  
>   Covers local installation from a wheel package and wrapping MCP calls in a lightweight Python CLI for scriptable conversion.
>
> - **Part 2**: *MarkItDown MCP: Using Document Conversion in Agent Workflows*  
>   Covers exposing document conversion as a callable tool inside agent pipelines, where conversion becomes a reusable workflow step for summarization, extraction, indexing, and downstream reasoning.
>
> Part 1 is about **making conversion callable from scripts**.  
> Part 2 is about **making conversion callable from agents**.
>
> Same engine, different orchestra conductor 🎼🤖

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol for connecting AI models to external tools, data sources, and executable capabilities through a standard interface. Think of it as a common "tool bus" for AI applications, allowing models to discover and invoke tools consistently instead of relying on one-off custom integrations. :contentReference[oaicite:0]{index=0}

In this example, **MarkItDown MCP** exposes document conversion as an MCP tool, making PDF → Markdown conversion callable from scripts, editors, or agent workflows.

---

## Why this writeup

This writeup came out of solving three practical problems while working with VS Code + PDF->Markdown Conversion + MCP tooling:

1. **Could not install the extension from VS Code Extension UI**  
   The standard Extension Marketplace install path was unavailable in my corporate environment, so I needed a direct installation approach that bypassed editor-managed packaging.

2. **Understanding MCP server setup**  
   I wanted to understand the MCP server lifecycle end-to-end:

   ```text
   install → configure → launch → connect → invoke tools → handle failures
   ```

   Working with a local wheel made the server binary explicit and controllable, instead of hiding it behind editor abstractions.

3. **Creating a reusable MCP workflow via CLI wrapper**  
   Once the server was running, the next goal was ergonomics:

   - convert documents with a simple command
   - integrate into scripts
   - make MCP usage repeatable in automation pipelines

   A lightweight Python CLI wrapper became the cleanest interface.

In short:

- **Explicit install**
- **Explicit server control**
- **Scriptable workflow**

I’m always big on experimenting and automation, and this combination has been especially useful for trying ideas quickly, debugging when things go sideways, and turning repeatable work into something automated. ⚙️🌱.

---

## Why this setup

- **Reproducible**: pin exact server build from a `.whl`
- **Offline-friendly**: no marketplace dependency
- **Automatable**: scriptable conversion in pipelines
- **Transparent**: server path, version, and invocation are fully visible
- **Portable**: easy to move between machines / environments

---

## 1) Install MCP server from local wheel (Windows, venv)

```bash
# activate your venv first
pip install C:/path/to/markitdown_mcp-<version>-py3-none-any.whl
```

This creates a console entrypoint:

```text
.../.venv/Scripts/markitdown-mcp.exe
```

---

## 2) What the CLI wrapper does (high level)

1. Parse CLI args (`input`, `--out`, `--server`, `--timeout`)
2. Normalize input to URI (`file:`, `http:`, `https:`, `data:`)
3. Start MCP server over stdio
4. Initialize MCP session
5. Call tool: `convert_to_markdown`
   - The tool name is defined by the MCP tool contract exposed by the server; this is the tool identifier the client uses when invoking the conversion action.
   - You can find it by inspecting the server's tool registry or tool manifest, typically via MCP discovery APIs, server logs, or the package docs for `markitdown-mcp`.
   - In the wrapper, use `session.list_tools()` (exposed by the CLI as `--list-tools`) to discover the registered tool names from the specific MCP server being launched before calling `convert_to_markdown`.

   ```bash
   python ai-ml/markitdown_mcp_client_convert.py \
     --server "C:/.../.venv/Scripts/markitdown-mcp.exe" \
     --list-tools
   ```
6. Extract text response block
7. Write Markdown to file (or stdout)
8. Return nonzero exit code on failure

---

## 3) Minimal call pattern (core logic)

```python
result = await session.call_tool(
    "convert_to_markdown",
    {"uri": uri},
    read_timeout_seconds=timedelta(seconds=timeout_seconds),
)
```

---

## 4) Example usage

> Note: the wrapper script is located in the `ai-ml` folder as `markitdown_mcp_client_convert.py`.

```bash
C:/.../.venv/Scripts/python.exe scripts/markitdown_mcp_client_convert.py ^
  "docs/input.pdf" ^
  --out "docs/input.from_mcp.md"
```

> Here, `docs/input.pdf` is the input PDF file and `docs/input.from_mcp.md` is the generated Markdown output file.

---

## 5) Local wheel vs editor extension (quick distinction)

### Local wheel

Installs into your Python environment, creates:

```text
markitdown-mcp.exe
```

For Markdown conversion, this local server exposes the MCP tool:

```text
convert_to_markdown
```

Version is pinned by the wheel package.

### Editor extension

Editor-managed lifecycle and UX; package / binary location may be abstracted away.

For deterministic automation:

> **local wheel + virtual environment** is usually the better fit.

---

## 6) Practical tips

- Keep `--server` configurable (do not permanently hardcode it)
- Validate file existence before conversion
- Log timeout and server path on failures
- Pin package versions for repeatable output
- Wrap conversion into reusable shell / Python helpers
- Treat MCP server binaries like build dependencies: **explicit is better than magical**

---

## References / Links

### MCP

- Anthropic, **Introducing Model Context Protocol (official)**  
  [Model Context Protocol Overview](https://en.wikipedia.org/wiki/Model_Context_Protocol?utm_source=chatgpt.com)

- MCP Specification (GitHub)  
  https://github.com/modelcontextprotocol/specification

- MCP Python SDK  
  https://github.com/modelcontextprotocol/python-sdk

---

### MarkItDown

- Microsoft, **MarkItDown (official repo)**  
  https://github.com/microsoft/markitdown

---

### VS Code AI / tooling ecosystem

- VS Code documentation on MCP / AI extensibility  
  https://code.visualstudio.com/

---

## Closing thought

I’ve always liked tools that can be taken apart, understood, and wired into something bigger.

This pattern turns MCP into exactly that: **installable, inspectable, scriptable, and automatable**.

A small tool, perhaps, but the kind that can grow roots and branch into all sorts of workflows 🌱
