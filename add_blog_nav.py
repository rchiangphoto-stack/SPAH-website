"""Add BLOG link to navigation on all main HTML pages."""
import os

BASE = r"C:\Users\rchia\Documents\SPAH-website"

# Pages to update (root-level only, blog pages already have it)
pages = [
    "index.html", "about.html", "services.html", "pricing.html", "contact.html",
    "vet-alhambra.html", "vet-south-pasadena.html", "vet-highland-park.html",
    "vet-san-gabriel.html", "vet-monterey-park.html", "vet-san-marino.html",
    "vet-rosemead.html", "vet-eagle-rock.html", "exotic-vet-pasadena.html",
]

for page in pages:
    filepath = os.path.join(BASE, page)
    if not os.path.exists(filepath):
        print(f"SKIP (not found): {page}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if BLOG link already exists
    if 'BLOG' in content:
        print(f"SKIP (already has BLOG): {page}")
        continue

    # Desktop nav: Add BLOG after PHARMACY link (or after CONTACT if no PHARMACY)
    # Pattern: find the PHARMACY link and add BLOG after it
    # Or find CONTACT link in the right-side nav and add BLOG after the pharmacy

    # Desktop nav - add BLOG link after the pharmacy link
    old_pharmacy = '           class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide font-bold transition-colors duration-200">PHARMACY ↗</a>'
    new_pharmacy = '           class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide font-bold transition-colors duration-200">PHARMACY ↗</a>\n        <a href="blog/index.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">BLOG</a>'

    if old_pharmacy in content:
        content = content.replace(old_pharmacy, new_pharmacy, 1)
    else:
        # Try alternate pattern - CONTACT link in right-side desktop nav
        # Add after the last link before </div> in right nav
        old_contact_desktop = '<a href="contact.html"   class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">CONTACT</a>'
        new_contact_desktop = '<a href="contact.html"   class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">CONTACT</a>\n        <a href="blog/index.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">BLOG</a>'
        if old_contact_desktop in content:
            content = content.replace(old_contact_desktop, new_contact_desktop, 1)

    # Mobile nav - add BLOG link after PHARMACY or CONTACT
    old_mobile_pharmacy = '<a href="https://spah.koala.health/" target="_blank" class="text-dark/70 font-body text-sm font-bold py-3">PHARMACY ↗</a>'
    new_mobile_pharmacy = '<a href="https://spah.koala.health/" target="_blank" class="text-dark/70 font-body text-sm font-bold py-3">PHARMACY ↗</a>\n      <a href="blog/index.html" class="text-dark/70 font-body text-sm tracking-wide py-3">BLOG</a>'

    if old_mobile_pharmacy in content:
        content = content.replace(old_mobile_pharmacy, new_mobile_pharmacy, 1)
    else:
        old_mobile_contact = '<a href="contact.html"  class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>'
        new_mobile_contact = '<a href="contact.html"  class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>\n      <a href="blog/index.html" class="text-dark/70 font-body text-sm tracking-wide py-3">BLOG</a>'
        if old_mobile_contact in content:
            content = content.replace(old_mobile_contact, new_mobile_contact, 1)
        else:
            # Try without extra spaces
            old_mc2 = '<a href="contact.html" class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>'
            new_mc2 = '<a href="contact.html" class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>\n      <a href="blog/index.html" class="text-dark/70 font-body text-sm tracking-wide py-3">BLOG</a>'
            content = content.replace(old_mc2, new_mc2, 1)

    # Footer - add Blog link to Quick Links
    old_footer_pharmacy = '<a href="https://spah.koala.health/" target="_blank" class="font-body text-terra font-bold text-sm hover:text-brand transition-colors duration-200">Online Pharmacy ↗</a>'
    new_footer_pharmacy = '<a href="https://spah.koala.health/" target="_blank" class="font-body text-terra font-bold text-sm hover:text-brand transition-colors duration-200">Online Pharmacy ↗</a>\n              <a href="blog/index.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Blog</a>'

    if old_footer_pharmacy in content:
        content = content.replace(old_footer_pharmacy, new_footer_pharmacy, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"UPDATED: {page}")

print("\nDone! Blog nav links added.")
