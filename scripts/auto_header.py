#!/usr/bin/env python3
"""
Auto-generate a blog header image for CI (non-interactive).
Usage: python3 auto_header.py <slug>

Reads title from blog/{slug}.html og:title.
Reads Pexels/Unsplash query from the HTML comment:
  <!-- Photo: ... using query "your search query here" -->
Requires UNSPLASH_ACCESS_KEY env var.
"""

import sys
import os
import re
import urllib.request
import urllib.parse
import json
import textwrap
import io
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OVERLAY_ALPHA = 130
SUBTITLE = "South Pasadena Animal Hospital  •  Alhambra, CA"
UA = "Mozilla/5.0 (compatible; SPAH-bot/1.0)"

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")


def _find_font(bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "C:/Windows/Fonts/georgiab.ttf" if bold else "C:/Windows/Fonts/georgia.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def get_api_key():
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        env_path = os.path.join(REPO_ROOT, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("UNSPLASH_ACCESS_KEY="):
                        key = line.strip().split("=", 1)[1].strip('"').strip("'")
    if not key:
        sys.exit("UNSPLASH_ACCESS_KEY not set")
    return key


def extract_from_html(slug):
    html_path = os.path.join(REPO_ROOT, "blog", f"{slug}.html")
    if not os.path.exists(html_path):
        sys.exit(f"HTML not found: {html_path}")
    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # og:title
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    title = m.group(1) if m else slug.replace("-", " ").title()

    # Query from comment: <!-- Photo: ... using query "..." -->
    m = re.search(r'using query "([^"]+)"', html)
    query = m.group(1) if m else slug.replace("-", " ")

    return title, query


def search_unsplash(query, api_key):
    url = (
        f"https://api.unsplash.com/search/photos"
        f"?query={urllib.parse.quote(query)}&per_page=10&orientation=landscape"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {api_key}",
        "Accept-Version": "v1",
        "User-Agent": UA,
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    results = data.get("results", [])
    if not results:
        sys.exit(f"No Unsplash results for: {query!r}")
    return results[0]


def make_header(out_path, photo_url, title, photo_id, photographer):
    font_bold = _find_font(bold=True)
    font_reg  = _find_font(bold=False)

    req = urllib.request.Request(photo_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        img = Image.open(io.BytesIO(r.read())).convert("RGB")

    img = img.resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, OVERLAY_ALPHA))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    for pt in (64, 56, 48, 42, 36):
        fnt = ImageFont.truetype(font_bold, pt) if font_bold else ImageFont.load_default()
        wrapped = textwrap.fill(title, width=28)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=fnt, align="center", spacing=12)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw <= W - 80 and th <= H // 2:
            break

    tx, ty = W / 2, H / 2 - th / 2 - 20
    draw.multiline_text((tx, ty), wrapped, font=fnt, fill=(255, 255, 255),
                        align="center", anchor="ma", spacing=12)
    fnt_sub = ImageFont.truetype(font_reg, 26) if font_reg else ImageFont.load_default()
    draw.text((tx, ty + th + 28), SUBTITLE, font=fnt_sub, fill=(230, 230, 230), anchor="ma")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "WEBP", quality=88)
    print(f"Saved: {out_path}")
    print(f"Photo by {photographer} on Unsplash (ID: {photo_id})")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    slug = sys.argv[1]
    api_key = get_api_key()
    title, query = extract_from_html(slug)

    print(f"Slug:  {slug}")
    print(f"Title: {title}")
    print(f"Query: {query}")

    photo = search_unsplash(query, api_key)
    photo_id     = photo["id"]
    photographer = photo["user"]["name"]
    photo_url    = photo["urls"]["full"]

    # Trigger download for Unsplash attribution tracking
    dl_url = photo.get("links", {}).get("download_location", "")
    if dl_url:
        try:
            req = urllib.request.Request(
                dl_url,
                headers={"Authorization": f"Client-ID {api_key}", "User-Agent": UA}
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    out_path = os.path.join(REPO_ROOT, "images", "blog", f"{slug}-header.webp")
    make_header(out_path, photo_url, title, photo_id, photographer)


if __name__ == "__main__":
    main()
