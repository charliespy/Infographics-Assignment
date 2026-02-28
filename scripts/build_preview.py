#!/usr/bin/env python3
"""
Build preview/index.html from Jekyll sources so you can preview without running Jekyll.
Run with --watch to rebuild whenever source files change.
"""
import re
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "_config.yml"
DEFAULT_LAYOUT = ROOT / "_layouts" / "default.html"
INDEX = ROOT / "index.html"
PREVIEW_DIR = ROOT / "preview"
PREVIEW_INDEX = PREVIEW_DIR / "index.html"
# For local preview, paths from /preview/ to repo root use ../
ASSET_PREFIX = "../"


def parse_config():
    """Parse _config.yml for title, description, navigation."""
    text = CONFIG.read_text(encoding="utf-8")
    data = {"title": "Infographics Assignment", "description": "", "navigation": []}
    # title: ...
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if m:
        data["title"] = m.group(1).strip().strip('"')
    # description: ...
    m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if m:
        data["description"] = m.group(1).strip().strip('"')
    # navigation: ... (list of - title: X / url: Y)
    nav_block = re.search(r"^navigation:\s*\n((?:\s+-\s+title:.*\n(?:\s+url:.*\n)*)*)", text, re.MULTILINE)
    if nav_block:
        for item in re.finditer(r"-\s+title:\s*(.+)\n\s+url:\s*(.+)", nav_block.group(1)):
            data["navigation"].append({"title": item.group(1).strip(), "url": item.group(2).strip()})
    return data


def strip_front_matter(content: str) -> str:
    """Remove Jekyll front matter (--- ... ---) and return the rest."""
    if content.strip().startswith("---"):
        parts = content.strip().split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return content


def relative_url(path: str) -> str:
    """For local preview: / -> ../preview/, /structure/ -> ../structure/."""
    path = path.rstrip("/") or "/"
    if path == "/":
        return "../preview/"
    return ".." + path + ("/" if not path.endswith("/") else "")


def build_preview():
    """Regenerate preview/index.html from layout + index + config."""
    config = parse_config()
    layout = DEFAULT_LAYOUT.read_text(encoding="utf-8")
    index_raw = INDEX.read_text(encoding="utf-8")
    content = strip_front_matter(index_raw)

    # Page context for home
    page = {"title": "Home", "url": "/"}
    year = time.strftime("%Y")

    # Replace {{ content }}
    layout = layout.replace("{{ content }}", content)

    # Resolve image paths for preview ({{ '/assets/images/...' | relative_url }} -> ../assets/images/...)
    layout = re.sub(
        r"\{\{\s*'/assets/images/([^']+)'\s*\|\s*relative_url\s*\}\}",
        ASSET_PREFIX + "assets/images/\\1",
        layout,
    )

    # Title tag
    layout = re.sub(
        r"\{% if page\.title %\}\{\{ page\.title \}\} \| \{% endif %\}\{\{ site\.title \}\}",
        f"{page['title']} | {config['title']}",
        layout,
    )
    layout = layout.replace("{{ site.title }}", config["title"])
    layout = layout.replace("{{ page.title }}", page["title"])

    # Description
    layout = re.sub(
        r'\{\{ page\.description \| default: site\.description \}\}',
        config["description"],
        layout,
    )

    # CSS and links
    layout = layout.replace("{{ '/assets/css/style.css' | relative_url }}", ASSET_PREFIX + "assets/css/style.css")
    layout = layout.replace("{{ '/' | relative_url }}", relative_url("/"))

    # Nav links: replace the whole <ul>...</ul> block
    nav_html = []
    for item in config["navigation"]:
        url = relative_url(item["url"])
        active = ' class="active"' if item["url"] == page["url"] else ""
        nav_html.append(f'<li><a href="{url}"{active}>{item["title"]}</a></li>')
    nav_block = "\n        ".join(nav_html)
    layout = re.sub(
        r'<ul class="nav-links">\s*\{% for item in site\.navigation %\}.*?\{% endfor %\}\s*</ul>',
        '<ul class="nav-links">\n        ' + nav_block + "\n      </ul>",
        layout,
        flags=re.DOTALL,
    )

    # Footer year
    layout = layout.replace("{{ 'now' | date: \"%Y\" }}", year)

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_INDEX.write_text(layout, encoding="utf-8")
    print("Preview built:", PREVIEW_INDEX)


def watch():
    """Watch source files and rebuild on change."""
    watched = [CONFIG, DEFAULT_LAYOUT, INDEX, ROOT / "assets" / "css" / "style.css"]
    last_mtimes = {f: os.path.getmtime(f) for f in watched if f.exists()}
    print("Watching for changes (Ctrl+C to stop)...")
    while True:
        try:
            time.sleep(0.5)
            changed = False
            for f in watched:
                if not f.exists():
                    continue
                m = os.path.getmtime(f)
                if m != last_mtimes.get(f):
                    last_mtimes[f] = m
                    changed = True
            if changed:
                build_preview()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    build_preview()
    if "--watch" in sys.argv or "-w" in sys.argv:
        watch()
