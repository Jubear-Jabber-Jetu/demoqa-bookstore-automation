"""Build a GitHub Pages site with the latest HTML report and screenshots."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

SITE_DIR = Path("site")
REPORT_SRC = Path("reports/report.html")
SCREENSHOTS_SRC = Path("screenshots")
SCREENSHOTS_DST = SITE_DIR / "screenshots"


def _screenshot_cards() -> str:
    if not SCREENSHOTS_DST.exists():
        return "<p>No screenshots available.</p>"

    images = sorted(SCREENSHOTS_DST.glob("*.png"))
    if not images:
        return "<p>No screenshots available.</p>"

    cards = []
    for image in images:
        cards.append(
            f"""
            <a class="card" href="screenshots/{image.name}" target="_blank" rel="noopener">
              <img src="screenshots/{image.name}" alt="{image.stem}" loading="lazy" />
              <span>{image.stem}</span>
            </a>
            """
        )
    return "\n".join(cards)


def build_site() -> None:
    SITE_DIR.mkdir(exist_ok=True)

    if REPORT_SRC.exists():
        shutil.copy2(REPORT_SRC, SITE_DIR / "report.html")
    else:
        (SITE_DIR / "report.html").write_text(
            "<html><body><h1>Report not generated</h1></body></html>",
            encoding="utf-8",
        )

    if SCREENSHOTS_DST.exists():
        shutil.rmtree(SCREENSHOTS_DST)
    if SCREENSHOTS_SRC.exists():
        shutil.copytree(
            SCREENSHOTS_SRC,
            SCREENSHOTS_DST,
            ignore=shutil.ignore_patterns(".gitkeep"),
        )

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DemoQA Book Store — Test Results</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --panel: #111827;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #38bdf8;
      --border: #1f2937;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, Segoe UI, Arial, sans-serif;
      background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
      color: var(--text);
      min-height: 100vh;
    }}
    .wrap {{ max-width: 1100px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ margin: 0 0 8px; font-size: 2rem; }}
    .meta {{ color: var(--muted); margin-bottom: 28px; }}
    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 36px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 18px;
      border-radius: 10px;
      background: var(--accent);
      color: #082f49;
      text-decoration: none;
      font-weight: 700;
    }}
    .btn.secondary {{
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }}
    h2 {{ margin: 0 0 16px; font-size: 1.25rem; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 16px;
    }}
    .card {{
      display: block;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      color: inherit;
      text-decoration: none;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: var(--accent);
    }}
    .card img {{
      width: 100%;
      height: 160px;
      object-fit: cover;
      object-position: top;
      display: block;
      background: #000;
    }}
    .card span {{
      display: block;
      padding: 12px 14px;
      font-size: 0.92rem;
      color: var(--muted);
      word-break: break-word;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>DemoQA Book Store — Test Results</h1>
    <p class="meta">Last updated after CI run: {generated_at}</p>

    <div class="actions">
      <a class="btn" href="report.html">Download / View HTML Report</a>
      <a class="btn secondary" href="https://github.com/Jubear-Jabber-Jetu/demoqa-bookstore-automation/actions" target="_blank" rel="noopener">GitHub Actions Runs</a>
    </div>

    <h2 id="screenshots">Screenshots</h2>
    <div class="grid">
      {_screenshot_cards()}
    </div>
  </div>
</body>
</html>
"""
    (SITE_DIR / "index.html").write_text(index_html, encoding="utf-8")


if __name__ == "__main__":
    build_site()
