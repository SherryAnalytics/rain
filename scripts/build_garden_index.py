"""Read all markdown files in garden-of-thoughts/ and rebuild index.html.

Usage:
  uv run python scripts/build_garden_index.py

Changelog:
  2026-06-07  Initial version — extracted from convert_md_to_html.py.
              - Reads frontmatter (title, date) from each .md file.
              - Rebuilds garden-of-thoughts/index.html sorted newest-first.
              - Matches root index.html font (system sans-serif) and color scheme (#dce8f5).
"""

import yaml
from pathlib import Path
from datetime import date

GARDEN_DIR = Path(__file__).parent.parent / "garden-of-thoughts"

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Garden of Thoughts — SherryAnalytics</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
      background-color: #dce8f5;
      color: #111;
      min-height: 100vh;
      padding: 48px 56px 48px 96px;
    }}
    .back {{ font-size: 0.85rem; margin-bottom: 48px; }}
    .back a {{ color: #5a8ab0; text-decoration: none; font-weight: 500; }}
    .back a:hover {{ opacity: 0.7; }}
    h1 {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      border-bottom: 2px solid #5a8ab0;
      padding-bottom: 16px;
      margin-bottom: 12px;
    }}
    .subtitle {{
      font-size: 1rem;
      color: #445;
      margin-bottom: 48px;
    }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 0; padding: 20px 0; border-bottom: 1px solid #b8cfdf; }}
    li a {{
      font-size: 1.05rem;
      font-weight: 600;
      color: #111;
      text-decoration: none;
    }}
    li a:hover {{ color: #5a8ab0; }}
    .date {{ font-size: 0.82rem; color: #667; margin-top: 4px; }}
  </style>
</head>
<body>
  <div class="back"><a href="../">← Back to Rain</a></div>
  <h1>🌱 Garden of Thoughts</h1>
  <p class="subtitle">Personal reflections on data engineering, Python coding, AI tools, and cloud practice, projects I am imagining.</p>
  <ul>
{items}
  </ul>
</body>
</html>"""

INDEX_ITEM = """\
    <li>
      <a href="{filename}">{title}</a>
      <div class="date">{date_str}</div>
    </li>"""


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.index("---", 3)
    return yaml.safe_load(text[3:end]) or {}


def format_date(d) -> str:
    if isinstance(d, date):
        return d.strftime("%B %-d, %Y")
    return str(d)


def main():
    md_files = sorted(GARDEN_DIR.glob("*.md"))
    if not md_files:
        print("No markdown files found.")
        return

    articles = []
    for f in md_files:
        meta = parse_frontmatter(f.read_text(encoding="utf-8"))
        title = meta.get("title", f.stem).strip('"')
        d = meta.get("date")
        articles.append((f.stem + ".html", title, d, format_date(d)))

    articles.sort(key=lambda x: x[2] or date.min, reverse=True)

    items = "\n".join(
        INDEX_ITEM.format(filename=fname, title=title, date_str=date_str)
        for fname, title, _, date_str in articles
    )

    index_path = GARDEN_DIR / "index.html"
    index_path.write_text(INDEX_TEMPLATE.format(items=items), encoding="utf-8")
    print(f"  rebuilt index.html with {len(articles)} entries")


if __name__ == "__main__":
    main()
