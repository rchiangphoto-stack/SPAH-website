"""Remove BLOG link from desktop nav and mobile menu, keep in footer only."""
import os, re

BASE = r"C:\Users\rchia\Documents\SPAH-website"

pages = [
    "index.html", "about.html", "services.html", "pricing.html", "contact.html",
    "vet-alhambra.html", "vet-south-pasadena.html", "vet-highland-park.html",
    "vet-san-gabriel.html", "vet-monterey-park.html", "vet-san-marino.html",
    "vet-rosemead.html", "vet-eagle-rock.html", "exotic-vet-pasadena.html",
]

for page in pages:
    filepath = os.path.join(BASE, page)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove desktop nav BLOG link (line with blog/index.html in nav area)
    content = content.replace(
        '\n        <a href="blog/index.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">BLOG</a>',
        ''
    )

    # Remove mobile menu BLOG link
    content = content.replace(
        '\n      <a href="blog/index.html" class="text-dark/70 font-body text-sm tracking-wide py-3">BLOG</a>',
        ''
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"UPDATED: {page}")

print("\nDone! Blog removed from nav/mobile, kept in footer.")
