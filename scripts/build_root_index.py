"""Read README.md and regenerate the root index.html.

Usage:
  uv run python scripts/build_root_index.py

Changelog:
  2026-06-07  Initial version.
              - Reads title (first # heading) and description (first paragraph) from README.md.
              - Regenerates root index.html from ROOT_INDEX_TEMPLATE.
              - CSS and nav links live in the template — edit here, not in index.html directly.
  2026-06-07  Redesigned style inspired by StashCapital Leadership Program layout.
              - Light blue background (#dce8f5), large bold sans-serif heading.
              - Small all-caps brand line at top with SVG rain drop logo.
              - Clean minimal layout with no border decorations.
              - Added left margin (padding-left: 96px), vertical nav links,
                smaller one-liner h1, smaller rain drop SVG in slate blue (#5a8ab0).
  2026-06-07  Replaced inline SVG brand line with assets/logo.svg embedded inline.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
README  = ROOT_DIR / "README.md"
LOGO    = ROOT_DIR / "assets" / "logo.svg"
OUTPUT  = ROOT_DIR / "index.html"

ROOT_INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{title}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      height: 100%;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
      background-color: #dce8f5;
      color: #111;
      min-height: 100vh;
      padding: 48px 56px 48px 96px;
    }}
    .logo {{
      margin-bottom: 48px;
    }}
    .logo svg {{
      width: 90px;
      height: auto;
    }}
    h1 {{
      font-size: clamp(2rem, 4vw, 3.2rem);
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.02em;
      color: #111;
      max-width: 800px;
      white-space: nowrap;
      border-bottom: 2px solid #5a8ab0;
      padding-bottom: 16px;
      margin-bottom: 32px;
    }}
    .description {{
      font-size: 1.15rem;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin-bottom: 56px;
    }}
    .nav-links {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .nav-links a {{
      font-size: 1rem;
      font-weight: 500;
      color: #111;
      text-decoration: none;
      border-bottom: 2px solid #111;
      padding-bottom: 2px;
      letter-spacing: 0.01em;
      width: fit-content;
    }}
    .nav-links a:hover {{
      opacity: 0.6;
    }}
  </style>
</head>
<body>
  <div class="logo">{logo}</div>
  <h1>{title}</h1>
  <p class="description">{description}</p>
  <div class="nav-links">
    <a href="garden-of-thoughts/">Garden of Thoughts</a>
    <a href="https://github.com/SherryAnalytics/Rain" target="_blank">GitHub Repo</a>
  </div>
</body>
</html>"""


def parse_readme(path: Path) -> tuple[str, str]:
    """Extract title (first # heading) and description (first non-empty paragraph) from README.md."""
    lines = path.read_text(encoding="utf-8").splitlines()
    title = ""
    description = ""
    for line in lines:
        if not title and line.startswith("# "):
            title = line[2:].strip()
        elif title and not description and line.strip():
            description = line.strip()
    return title, description


def main():
    title, description = parse_readme(README)
    logo = LOGO.read_text(encoding="utf-8")
    print(f"  title: {title}")
    print(f"  description: {description[:60]}...")

    html = ROOT_INDEX_TEMPLATE.format(title=title, description=description, logo=logo)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"  wrote {OUTPUT.name}")


if __name__ == "__main__":
    main()
