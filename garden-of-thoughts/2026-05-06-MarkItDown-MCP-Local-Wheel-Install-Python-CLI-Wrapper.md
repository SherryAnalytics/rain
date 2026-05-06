# MarkItDown MCP: Local Wheel Install + Minimal Python CLI Wrapper

A compact pattern for converting PDFs (or any URI-supported input) to Markdown using a local `markitdown-mcp` server binary and an MCP client wrapper.

---

## Why this writeup

This writeup came out of solving three practical problems while working with VS Code + MCP tooling:

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

That combination is ideal for experimentation, debugging, and automation.

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

```bash
C:/.../.venv/Scripts/python.exe scripts/markitdown_mcp_client_convert.py ^
  "docs/input.pdf" ^
  --out "docs/input.from_mcp.md"
```

---

## 5) Local wheel vs editor extension (quick distinction)

### Local wheel

Installs into your Python environment, creates:

```text
markitdown-mcp.exe
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

## Closing thought

This pattern turns MCP from an editor feature into an engineering building block:

**installable, inspectable, scriptable, and automatable**.

That is usually where good tooling begins.
