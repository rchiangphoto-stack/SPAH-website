"""
SPAH Blog Header Image Generator (Unsplash)
Usage: python3 make_blog_header.py <slug> "<Blog Title>" "<unsplash search query>"
Example: python3 make_blog_header.py hamster-health-problems "Hamster Health Problems" "hamster pet cute"

Requires UNSPLASH_ACCESS_KEY env var or .env file:
  export UNSPLASH_ACCESS_KEY=your_key_here
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

# Linux paths (DejaVu); Windows fallback to Georgia
def _find_font(bold=True):
    candidates = (
        ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "C:/Windows/Fonts/georgiab.ttf",
         "C:/Windows/Fonts/georgia.ttf"]
        if bold else
        ["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
         "C:/Windows/Fonts/georgia.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            return p
    return None  # PIL will fall back to default bitmap font

FONT_BOLD = _find_font(bold=True)
FONT_REG  = _find_font(bold=False)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images", "blog")
UA = "Mozilla/5.0 (compatible; SPAH-bot/1.0)"


def get_api_key():
    key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not key:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("UNSPLASH_ACCESS_KEY="):
                        key = line.strip().split("=", 1)[1].strip('"').strip("'")
    if not key:
        sys.exit("Error: UNSPLASH_ACCESS_KEY not found. Set it with: export UNSPLASH_ACCESS_KEY=your_key")
    return key


def search_unsplash(query, api_key, per_page=10):
    url = (
        f"https://api.unsplash.com/search/photos"
        f"?query={urllib.parse.quote(query)}"
        f"&per_page={per_page}&orientation=landscape"
    )
    req = urllib.request.Request(url, headers={
        "Authorization": f"Client-ID {api_key}",
        "User-Agent": UA,
        "Accept-Version": "v1",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read())
    photos = data.get("results", [])
    if not photos:
        sys.exit(f"No photos found for query: {query!r}")
    return photos


def make_header(out_path, photo_url, title, photo_id, photographer):
    req = urllib.request.Request(photo_url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        img = Image.open(io.BytesIO(r.read())).convert("RGB")

    img = img.resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, OVERLAY_ALPHA))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Fit title text
    for pt in (64, 56, 48, 42, 36):
        fnt = ImageFont.truetype(FONT_BOLD, pt) if FONT_BOLD else ImageFont.load_default()
        wrapped = textwrap.fill(title, width=28)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=fnt, align="center", spacing=12)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if tw <= W - 80 and th <= H // 2:
            break

    tx, ty = W / 2, H / 2 - th / 2 - 20
    draw.multiline_text((tx, ty), wrapped, font=fnt, fill=(255, 255, 255),
                        align="center", anchor="ma", spacing=12)

    fnt_sub = ImageFont.truetype(FONT_REG, 26) if FONT_REG else ImageFont.load_default()
    draw.text((tx, ty + th + 28), SUBTITLE, font=fnt_sub, fill=(230, 230, 230), anchor="ma")

    os.makedirs(out_path.rsplit("/", 1)[0], exist_ok=True)
    img.save(out_path, "WEBP", quality=88)
    print(f"Saved: {out_path}")
    print(f"  Photo by {photographer} on Unsplash (ID: {photo_id})")
    print(f"  Attribution: <!-- Photo by {photographer} on Unsplash (ID: {photo_id}) -->")


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    slug   = sys.argv[1]
    title  = sys.argv[2]
    query  = sys.argv[3]
    api_key = get_api_key()

    print(f"Searching Unsplash for: {query!r}")
    photos = search_unsplash(query, api_key)

    for i, p in enumerate(photos[:5]):
        print(f"  [{i}] ID:{p['id']} by {p['user']['name']} — {p['urls']['regular'][:80]}...")

    choice = input("Pick photo index [0]: ").strip()
    idx = int(choice) if choice.isdigit() else 0
    photo = photos[idx]
    photo_url    = photo["urls"]["full"]
    photo_id     = photo["id"]
    photographer = photo["user"]["name"]

    # Unsplash requires a download trigger for attribution tracking
    dl_url = photo.get("links", {}).get("download_location", "")
    if dl_url:
        try:
            req = urllib.request.Request(
                dl_url, headers={"Authorization": f"Client-ID {api_key}", "User-Agent": UA}
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    out_path = os.path.join(OUT_DIR, f"{slug}-header.webp")
    make_header(out_path, photo_url, title, photo_id, photographer)


if __name__ == "__main__":
    main()
