#!/usr/bin/env python3
"""
Export the infographic page to PDF.
Builds preview if needed, then uses a headless browser to print to PDF.
Requires: pip install playwright && playwright install chromium
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREVIEW_INDEX = ROOT / "preview" / "index.html"
OUTPUT_PDF = ROOT / "infographic.pdf"


def main():
    # Ensure preview exists
    if not PREVIEW_INDEX.exists():
        print("Preview not found. Running build_preview...")
        import subprocess
        subprocess.run([sys.executable, ROOT / "scripts" / "build_preview.py"], check=True, cwd=ROOT)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is required. Install with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)

    # file:// URL so relative paths (../assets/...) resolve from preview/index.html
    file_url = PREVIEW_INDEX.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        # Use print media so we get print CSS (no header/footer)
        page.emulate_media(media="print")
        # Measure full content height so we can export as one long page
        content_height_px = page.evaluate(
            "() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"
        )
        # 96 CSS pixels per inch; add margin (20mm top + 20mm bottom ≈ 1.57in)
        margin_in = 40 / 25.4
        height_in = (content_height_px / 96) + margin_in
        width_in = 210 / 25.4  # A4 width
        page.pdf(
            path=str(OUTPUT_PDF),
            width=f"{width_in}in",
            height=f"{height_in}in",
            print_background=True,
            margin={"top": "20mm", "right": "20mm", "bottom": "20mm", "left": "20mm"},
        )
        browser.close()

    print("Exported:", OUTPUT_PDF)


if __name__ == "__main__":
    main()
