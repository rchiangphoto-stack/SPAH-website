# SPAH Website — Claude Code Context

South Pasadena Animal Hospital website at **https://spah.la**
GitHub repo: `rchiangphoto-stack/SPAH-website` (static HTML, no build step)

---

## Business Info

| Field | Value |
|---|---|
| **Business** | South Pasadena Animal Hospital (SPAH) |
| **Website** | https://spah.la |
| **Instagram** | @southpasah |
| **Phone** | (626) 441-1314 |
| **Main location** | 3116 W Main St, Alhambra, CA 91801 |
| **Original location** | 1911 Fremont Ave, South Pasadena |
| **Booking link** | https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2 |
| **GA4** | G-0WEP9XT29L |
| **Ahrefs** | `data-key="ZIMxhr5nEAsxfE8H6JNaeQ"` |

**Staff:** Dr. Sylvia Chiang (co-founder), Dr. Gina Navia (co-founder, exotic animal care), Dr. Fannie Chiang (relief), Dr. Curtis Eng (relief), Dr. Ruby Jong (relief)

**Target audience:** Pet parents in South Pasadena, Alhambra, San Marino, Monterey Park, San Gabriel, Pasadena, and the greater SGV/LA area.

---

## Sitewide Rules (MANDATORY)

- **Never use:** specialize, specialty, expert, expertise — veterinary board restriction
- **No author byline** on any blog post
- **Banner on all pages:** `"Sorry, we are not accepting new clients at this time except exotics appointments."`
- **No walk-ins language** in meta descriptions or CTAs (appointment-only is fine)
- **Never invent** staff credentials, services, equipment, or certifications not listed on spah.la
- **Heading color spans** (h1/h2/h3 and inline references only):
  - `<span style="color:#7A9E8E">South Pasadena</span>`
  - `<span style="color:#5A7FA6">Alhambra</span>`

---

## Site Structure

All pages are static `.html` files at the repo root or in `blog/`.

**Key internal links to use in content:**
`/services`, `/pricing`, `/contact`, `/about`, `/vet-alhambra`, `/rabbit-vet-alhambra`, `/bird-vet-alhambra`, `/reptile-vet-alhambra`, `/cat-vet-alhambra`, `/exotic-vet-alhambra`

**Fonts:** Playfair Display (headings) + Lato (body) — loaded via Google Fonts
**Colors:** `#7A9E8E` (brand green/teal), `#5A7FA6` (brand blue), `#2A3442` (dark), `#FAF9F7` (warm bg)

---

## Blog Posts

**Current count as of 2026-06-04: Blog 76** — next post is Blog 77.

### Blog post HTML structure
Model after `blog/bearded-dragon-health-problems.html`. Key sections in order:
1. `<head>` — GA4, Ahrefs, meta, canonical, OG, Twitter cards, 3 JSON-LD schemas
2. `<nav>` — sticky top nav (same on every page)
3. New-client banner (amber/yellow)
4. Breadcrumb nav
5. `<article>` — category badge + date + H1 + header image + `<div class="prose">`
6. FAQ section (`.faq-item` divs with H3 + P)
7. CTA section (gradient, phone + book online)
8. `<footer>` — dark footer with Services / Learn columns

### Required JSON-LD schemas (all three, every post)
- `BlogPosting` — headline, description, datePublished, dateModified, image, author/publisher as Organization
- `BreadcrumbList` — Home → Blog → Post title
- `FAQPage` — mirrors the FAQ section

### Blog header images
Every post needs a 1200×630 WebP header image at `images/blog/{slug}-header.webp`.
A GitHub Actions workflow (`generate-blog-headers.yml`) auto-generates missing headers on push using the Pixabay API. Just add an HTML comment in the file:
```html
<!-- Photo: {description} — generate with scripts/auto_header.py using query "{search query}" -->
```
The image tag goes before `<div class="prose">`:
```html
<img src="../images/blog/{slug}-header.webp"
     alt="{geo-tagged description}"
     width="1200" height="630"
     style="width:100%;height:auto;border-radius:0.75rem;margin-bottom:2rem;"
     loading="eager" />
```

### Category badge colors
| Category | Background | Color |
|---|---|---|
| Reptile Care | `#E8F5E9` | `#2E7D32` |
| Small Animal Care | `#FFF3E0` | `#E65100` |
| Bird Care | `#E3F2FD` | `#1565C0` |
| Dog Health | `#FFF3E0` | `#E65100` |
| Cat Health | `#FCE4EC` | `#C62828` |
| General | `#F3E5F5` | `#6A1B9A` |

### Blog index (`blog/index.html`)
- Update the article count comment `CARD GRID (N articles)` when adding posts
- Add new cards at the **top** of `#cardGrid`
- Card format: `<a href="{slug}" class="mag-card" data-cat="exotic|dog|cat|general" data-date="YYYYMMDD" data-views="NNN">`

---

## City Landing Pages

Model after `vet-monterey-park.html` (14-section structure).

**Cities with pages:** Alhambra, South Pasadena, Pasadena, San Gabriel, San Marino, Monterey Park, Rosemead, Eagle Rock, Altadena, Temple City, El Monte, Highland Park, Arcadia, West Covina, Covina, Whittier, Glendale

**Cross-link pattern:** Each city page links to 4–5 nearby city pages.

**Footer dropdown** (`index.html` and all main pages): The "Areas We Serve" section uses `.footer-areas-col` / `.footer-areas-links` / `.is-open` CSS toggle. Add new city links inside `.footer-areas-links`.

---

## Sitemap (`sitemap.xml`)

Located at repo root. Add new entries before `</urlset>`:
```xml
<url>
  <loc>https://www.spah.la/{path}</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.8</priority>  <!-- 0.9 for main service pages, 0.8 for city/blog, 0.7 for older posts -->
</url>
```
Always update `sitemap.xml` and `blog/index.html` when adding new pages.

---

## Git Workflow

```bash
# Push to feature branch (PAT stored in your password manager / .env — never commit it)
git push -u https://{GITHUB_PAT}@github.com/rchiangphoto-stack/SPAH-website.git {branch-name}

# Create PR via GitHub API (MCP tools don't have write access for PRs)
curl -X POST \
  -H "Authorization: token {GITHUB_PAT}" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/rchiangphoto-stack/SPAH-website/pulls \
  -d '{"title":"...","head":"...","base":"master","body":"..."}'

# Merge PR
curl -X PUT \
  -H "Authorization: token {GITHUB_PAT}" \
  https://api.github.com/repos/rchiangphoto-stack/SPAH-website/pulls/{number}/merge \
  -d '{"merge_method":"merge"}'
```

**Branch naming:** `claude/{descriptor}` (e.g. `claude/spah-seo-improvements`)
**MCP GitHub tools** can read (PRs, files, issues) but cannot write PRs — use curl with the PAT above.

---

## SEO Notes

### Meta description rules
- 150–160 characters max — never truncate mid-sentence
- Include primary keyword + location signal
- No "walk-ins" language
- Write for click-through, not just keyword stuffing

### High-value pages to protect (high impressions from GSC)
| Page | Impressions | Notes |
|---|---|---|
| `blog/hamster-sick-signs` | ~57k | Inflated by AI research queries; real audience ~8k |
| `blog/turtle-tortoise-health` | ~33k | Position 4.5, CTR fixed May 2026 |
| `blog/rabbit-not-eating` | ~21k | CTR fixed May 2026 |
| `blog/corn-snake-care` | ~124k | Meta fixed June 2026 |

### Blog post voice guidelines
- Write like a clinician explaining to a worried client — not a textbook
- Use first-person plural: "We see this in our clinic..."
- Vary sentence length; mix short punchy sentences with longer ones
- Use specific numbers: "within 12–24 hours," "day 3–5"
- Avoid: "It is important to note that...", "In most cases it is recommended..."

---

## Pixabay API
Key stored in `.claude/settings.local.json` env as `PIXABAY_API_KEY`.
Used by `scripts/auto_header.py` to generate blog header images on CI.
