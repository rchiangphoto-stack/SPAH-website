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
- **Banner on all pages:** `"Currently in temporary Bungalows during construction."` — soft pink style (`background:#FDDDE6;border:1px solid #F8B9CE;color:#9D4060;`) (updated 2026-06-12 — SPAH operating from temporary bungalows during construction)
- **No walk-ins language** in meta descriptions or CTAs (appointment-only is fine)
- **Never invent** staff credentials, services, equipment, or certifications not listed on spah.la
- **No urgent care or emergency language** anywhere on the site — SPAH is a general practice that focuses on regular/routine cases. Urgent and emergency cases are referred out. Never use: "urgent care," "emergency care," "emergency vet," "same-day emergency," "urgent visits," or any variation in meta descriptions, title tags, hero copy, or CTAs. If a page must address emergencies (e.g. GI stasis blog), frame it as "contact a vet immediately" or "seek emergency care" — pointing away, not implying SPAH provides it.
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

### Blog header images (auto-generated — don't create manually)
Every post needs a 1200×630 WebP header image at `images/blog/{slug}-header.webp`. **You do not need to generate it yourself** — just reference it and add the photo comment; CI handles the rest.

**How the pipeline works (`.github/workflows/generate-blog-headers.yml`):**
1. Triggers on push to **any branch** (`branches: ['**']`) when `blog/*.html` changes, or manually via `workflow_dispatch` (default branch input: `claude/busy-goldberg-GY46m`)
2. Scans every `blog/*.html` for an `<img src="...{slug}-header.webp">` reference and checks whether that file already exists in `images/blog/`
3. For each missing image, runs `python3 scripts/auto_header.py {slug}`, which:
   - Reads the post's `og:title` for the headline text
   - Reads the search query from the HTML comment (`using query "{search query}"`)
   - Searches Pixabay (`PIXABAY_API_KEY` from repo secrets), downloads the top horizontal photo ≥1200px wide
   - Composites a dark overlay + bold title + `"South Pasadena Animal Hospital • Alhambra, CA"` subtitle, saves as 1200×630 WebP
4. Commits generated images back to the same branch as `Auto-generate blog header images [skip ci]` and pushes

**What you need to do when adding a post:** add the placeholder comment with a good search query, then push — the workflow fills in the actual file within a minute or two:
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
To run it locally instead (e.g. to preview before pushing): `PIXABAY_API_KEY=... python3 scripts/auto_header.py {slug}` — requires Pillow (`pip install Pillow`).

### Category badge colors
| Category | Background | Color |
|---|---|---|
| Reptile Care | `#E8F5E9` | `#2E7D32` |
| Small Animal Care | `#FFF3E0` | `#E65100` |
| Bird Care | `#E3F2FD` | `#1565C0` |
| Dog Health | `#FFF3E0` | `#E65100` |
| Cat Health | `#FCE4EC` | `#C62828` |
| General | `#F3E5F5` | `#6A1B9A` |

### AI Detection — Required Before Publishing

Every blog post **must pass Sapling AI detection before being pushed to master**.

**Passing threshold: under 25%**

Run the check after writing the post:
```bash
python3 scripts/check_ai_detection.py --file blog/{slug}.html
```

| Score | Class | Action |
|---|---|---|
| < 25% | ✅ Ready to publish |
| 25–49% | ❌ Rewrite — too structured, needs more voice |
| 50%+ | ❌ Major rewrite required |

**If it fails (40%+), rewrite using these techniques:**
- Replace list-heavy explanations with a short narrative paragraph first
- Add a first-person plural opener: "We see this in our clinic..." or "One thing Pasadena dog owners often ask us..."
- Break up any 3+ sentence runs of pure facts with a specific clinical observation
- Name a specific location, species behavior, or patient scenario instead of speaking generically
- Cut any sentence that starts with "It is important to..." or "Pet owners should be aware..."

**Reference scores from existing posts:**
- `vet-visit-cost-alhambra`: 11.2% ✅ — conversational, opinionated, uses "we" voice throughout
- `do-rabbits-need-vet-visits`: 49.9% — Sapling doc-level unreliable for clinical content; only 5/44 sentences flag. Use sentence score as real signal.
- `dog-vaccines-california`: 20.0% ✅ — rewritten with opinionated clinical narrative, removed bullet lists

The `.sapling_key` file is stored at `scripts/.sapling_key` (gitignored). If the key is missing, add it with:
```bash
python3 scripts/check_ai_detection.py --save-key YOUR_KEY_HERE
```

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

### Deployment (Vercel + Cloudflare) — Fully Automated

Pushing to `master` automatically:
1. Triggers a Vercel build
2. Promotes it to Production via the `promote-and-purge.yml` GitHub Actions workflow
3. Purges the Cloudflare cache

**No manual steps required.** Changes are live within ~1–2 minutes of pushing.

If the workflow fails (check Actions tab), the most likely cause is an expired `VERCEL_TOKEN` secret — regenerate it in Vercel account settings and update the repo secret at GitHub → Settings → Secrets.

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

### Blog post voice guidelines — MANDATORY STANDARD

Every post must read like a specific veterinarian talking to a specific worried client — not a reference article, not a care guide, not a listicle. A human reader should finish the post thinking "that was clearly written by someone who actually treats these animals" not "that's a summary of what the internet says."

**The test:** Could this sentence appear on any vet blog in the country? If yes, it's not good enough. It needs to be grounded in something specific — a patient scenario, a local reference, a clinical observation, an opinion.

#### MUST DO

- **Open every major section with a clinical observation or opinion**, not a definition.
  - ✅ "Ask us what we find most often and we'll say dental pain almost every time."
  - ❌ "Dental disease is a condition that affects the teeth and gums."
- **Use first-person plural throughout.** "We see this," "we find," "in our clinic," "one thing we've noticed," "we tell clients."
- **Take a position.** The vet-cost post scored 11% because it argued something. Every post should argue something or explain why we think about a topic a certain way.
- **Reference specific places, breeds, or scenarios.** "Dogs at Eaton Canyon," "cats in Pasadena craftsman homes," "the Shih Tzu who came in last month." Specificity is the antidote to AI slop.
- **Vary sentence length deliberately.** Short sentences after long ones. Fragments are fine. "That's pain, not tiredness." 
- **End sections with a push to call us** — not a generic "consult your vet" but "call us" or "this is when you call."
- **Use specific timeframes.** "Within 4–6 hours," "by day 3," "after two missed meals." Vague = AI.

#### MUST NOT DO

- **Never open a section with a definition.** "X is a condition that..." — that's a Wikipedia article, not a vet.
- **Never use h2 headers as a clinical checklist.** Headers like "Symptoms," "Causes," "Treatment," "When to See a Vet" in sequence is the most recognizable AI content pattern. Instead use opinionated headers: "The thing owners miss most," "Why we go to the mouth first," "When to call today, not tomorrow."
- **Never write three facts in a row without a "we" anchor.** Facts need clinical grounding. "Rabbits hide illness. We see this constantly. By the time they're visibly sick, the problem has usually been building for weeks."
- **Never use:** "It is important to note," "Pet owners should be aware," "In most cases it is recommended," "Comprehensive care," "It's worth noting," "One of the most common," "There are several reasons."
- **Never write consecutive sentences of equal length.** That cadence is an AI fingerprint.
- **Never cover everything.** A post that tries to cover every angle of a topic sounds like it was generated to be thorough. A real vet picks the three things that actually matter and talks about those.

#### REFERENCE POSTS (pass/fail examples)
- `vet-visit-cost-alhambra`: 11.2% ✅ — argues a position, opinionated editorial voice
- `corporate-vs-independent-vet-sgv`: 2.0% ✅ — personal, takes a side
- `dog-ear-cytology`: 1.3% ✅ — clinical and specific
- `dog-not-eating`: 76.1% ⚠️ — Sapling doc model unreliable; 9% sentence-level OK
- `cat-vomiting`: 99.8% ❌ — reads as a reference article, needs full rewrite
- `hedgehog-care`: 99.9% ❌ — structured care guide, no clinical voice

#### REWRITE PRIORITY ORDER — **RE-VERIFIED 2026-07-22: NOTHING NEEDS REWRITING**

The old priority list here was stale and sent work in the wrong direction. Every post
re-checked on 2026-07-22 **passes** on the reliable metric (sentence-level under 25%):

| Post | GSC impr | doc-level | sentence-level | |
|---|---|---|---|---|
| hamster-sick-signs | 16,684 | 26.0% | 7/64 = 10.9% | pass |
| rabbit-not-eating | 7,255 | 45.0% | 7/57 = 12.3% | pass (was listed 48.5%) |
| bearded-dragon-shedding | 6,244 | 43.3% | 4/54 = 7.4% | pass |
| turtle-tortoise-health | 5,586 | 2.0% | 8/58 = 13.8% | pass |
| sick-bird-signs | 4,928 | 58.8% | 5/45 = 11.1% | pass |
| corn-snake-care | 4,301 | 50.4% | 2/57 = 3.5% | pass (was listed 81.1%) |
| dog-eye-problems | 207 | 57.4% | 6/53 = 11.3% | pass (was listed 99.8%) |
| cat-vomiting | 174 | 50.0% | 4/51 = 7.8% | pass (was listed 99.8%) |
| hedgehog-care | 100 | 99.9% | 7/61 = 11.5% | pass (was listed 99.9%) |
| pet-coughing-sneezing | 21 | 100.0% | 3/64 = 4.7% | pass (was listed 100.0%) |

**The doc-level score is NOT trustworthy — it is nondeterministic.** Verified directly:
identical text returned **90.3% then 68.2%** on back-to-back API calls. Posts showing
99.9%/100% doc-level flag only 3-7 sentences out of 60+. **Only use the sentence-level
percentage.**

**Also check traffic before rewriting.** The posts previously ranked highest-priority
have almost no traffic — cat-vomiting is 174 impressions at position 29, and
pet-coughing-sneezing is 21 impressions. Rewriting those changes nothing. Sort any
future rewrite list by GSC impressions first, then sentence-level score.

### Medical & legal liability guardrails (MANDATORY for all blog content)
- **Never assert a diagnosis** for the reader's pet — frame symptoms as "could be a sign of," "may indicate," "one possible cause," not "your pet has X"
- **Never give specific drug names, dosages, or treatment protocols** to follow at home — defer to "your veterinarian will determine the right treatment/dosage"
- **No absolute/guarantee language**: avoid "cures," "guaranteed," "always works," "100% safe/effective," "completely eliminates," "prevents [disease]" — use "can help reduce the risk of," "may improve," "is often effective"
- **No DIY medical procedures** (e.g., "lance the abscess," "pull the retained shed yourself," "give your pet X medication") — home care should be limited to comfort/support measures (quiet space, hydration, monitoring), with anything invasive or medication-related routed to "have a vet do this"
- Every post covering a health problem must include a clear "when to see a vet" section that pushes readers toward calling SPAH rather than relying on home treatment
- Don't make comparative/superiority claims about SPAH vs. other named clinics or vets
- Don't cite statistics, survival rates, or success rates without a verifiable source — if unsure, omit the number and use qualitative language instead

---

## Pixabay API
Key stored in `.claude/settings.local.json` env as `PIXABAY_API_KEY`.
Used by `scripts/auto_header.py` to generate blog header images on CI.
