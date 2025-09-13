#!/usr/bin/env python3
# generate_sitemap.py
# Scans the repo for .html files and writes sitemap.xml at repo root.
# Usage:
#   DOMAIN="https://example.com" python .github/scripts/generate_sitemap.py
import os
import datetime
from pathlib import Path

DOMAIN = os.environ.get("DOMAIN", "https://d1sh1x.github.io/maminhleb").rstrip("/")
REPO_ROOT = Path(__file__).resolve().parents[2]  # go two levels up from .github/scripts/
IGNORE_DIRS = {".git", ".github", "node_modules", "vendor", "dist", "build", "__pycache__"}

def url_from_path(p: Path) -> str:
    rel = p.relative_to(REPO_ROOT).as_posix()
    # map index.html to directory or root
    if rel.endswith("/index.html"):
        rel = rel[:-len("index.html")]
    return f"{DOMAIN}/{rel}".replace("//", "/").replace(":/", "://")

def main():
    html_files = []
    for root, dirs, files in os.walk(REPO_ROOT):
        # prune ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for fn in files:
            if fn.endswith(".html"):
                html_files.append(Path(root) / fn)

    today = datetime.date.today().isoformat()
    urls = []
    for f in sorted(html_files):
        urls.append((url_from_path(f), today))

    # ensure at least homepage is present
    if not any(u[0].rstrip("/") == DOMAIN for u in urls):
        urls.insert(0, (DOMAIN + "/", today))

    # write sitemap.xml
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in urls:
        out.append("  <url>")
        out.append(f"    <loc>{loc}</loc>")
        out.append(f"    <lastmod>{lastmod}</lastmod>")
        out.append("    <priority>0.8</priority>")
        out.append("  </url>")
    out.append("</urlset>\n")
    (REPO_ROOT / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")
    print(f"Generated sitemap.xml with {len(urls)} URLs at {REPO_ROOT / 'sitemap.xml'}")

if __name__ == "__main__":
    main()
