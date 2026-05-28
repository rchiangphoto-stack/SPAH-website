"""
SPAH Blog Header Image Generator (Pixabay)
Usage: python3 make_blog_header.py <slug> "<Blog Title>" "<pixabay search query>"
Example: python3 make_blog_header.py hamster-health-problems "Hamster Health Problems" "hamster pet cute"

Requires PIXABAY_API_KEY env var or .env file:
  export PIXABAY_API_KEY=your_key_here
"""

import sys
import os
import urllib.request
import urllib.parse
import textwrap
import io
import json
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
OVERLAY_ALPHA = 130
SUBTITLE = "South Pasadena Animal Hospital  •  Alhambra, CA"

def _find_font(bold=True):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "C:/Windows/Fonts/georgiab.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "C:/Windows/Fonts/georgia.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images", "blog")
UA = "Mozilla/5.0 (compatible; SPAH-bot/1.0)"


def get_api_key():
    key = os.environ.get("PIXABAY_API_KEY", "")
    if not key:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("PIXABAY_API_KEY="):
                        key = line.strip().split("=", 1)[1].strip('"').strip("'")
    if not key:
        sys.exit("Error: PIXABAY_API_KEY not found. Set it with: export PIXABAY_API_KEY=your_key")
    return key


def search_pixabay(query, api_key, per_page=10):
    url = (
        "https://pixabay.com/api/?"
        + urllib.parse.urlencode({
            "key": api_key,
            "q": query,
            "image_type": "photo",
            "orientation": "horizontal",
            "per_page": per_page,
            "safesearch": "true",
            "min_width": 1200,
        })
    )
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    hits = data.get("hits", [])
    if not hits:
        sys.exit(f"No photos found for query: {query!r}")
    return hits


def make_header(out_path, photo_url, title, photo_id, photographer):
    font_bold = _find_font(bold=True)
    font_reg  = _find_font(bold=False)

    req = urllib.request.Request(photo_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
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

    os.makedirs(out_path.rsplit("/", 1)[0], exist_ok=True)
    img.save(out_path, "WEBP", quality=88)
    print(f"Saved: {out_path}")
    print(f"  Photo by {photographer} on Pixabay (ID: {photo_id})")
    print(f"  Attribution: <!-- Photo by {photographer} on Pixabay (ID: {photo_id}) -->")


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    slug   = sys.argv[1]
    title  = sys.argv[2]
    query  = sys.argv[3]
    api_key = get_api_key()

    print(f"Searching Pixabay for: {query!r}")
    hits = search_pixabay(query, api_key)

    for i, p in enumerate(hits[:5]):
        print(f"  [{i}] ID:{p['id']} by {p['user']} — {p['largeImageURL'][:80]}...")

    choice = input("Pick photo index [0]: ").strip()
    idx = int(choice) if choice.isdigit() else 0
    photo = hits[idx]

    out_path = f"{OUT_DIR}/{slug}-header.webp"
    make_header(out_path, photo["largeImageURL"], title, photo["id"], photo["user"])


if __name__ == "__main__":
    main()
