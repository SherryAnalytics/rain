"""Convert all markdown files in garden-of-thoughts/ to HTML and rebuild index.html.

uv run python scripts/convert_md_to_html.py

Changelog:
  2026-06-05  Initial version — converts all .md files, rebuilds index.html.
  2026-06-05  Skip conversion if .html already exists and is newer than .md.
"""

import yaml
import markdown
from pathlib import Path
from datetime import date

GARDEN_DIR = Path(__file__).parent.parent / "garden-of-thoughts"

ARTICLE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title} — SherryAnalytics</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 720px; margin: 60px auto; padding: 0 24px; color: #222; }}
    h1, h2, h3 {{ line-height: 1.3; }}
    h1 {{ font-size: 1.9rem; border-bottom: 2px solid #222; padding-bottom: 12px; }}
    p {{ line-height: 1.7; color: #333; }}
    a {{ color: #0066cc; }}
    a:hover {{ color: #004499; }}
    code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
    pre {{ background: #f4f4f4; padding: 16px; border-radius: 6px; overflow-x: auto; }}
    pre code {{ background: none; padding: 0; }}
    blockquote {{ border-left: 3px solid #ccc; margin: 0; padding: 0 16px; color: #555; }}
    .back {{ font-size: 0.9rem; margin-bottom: 32px; }}
    .back a {{ text-decoration: none; }}
    .meta {{ font-size: 0.85rem; color: #888; margin-top: 6px; margin-bottom: 32px; }}
    .tag {{ background: #eee; border-radius: 3px; padding: 2px 8px; margin-right: 4px; font-size: 0.8rem; }}
  </style>
</head>
<body>
  <div class="back"><a href="index.html">← Garden of Thoughts</a></div>
  <h1>{title}</h1>
  <div class="meta">
    <span>{date_str}</span>
    {tags_html}
  </div>
  {body}
</body>
</html>"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Garden of Thoughts — SherryAnalytics</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 720px; margin: 60px auto; padding: 0 24px; color: #222; }}
    h1 {{ font-size: 2rem; border-bottom: 2px solid #222; padding-bottom: 12px; }}
    .back {{ font-size: 0.9rem; margin-bottom: 32px; }}
    .back a {{ color: #0066cc; text-decoration: none; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ margin: 18px 0; padding-bottom: 18px; border-bottom: 1px solid #eee; }}
    li a {{ font-size: 1.1rem; color: #0066cc; text-decoration: none; }}
    li a:hover {{ text-decoration: underline; }}
    .date {{ font-size: 0.85rem; color: #888; margin-top: 4px; }}
  </style>
</head>
<body>
  <div class="back"><a href="../">← Back to Rain</a></div>
  <h1>🌱 Garden of Thoughts</h1>
  <p>Personal reflections on data engineering, AI tools, and cloud practice.</p>
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


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body. Returns (meta, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    meta = yaml.safe_load(text[3:end])
    body = text[end + 3:].lstrip("\n")
    return meta or {}, body


def format_date(d) -> str:
    if isinstance(d, date):
        return d.strftime("%B %-d, %Y")
    return str(d)


def convert_file(md_path: Path) -> tuple[str, dict]:
    """Convert one .md file to .html. Returns (html_filename, meta)."""
    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    title = meta.get("title", md_path.stem).strip('"')
    date_str = format_date(meta.get("date", ""))
    tags = meta.get("tags", [])
    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)

    body_html = markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "nl2br"],
    )

    html = ARTICLE_TEMPLATE.format(
        title=title,
        date_str=date_str,
        tags_html=tags_html,
        body=body_html,
    )

    out_path = md_path.with_suffix(".html")
    if out_path.exists() and out_path.stat().st_mtime > md_path.stat().st_mtime:
        print(f"  skip  {out_path.name} (up to date)")
        return out_path.name, {"title": title, "date": meta.get("date"), "date_str": date_str}
    out_path.write_text(html, encoding="utf-8")
    print(f"  wrote {out_path.name}")
    return out_path.name, {"title": title, "date": meta.get("date"), "date_str": date_str}


def rebuild_index(articles: list[tuple[str, dict]]):
    """Rebuild index.html from the list of (filename, meta) pairs."""
    articles_sorted = sorted(articles, key=lambda x: x[1]["date"] or date.min, reverse=True)
    items = "\n".join(
        INDEX_ITEM.format(filename=fname, title=info["title"], date_str=info["date_str"])
        for fname, info in articles_sorted
    )
    index_html = INDEX_TEMPLATE.format(items=items)
    index_path = GARDEN_DIR / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"  rebuilt {index_path.name} with {len(articles)} entries")


def main():
    md_files = sorted(GARDEN_DIR.glob("*.md"))
    if not md_files:
        print("No markdown files found.")
        return

    print(f"Converting {len(md_files)} markdown files...")
    articles = [convert_file(f) for f in md_files]

    print("Rebuilding index.html...")
    rebuild_index(articles)

    print("Done.")


if __name__ == "__main__":
    main()
