"""Generate 5 Alhambra-focused SEO blog posts for SPAH website (posts 6-10)."""
import os, re

BLOG_DIR = r"C:\Users\rchia\Documents\SPAH-website\blog"

# ─── Reuse the shared template parts from generate_blogs.py ──────────

HEAD_START = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="../images/spah-logo.png" />"""

def og_meta(title, desc, url):
    return f"""  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:site_name" content="South Pasadena Animal Hospital" />
  <meta property="og:image" content="https://www.spah.la/images/spah-logo.png" />"""

def blog_schema(headline, desc, url, date="2026-04-01"):
    return f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BlogPosting","headline":"{headline}","description":"{desc}","datePublished":"{date}","dateModified":"{date}","author":{{"@type":"Organization","name":"South Pasadena Animal Hospital","url":"https://www.spah.la"}},"publisher":{{"@type":"Organization","name":"South Pasadena Animal Hospital","url":"https://www.spah.la","logo":{{"@type":"ImageObject","url":"https://www.spah.la/images/spah-logo.png"}}}},"mainEntityOfPage":"{url}"}}
  </script>"""

def breadcrumb_schema(name):
    return f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.spah.la/"}},{{"@type":"ListItem","position":2,"name":"Blog","item":"https://www.spah.la/blog/"}},{{"@type":"ListItem","position":3,"name":"{name}"}}]}}
  </script>"""

STYLES_AND_FONTS = """  <link rel="stylesheet" href="../css/styles.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    html { scroll-behavior: smooth; }
    body { font-family: 'Lato', sans-serif; background: #FAFAF8; color: #2A3442; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }
    .card-shadow { box-shadow: 0 2px 4px rgba(90,127,166,0.06), 0 8px 24px rgba(90,127,166,0.10); }
    .btn-primary { background: #5A7FA6; color: white; border-radius: 9999px; padding: 0.75rem 2rem; font-family: 'Lato', sans-serif; font-weight: 700; letter-spacing: 0.04em; transition: background 0.2s, transform 0.2s; box-shadow: 0 4px 14px rgba(90,127,166,0.30); }
    .btn-primary:hover { background: #4A6D92; transform: scale(1.03); }
    .nav-link { position: relative; }
    .nav-link::after { content: ''; position: absolute; left: 0; bottom: -4px; width: 100%; height: 2px; background: #5A7FA6; border-radius: 1px; transform: scaleX(0); transition: transform 0.25s ease; }
    .nav-link:hover::after { transform: scaleX(1); }
    .prose h2 { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #2A3442; margin-top: 2.5rem; margin-bottom: 1rem; }
    .prose h3 { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #2A3442; margin-top: 1.8rem; margin-bottom: 0.75rem; }
    .prose p { font-family: 'Lato', sans-serif; color: #555; font-size: 1.05rem; line-height: 1.8; margin-bottom: 1.25rem; }
    .prose ul { list-style: disc; padding-left: 1.5rem; margin-bottom: 1.25rem; }
    .prose li { font-family: 'Lato', sans-serif; color: #555; font-size: 1.05rem; line-height: 1.8; margin-bottom: 0.5rem; }
    .prose a { color: #5A7FA6; text-decoration: underline; }
    .prose a:hover { color: #4A6D92; }
    .prose strong { color: #2A3442; }
    .blog-card { background: white; border-radius: 1rem; overflow: hidden; transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .blog-card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(90,127,166,0.15); }
    .tag { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }
    .tag-reptile { background: #E8F5E9; color: #2E7D32; }
    .tag-small-mammal { background: #FFF3E0; color: #E65100; }
    .tag-rabbit { background: #F3E5F5; color: #7B1FA2; }
    .tag-bird { background: #E3F2FD; color: #1565C0; }
    .tag-exotic { background: #FCE4EC; color: #C62828; }
    .tag-local { background: #E0F2F1; color: #00695C; }
    .tag-all-pets { background: #FFF8E1; color: #F57F17; }
  </style>"""

NAV = """  <div class="text-center py-2 px-4 text-sm font-body font-bold tracking-wide" style="background: #FDDDE6; color: #2A3442;">
    Sorry, we are not accepting new clients at this time except <strong>exotics appointments</strong>. &nbsp;<a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank" class="underline hover:no-underline" style="color:#5A7FA6;">Book now&nbsp;&rarr;</a>
  </div>
  <nav class="sticky top-0 z-50 bg-warm/95 backdrop-blur-sm border-b border-sky/20" style="box-shadow: 0 2px 12px rgba(90,127,166,0.08);">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-center gap-10 relative">
      <div class="hidden md:flex items-center gap-8">
        <a href="../index.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">HOME</a>
        <a href="../about.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">ABOUT US</a>
        <a href="../services.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">SERVICES</a>
      </div>
      <a href="../index.html"><img src="../images/spah-logo-new.png" alt="South Pasadena Animal Hospital logo" class="h-[70px]" /></a>
      <div class="hidden md:flex items-center gap-8">
        <a href="../pricing.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">PRICING</a>
        <a href="../contact.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">CONTACT</a>
        <a href="https://spah.koala.health/" target="_blank" class="nav-link text-terra font-body text-sm tracking-wide font-bold">PHARMACY &nearr;</a>
      </div>
      <button id="menuBtn" class="md:hidden absolute right-6 text-dark focus-visible:outline-none" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
    <div id="mobileMenu" class="hidden md:hidden px-6 pb-4 flex-col gap-4 bg-warm border-t border-sky/20">
      <a href="../index.html" class="text-dark/70 font-body text-sm tracking-wide py-3">HOME</a>
      <a href="../about.html" class="text-dark/70 font-body text-sm tracking-wide py-3">ABOUT US</a>
      <a href="../services.html" class="text-dark/70 font-body text-sm tracking-wide py-3">SERVICES</a>
      <a href="../pricing.html" class="text-dark/70 font-body text-sm tracking-wide py-3">PRICING</a>
      <a href="../contact.html" class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>
      <a href="https://spah.koala.health/" target="_blank" class="text-terra font-body text-sm font-bold py-3">PHARMACY &nearr;</a>
    </div>
  </nav>"""

FOOTER = """  <footer class="bg-sky/15 pt-12 pb-[84px] md:pb-6">
    <div class="max-w-6xl mx-auto px-6">
      <div class="pb-8 mb-8 border-b border-dark/10">
        <div class="mb-8">
          <img src="../images/spah-logo-new-lg.png" alt="South Pasadena Animal Hospital logo" class="h-[77px] mb-4" />
          <p class="font-body text-dark text-sm leading-relaxed max-w-lg" style="line-height:1.7;">Compassionate, comprehensive care for pets of all shapes and sizes. Proudly serving Alhambra, South Pasadena, San Marino, Highland Park, Altadena, and greater Los Angeles.</p>
        </div>
        <div class="grid grid-cols-2 gap-6 max-w-lg">
          <div>
            <h4 class="font-body font-bold tracking-widest text-xs uppercase text-dark/80 mb-4">Quick Links</h4>
            <div class="flex flex-col gap-2">
              <a href="../index.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Home</a>
              <a href="../about.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">About Us</a>
              <a href="../services.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Services</a>
              <a href="../contact.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Contact</a>
              <a href="https://spah.koala.health/" target="_blank" class="font-body text-terra font-bold text-sm hover:text-brand transition-colors duration-200">Online Pharmacy &nearr;</a>
            </div>
          </div>
          <div>
            <h4 class="font-body font-bold tracking-widest text-xs uppercase text-dark/80 mb-4">Contact</h4>
            <div class="flex flex-col gap-2">
              <p class="font-body text-dark text-sm">3116 W Main St<br />Alhambra, CA 91801</p>
              <a href="tel:6264411314" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">(626) 441-1314</a>
              <a href="mailto:info@spah.la" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">info@spah.la</a>
              <div class="flex gap-3 mt-1">
                <a href="https://www.instagram.com/southpasah" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="text-dark/60 hover:text-brand transition-colors duration-200"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></a>
                <a href="https://www.tiktok.com/@southpasah" target="_blank" rel="noopener noreferrer" aria-label="TikTok" class="text-dark/60 hover:text-brand transition-colors duration-200"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 0 0-.79-.05A6.34 6.34 0 0 0 3.15 15a6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.34-6.34V8.75a8.18 8.18 0 0 0 4.76 1.52V6.84a4.83 4.83 0 0 1-1-.15z"/></svg></a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col md:flex-row justify-between items-center gap-3">
        <p class="font-body text-dark/60 text-xs">&copy; 2026 South Pasadena Animal Hospital. Est. 2023.</p>
        <div class="flex gap-4">
          <a href="../blog/" class="font-body text-dark/60 text-xs hover:text-dark transition-colors duration-200">Blog</a>
          <a href="../contact.html" class="font-body text-dark/60 text-xs hover:text-dark transition-colors duration-200">Privacy Policy</a>
        </div>
      </div>
    </div>
  </footer>
  <script>
    document.getElementById('menuBtn').addEventListener('click', () => {
      const menu = document.getElementById('mobileMenu');
      menu.classList.toggle('hidden');
      menu.classList.toggle('flex');
    });
  </script>
</body>
</html>"""

def related_card(href, gradient, emoji, tag_class, tag_text, title):
    return f"""        <a href="{href}" class="blog-card card-shadow block">
          <div style="background:linear-gradient(135deg,{gradient});padding:2rem;text-align:center;"><span style="font-size:2.5rem;">{emoji}</span></div>
          <div class="p-5">
            <span class="tag {tag_class}">{tag_text}</span>
            <h3 class="font-display text-lg font-bold text-dark mt-2 mb-1">{title}</h3>
            <p class="font-body text-brand text-sm font-bold mt-2">Read more &rarr;</p>
          </div>
        </a>"""

def cta_section(text):
    return f"""  <section class="py-16 text-center" style="background:linear-gradient(135deg,#5A7FA6 0%,#7A9E8E 100%);">
    <div class="max-w-2xl mx-auto px-6 text-white">
      <h2 class="font-display text-3xl font-bold mb-4">{text}</h2>
      <p class="font-body text-white/80 mb-8" style="line-height:1.7;">Schedule your pet's appointment online in under a minute, or give us a call.</p>
      <div class="flex flex-wrap gap-4 justify-center">
        <a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank" class="bg-white text-brand font-body font-bold rounded-full px-8 py-3 hover:bg-warm transition-colors duration-200">Book Online</a>
        <a href="tel:6264411314" class="border-2 border-white/50 text-white font-body font-bold rounded-full px-8 py-3 hover:bg-white/10 transition-colors duration-200">(626) 441-1314</a>
      </div>
    </div>
  </section>"""


# ─── Blog Post Definitions ───────────────────────────────────────────

blogs = [
    # ── BLOG 6: Exotic Vet Visit Cost ──
    {
        "file": "exotic-vet-visit-cost-alhambra.html",
        "title": "How Much Does an Exotic Vet Visit Cost in Alhambra?",
        "meta_desc": "Wondering how much an exotic vet visit costs in Alhambra? SPAH breaks down exam fees, diagnostic costs, and common procedures for reptiles, birds, rabbits, and guinea pigs.",
        "keywords": "exotic vet cost Alhambra, how much does exotic vet cost, reptile vet cost, bird vet cost, rabbit vet cost, exotic pet vet prices, vet prices Alhambra, affordable exotic vet near me",
        "og_desc": "Transparent pricing breakdown for exotic pet vet visits in Alhambra. Learn what to expect for reptile, bird, rabbit, and guinea pig exams at SPAH.",
        "schema_headline": "How Much Does an Exotic Vet Visit Cost in Alhambra?",
        "schema_desc": "A transparent guide to exotic pet veterinary costs in Alhambra, CA, covering exam fees, diagnostics, and common procedures.",
        "breadcrumb_name": "Exotic Vet Visit Cost in Alhambra",
        "tag_class": "tag-exotic",
        "tag_text": "EXOTIC PETS",
        "date_text": "April 1, 2026 &middot; 6 min read",
        "h1": "How Much Does an Exotic Vet Visit Cost in Alhambra?",
        "content": """
        <p>One of the most common questions we hear from exotic pet owners in Alhambra and the San Gabriel Valley is: <strong>"How much is this going to cost?"</strong> It's a fair question — and one we believe you deserve a straight answer to before you walk through the door.</p>

        <p>At South Pasadena Animal Hospital on Main Street in Alhambra, we publish our <a href="../pricing.html">prices online</a> because we think transparency builds trust. Here's what exotic pet owners in Alhambra can expect to pay.</p>

        <h2>Exotic Pet Wellness Exam Fees</h2>
        <p>The foundation of every vet visit is the physical exam. During a wellness exam, your veterinarian will perform a thorough head-to-tail assessment, check your pet's weight, listen to their heart and lungs, examine their eyes, skin, and teeth, and review their diet and husbandry.</p>
        <p>Our wellness exam fees are the same regardless of species — whether you're bringing in a bearded dragon, a cockatiel, a rabbit, or a guinea pig. You can find the exact fee on our <a href="../pricing.html">pricing page</a>. Many corporate veterinary chains in the Alhambra area charge significantly more for exotic animals than for dogs and cats, but at SPAH, we believe every pet deserves affordable care.</p>

        <h2>Common Diagnostic Costs</h2>
        <p>Not every visit requires diagnostics, but when your vet recommends testing, here's what to expect:</p>
        <ul>
          <li><strong>Bloodwork:</strong> Blood panels help us assess organ function, check for infections, and screen for metabolic issues. This is especially important for reptiles with suspected metabolic bone disease and birds showing signs of liver problems.</li>
          <li><strong>Fecal testing:</strong> A fecal exam screens for parasites like coccidia, pinworms, and other organisms. Recommended annually for most exotic pets, and essential for newly adopted reptiles.</li>
          <li><strong>X-rays (radiographs):</strong> Digital X-rays help us evaluate bones, organs, and detect issues like egg binding in birds, bladder stones in guinea pigs, or respiratory infections in snakes.</li>
        </ul>
        <p>We always discuss diagnostic costs <em>before</em> running any tests, so you can make an informed decision. There are never surprise charges at our Alhambra clinic.</p>

        <h2>Common Procedure Costs by Species</h2>

        <h3>Reptiles</h3>
        <p>Common reptile procedures in Alhambra include treatment for metabolic bone disease (MBD), parasite treatment, abscess drainage, and husbandry consultations. Many reptile health issues are related to incorrect lighting, heating, or diet — and a husbandry review is included with every wellness exam at no extra charge.</p>

        <h3>Birds</h3>
        <p>Avian visits often include wing trims, nail trims, beak trims, and treatment for respiratory infections or feather-plucking. Grooming services like nail and wing trims are affordable and can be done during a wellness exam or as a standalone visit.</p>

        <h3>Rabbits</h3>
        <p>Rabbit care commonly involves wellness exams, <a href="rabbit-gi-stasis.html">GI stasis treatment</a>, dental checks, RHDV2 vaccination, and spay/neuter surgery. Spaying female rabbits is particularly important since unspayed does have up to an 80% chance of developing uterine cancer by age five.</p>

        <h3>Guinea Pigs</h3>
        <p>Guinea pig visits typically cover <a href="guinea-pig-sneezing.html">respiratory infection treatment</a>, dental checks, bladder stone evaluation, and skin/parasite care. Vitamin C deficiency screening is included with every guinea pig wellness exam.</p>

        <h2>Why Exotic Vet Visits Often Cost More Than Dog or Cat Visits</h2>
        <p>You may notice that exotic pet care can sometimes cost more than a standard dog or cat visit at other clinics. There are a few reasons:</p>
        <ul>
          <li><strong>Fewer vets see exotics:</strong> Exotic animal medicine requires additional training and experience. The limited number of vets who treat reptiles, birds, and small mammals means the demand is high in areas like Alhambra, Pasadena, and the greater San Gabriel Valley.</li>
          <li><strong>Different diagnostic approaches:</strong> Exotic pets often require species-specific blood panels, specialized handling, and different reference ranges for lab results than dogs and cats.</li>
          <li><strong>Smaller patients, more precision:</strong> Working with a 40-gram parakeet or a 300-gram guinea pig requires specialized equipment and careful technique.</li>
        </ul>
        <p>At SPAH, we keep our prices fair because we believe exotic pet owners in Alhambra shouldn't have to drive across Los Angeles or pay a premium just because their pet isn't a dog or cat.</p>

        <h2>How to Keep Exotic Vet Costs Manageable</h2>
        <ul>
          <li><strong>Schedule annual wellness exams:</strong> Prevention is always cheaper than treatment. Catching a problem early — before it becomes a crisis — can save hundreds of dollars and, more importantly, save your pet's life.</li>
          <li><strong>Get the husbandry right:</strong> Many exotic pet health problems stem from incorrect enclosure setup, diet, or lighting. A single husbandry consultation can prevent expensive vet visits down the road.</li>
          <li><strong>Don't wait when something seems off:</strong> Exotic pets hide illness. By the time symptoms are obvious, treatment is often more complex and costly. Early visits are simpler and less expensive.</li>
          <li><strong>Ask about payment options:</strong> We want to make care accessible. Ask our front desk about payment plans and options when you visit our Alhambra clinic.</li>
        </ul>

        <h2>Visit SPAH in Alhambra for Transparent Exotic Pet Care</h2>
        <p>We're located at <strong>3116 W Main St, Alhambra, CA 91801</strong>, and we welcome exotic pets of all kinds — reptiles, birds, rabbits, guinea pigs, hamsters, and more. Check our <a href="../pricing.html">full pricing page</a> for current fees, or call <a href="tel:6264411314">(626) 441-1314</a> to ask about your specific pet's needs. We're happy to give you a cost estimate before your visit so there are no surprises.</p>
""",
        "related_cards": [
            related_card("exotic-pet-first-vet-visit.html", "#FCE4EC 0%,#F8BBD0 100%", "🐾", "tag-exotic", "ALL EXOTICS", "What to Expect at Your Exotic Pet's First Vet Visit"),
            related_card("signs-bearded-dragon-needs-vet.html", "#E8F5E9 0%,#C8E6C9 100%", "🦎", "tag-reptile", "REPTILE", "Signs Your Bearded Dragon Needs to See a Vet"),
        ],
        "cta_text": "Ready to Book an Affordable Exotic Pet Exam?",
    },

    # ── BLOG 7: Finding an Exotic Vet in SGV ──
    {
        "file": "exotic-vet-san-gabriel-valley.html",
        "title": "Finding an Exotic Vet in the San Gabriel Valley",
        "meta_desc": "Struggling to find an exotic vet in the San Gabriel Valley? Learn what to look for, what questions to ask, and why SPAH in Alhambra is a top choice for reptile, bird, and small mammal care.",
        "keywords": "exotic vet San Gabriel Valley, exotic vet near me, exotic vet Alhambra, exotic vet Pasadena, reptile vet SGV, bird vet San Gabriel Valley, rabbit vet near me, exotic animal vet Los Angeles",
        "og_desc": "A guide to finding a qualified exotic vet in the San Gabriel Valley. What to look for, questions to ask, and where to go in Alhambra for reptile, bird, and small mammal care.",
        "schema_headline": "Finding an Exotic Vet in the San Gabriel Valley",
        "schema_desc": "How to find a qualified exotic pet veterinarian in the San Gabriel Valley, including what to look for and questions to ask.",
        "breadcrumb_name": "Exotic Vet in the San Gabriel Valley",
        "tag_class": "tag-local",
        "tag_text": "LOCAL GUIDE",
        "date_text": "April 1, 2026 &middot; 7 min read",
        "h1": "Finding an Exotic Vet in the San Gabriel Valley",
        "content": """
        <p>If you own a reptile, bird, rabbit, guinea pig, or other exotic pet in the San Gabriel Valley, you've probably discovered something frustrating: <strong>most vet clinics don't see exotic animals.</strong> The majority of veterinary practices in Alhambra, Pasadena, San Gabriel, Monterey Park, and the surrounding area are set up exclusively for dogs and cats.</p>

        <p>This guide will help you find a qualified exotic vet in the San Gabriel Valley and explain what to look for so your pet gets the care it deserves.</p>

        <h2>Why Can't I Just Take My Exotic Pet to Any Vet?</h2>
        <p>Exotic animal medicine is fundamentally different from dog and cat medicine. A few examples:</p>
        <ul>
          <li><strong>Reptiles</strong> are ectothermic (cold-blooded) and their health is directly tied to their environment — temperature, humidity, and UV lighting. A vet who doesn't understand reptile husbandry may miss the root cause of most reptile illnesses.</li>
          <li><strong>Birds</strong> have a unique respiratory system with air sacs, hollow bones, and an extremely fast metabolism. They require gentle handling techniques and species-specific diagnostics like crop washes and fecal gram stains.</li>
          <li><strong>Rabbits</strong> have a sensitive GI tract that can shut down within hours (<a href="rabbit-gi-stasis.html">GI stasis</a>), and certain antibiotics that are safe for dogs are <em>fatal</em> to rabbits.</li>
          <li><strong>Guinea pigs</strong> cannot produce their own vitamin C (like humans), and they too are sensitive to specific antibiotics that can kill them by destroying beneficial gut bacteria.</li>
        </ul>
        <p>A vet without exotic animal experience may not know these critical differences, which can lead to misdiagnosis, wrong medications, or delayed treatment.</p>

        <h2>What to Look for in an Exotic Vet</h2>
        <p>Here are the key qualities to evaluate when searching for an exotic vet in the San Gabriel Valley:</p>

        <h3>1. Regular Exotic Caseload</h3>
        <p>Ask: "How often do you see [your species]?" A vet who sees reptiles, birds, or rabbits weekly is very different from one who sees them once a month. Frequency builds hands-on experience that no amount of textbook reading can replace.</p>

        <h3>2. In-House Diagnostics</h3>
        <p>Exotic pets can decline rapidly once symptoms appear. A clinic with in-house bloodwork, X-rays, and fecal testing can diagnose and start treatment the same day, rather than sending samples to an outside lab and waiting days for results.</p>

        <h3>3. Species-Specific Knowledge</h3>
        <p>Does the vet review your pet's husbandry (enclosure, diet, lighting, temperature)? A good exotic vet knows that most health problems in captive exotic pets are husbandry-related. If they don't ask about your setup, that's a red flag.</p>

        <h3>4. Transparent Pricing</h3>
        <p>Exotic vet visits can vary widely in cost. Look for a clinic that publishes prices or provides estimates upfront. Surprise bills at checkout are a sign of poor communication, not quality care.</p>

        <h3>5. Comfortable Handling</h3>
        <p>Watch how the vet and staff handle your pet. Are they confident? Gentle? Rushing? A vet who is visibly uncomfortable holding your bearded dragon or cockatiel may not have enough experience with that species.</p>

        <h2>Questions to Ask Before Your First Visit</h2>
        <ul>
          <li>"Do you regularly treat [my specific species]?"</li>
          <li>"Do you have in-house lab equipment for exotic bloodwork and X-rays?"</li>
          <li>"Will you review my pet's diet and enclosure setup?"</li>
          <li>"Can you provide a cost estimate before running any diagnostics?"</li>
          <li>"What are your emergency protocols for exotic pets?"</li>
        </ul>

        <h2>Exotic Vet Options in the San Gabriel Valley</h2>
        <p>The San Gabriel Valley spans a large area — from Pasadena and South Pasadena in the north, through Alhambra, San Gabriel, and Monterey Park in the center, to Rosemead, Temple City, and Arcadia further east. Despite this large population, there are very few veterinary clinics in the SGV that regularly treat exotic animals.</p>

        <p>Many exotic pet owners in the area end up driving to West Los Angeles, Orange County, or the Inland Empire to find a qualified vet. But there is a closer option.</p>

        <h2>SPAH in Alhambra: Exotic Pet Care in the Heart of the SGV</h2>
        <p>South Pasadena Animal Hospital is located at <strong>3116 W Main St, Alhambra, CA 91801</strong> — centrally positioned in the San Gabriel Valley and easily accessible from Pasadena, San Gabriel, Monterey Park, Rosemead, Arcadia, Highland Park, and beyond.</p>

        <p>Our veterinarians regularly treat:</p>
        <ul>
          <li><strong>Reptiles:</strong> <a href="../reptile-vet-alhambra.html">bearded dragons, geckos, snakes, turtles, tortoises, chameleons</a></li>
          <li><strong>Birds:</strong> <a href="../bird-vet-alhambra.html">parrots, cockatiels, conures, parakeets, finches</a></li>
          <li><strong>Rabbits:</strong> <a href="../rabbit-vet-alhambra.html">wellness, GI stasis, RHDV2, dental, spay/neuter</a></li>
          <li><strong>Guinea pigs:</strong> <a href="../guinea-pig-vet-alhambra.html">URIs, dental, bladder stones, vitamin C</a></li>
          <li><strong>Hamsters, rats, and other small mammals</strong></li>
        </ul>

        <p>We perform all diagnostics in-house — bloodwork, fecal tests, and digital X-rays — so we can get answers and start treatment the same day. Our <a href="../pricing.html">pricing is published online</a>, and we always discuss costs before proceeding with any tests or treatments.</p>

        <p>If you've been searching for a reliable exotic vet in the San Gabriel Valley, <a href="../contact.html">contact us</a> or call <a href="tel:6264411314">(626) 441-1314</a> to book your pet's appointment.</p>
""",
        "related_cards": [
            related_card("exotic-pet-first-vet-visit.html", "#FCE4EC 0%,#F8BBD0 100%", "🐾", "tag-exotic", "ALL EXOTICS", "What to Expect at Your Exotic Pet's First Vet Visit"),
            related_card("exotic-vet-visit-cost-alhambra.html", "#FFF3E0 0%,#FFE0B2 100%", "💰", "tag-exotic", "EXOTIC PETS", "How Much Does an Exotic Vet Visit Cost in Alhambra?"),
        ],
        "cta_text": "Found Your Exotic Vet — Ready to Book?",
    },

    # ── BLOG 8: Why Alhambra Pet Owners Choose Non-Corporate ──
    {
        "file": "non-corporate-vet-alhambra.html",
        "title": "Why Alhambra Pet Owners Are Choosing a Non-Corporate Vet",
        "meta_desc": "More Alhambra pet owners are choosing privately-owned vet clinics over corporate chains. Here's why the personal touch matters for your pet's care — and your wallet.",
        "keywords": "non-corporate vet Alhambra, private vet Alhambra, independent vet clinic Alhambra, privately owned animal hospital, vet vs corporate vet, best vet Alhambra, affordable vet Alhambra, personal vet care Alhambra",
        "og_desc": "Why Alhambra pet owners prefer a privately-owned vet over corporate chains. Personalized care, transparent pricing, and no corporate upselling.",
        "schema_headline": "Why Alhambra Pet Owners Are Choosing a Non-Corporate Vet",
        "schema_desc": "The advantages of choosing a privately-owned veterinary clinic in Alhambra over a corporate chain, from personalized care to transparent pricing.",
        "breadcrumb_name": "Non-Corporate Vet in Alhambra",
        "tag_class": "tag-local",
        "tag_text": "LOCAL GUIDE",
        "date_text": "April 1, 2026 &middot; 5 min read",
        "h1": "Why Alhambra Pet Owners Are Choosing a Non-Corporate Vet",
        "content": """
        <p>Over the past decade, corporate veterinary groups have been buying up independent vet clinics across Los Angeles and the San Gabriel Valley at a rapid pace. In Alhambra and surrounding cities, many of the clinics you've known for years are now owned by large corporations — even if they still operate under their original name.</p>

        <p>At South Pasadena Animal Hospital, we're proudly privately owned and always will be. Here's why that matters to the pet families we serve in Alhambra.</p>

        <h2>You See the Same Vet Every Time</h2>
        <p>At corporate clinics, veterinarians rotate frequently. You might see a different vet every visit, which means re-explaining your pet's history each time. At a privately-owned practice like SPAH, led by Dr. Sylvia Chiang and Dr. Gina Navia, our vets build long-term relationships with both you and your pet. They know your pet's history, personality, and health patterns by heart.</p>

        <h2>No Pressure to Upsell</h2>
        <p>Corporate veterinary groups often have revenue targets and standardized protocols that encourage upselling — running tests or recommending treatments that may not be medically necessary. At SPAH, our vets make recommendations based on what your pet actually needs, not what a corporate office expects them to sell. If a test isn't necessary, we'll tell you.</p>

        <h2>Transparent, Published Pricing</h2>
        <p>Many pet owners in Alhambra have experienced sticker shock at corporate clinics where prices aren't discussed upfront. At SPAH, our <a href="../pricing.html">prices are published online</a> for anyone to see. We believe you have the right to know what something costs before you agree to it — not after the procedure is done.</p>

        <h2>Decisions Made in the Exam Room, Not a Boardroom</h2>
        <p>When a veterinary clinic is owned by a corporation, many decisions about pricing, protocols, staffing, and even which products to carry are made by people who have never met you or your pet. At a private practice, the veterinarian who treats your pet is also the person who runs the clinic. That means decisions are made with your pet's best interest in mind, not shareholder returns.</p>

        <h2>We Treat Every Species</h2>
        <p>Most corporate clinics in the Alhambra area focus exclusively on dogs and cats because that's where the volume is. They have little incentive to invest in exotic animal training or equipment. As a privately-owned clinic, we choose to welcome <a href="../exotic-vet-alhambra.html">reptiles, birds, rabbits, guinea pigs, hamsters</a>, and other exotic pets because we genuinely care about all animals — not just the ones that generate the most revenue.</p>

        <h2>Deep Roots in the Community</h2>
        <p>South Pasadena Animal Hospital has been caring for pets and families since 2023, first in South Pasadena and now at our new location at <strong>3116 W Main St in Alhambra</strong>. We're part of this community. Our team shops at the same stores, eats at the same restaurants on Main Street, and cares about the same neighborhoods you do. When you choose a non-corporate vet, you're supporting a local business that reinvests in the community rather than sending profits to a distant corporate headquarters.</p>

        <h2>How to Tell If Your Vet Is Corporate-Owned</h2>
        <p>It's not always obvious. Many corporate-owned clinics keep their original name and branding after being acquired. Here are signs to watch for:</p>
        <ul>
          <li>Frequent vet turnover — you see a different doctor every visit</li>
          <li>Aggressive upselling or "wellness plan" subscriptions</li>
          <li>Prices that aren't shared until after procedures</li>
          <li>Corporate branding on receipts or paperwork (look for names like VCA, Banfield, BluePearl, NVA, or Thrive)</li>
          <li>Standardized, one-size-fits-all treatment recommendations</li>
        </ul>

        <h2>Visit Alhambra's Privately-Owned Animal Hospital</h2>
        <p>If you're looking for a vet in Alhambra that puts your pet first — not corporate profits — we'd love to meet you and your companion. Visit us at <strong>3116 W Main St, Alhambra, CA 91801</strong>, or call <a href="tel:6264411314">(626) 441-1314</a> to schedule an appointment. You can also <a href="../about.html">learn more about our team</a> and our approach to veterinary care.</p>
""",
        "related_cards": [
            related_card("exotic-vet-visit-cost-alhambra.html", "#FFF3E0 0%,#FFE0B2 100%", "💰", "tag-exotic", "EXOTIC PETS", "How Much Does an Exotic Vet Visit Cost in Alhambra?"),
            related_card("exotic-pet-first-vet-visit.html", "#FCE4EC 0%,#F8BBD0 100%", "🐾", "tag-exotic", "ALL EXOTICS", "What to Expect at Your Exotic Pet's First Vet Visit"),
        ],
        "cta_text": "Ready to Try a Non-Corporate Vet?",
    },

    # ── BLOG 9: Bearded Dragon Care Guide SoCal ──
    {
        "file": "bearded-dragon-care-guide-socal.html",
        "title": "The Complete Guide to Bearded Dragon Care in Southern California",
        "meta_desc": "Everything you need to know about keeping a bearded dragon healthy in Southern California — enclosure setup, diet, UVB lighting, common health issues, and when to see a vet in Alhambra.",
        "keywords": "bearded dragon care guide, bearded dragon care Southern California, bearded dragon enclosure setup, bearded dragon diet, bearded dragon UVB lighting, bearded dragon vet Alhambra, bearded dragon health, how to care for bearded dragon",
        "og_desc": "The complete bearded dragon care guide for Southern California owners. Enclosure setup, diet, UVB lighting, and when to visit a reptile vet in Alhambra.",
        "schema_headline": "The Complete Guide to Bearded Dragon Care in Southern California",
        "schema_desc": "A comprehensive care guide for bearded dragon owners in Southern California, covering enclosure setup, diet, UVB lighting, common health issues, and veterinary care.",
        "breadcrumb_name": "Bearded Dragon Care Guide",
        "tag_class": "tag-reptile",
        "tag_text": "REPTILE",
        "date_text": "April 1, 2026 &middot; 10 min read",
        "h1": "The Complete Guide to Bearded Dragon Care in Southern California",
        "content": """
        <p>Bearded dragons are one of the most popular pet reptiles in Southern California — and for good reason. They're docile, interactive, and relatively easy to care for compared to many other reptile species. But "relatively easy" doesn't mean "no effort required." Proper husbandry is essential, and getting it wrong is the number one reason we see bearded dragons at our <a href="../reptile-vet-alhambra.html">Alhambra reptile vet clinic</a>.</p>

        <p>This comprehensive guide covers everything a Southern California bearded dragon owner needs to know, from enclosure setup to diet to recognizing when your beardie needs a vet.</p>

        <h2>Enclosure Setup</h2>

        <h3>Tank Size</h3>
        <p>Adult bearded dragons need a minimum of a <strong>75-gallon tank</strong> (36" x 18" x 18"), though a 120-gallon (48" x 24" x 24") is ideal. Baby bearded dragons can start in a 40-gallon, but they grow quickly and will need an upgrade within 6-12 months. Front-opening enclosures are less stressful than top-opening ones since bearded dragons perceive overhead movement as a predator threat.</p>

        <h3>Temperature Gradient</h3>
        <p>Bearded dragons are ectothermic and need a temperature gradient to thermoregulate:</p>
        <ul>
          <li><strong>Basking spot:</strong> 100-110°F (38-43°C)</li>
          <li><strong>Warm side:</strong> 90-95°F (32-35°C)</li>
          <li><strong>Cool side:</strong> 75-85°F (24-29°C)</li>
          <li><strong>Nighttime:</strong> No lower than 65°F (18°C)</li>
        </ul>
        <p><strong>SoCal tip:</strong> During hot summer months in Alhambra and the San Gabriel Valley, ambient room temperatures can exceed 90°F. If your beardie's cool side gets too warm, they can't thermoregulate properly. Consider placing the enclosure in an air-conditioned room during heat waves.</p>

        <h3>UVB Lighting — The Most Important Factor</h3>
        <p>UVB lighting is non-negotiable. Without it, bearded dragons cannot metabolize calcium, leading to <strong>metabolic bone disease (MBD)</strong> — the most common and preventable health issue we treat at our clinic.</p>
        <ul>
          <li>Use a <strong>T5 HO 10.0 UVB tube</strong> (not a coil bulb — those don't provide adequate coverage)</li>
          <li>The tube should span <strong>2/3 to 3/4 of the enclosure length</strong></li>
          <li>Mount it <strong>inside the enclosure</strong> or within 6-8 inches of the basking spot if on top of a mesh screen (mesh blocks ~30% of UVB)</li>
          <li><strong>Replace UVB bulbs every 6 months</strong> — they stop producing adequate UVB before they burn out visually</li>
        </ul>
        <p><strong>SoCal tip:</strong> Southern California's sunny climate may tempt you to use natural sunlight instead of UVB bulbs. While supervised outdoor time is beneficial, glass and screens filter out UVB, so a window doesn't count. UVB bulbs are still essential even in sunny Alhambra.</p>

        <h2>Diet</h2>

        <h3>Baby Bearded Dragons (0-4 months)</h3>
        <p>80% protein (appropriately-sized crickets, dubia roaches) and 20% vegetables. Feed insects 2-3 times per day — as many as they'll eat in 10-15 minutes.</p>

        <h3>Juvenile Bearded Dragons (4-18 months)</h3>
        <p>Shift gradually to 60% protein, 40% vegetables. Feed insects once daily with a fresh salad available at all times.</p>

        <h3>Adult Bearded Dragons (18+ months)</h3>
        <p>Flip the ratio: <strong>80% vegetables, 20% protein</strong>. Adults only need insects 2-3 times per week. Daily salads should include:</p>
        <ul>
          <li><strong>Staple greens:</strong> collard greens, mustard greens, turnip greens, butternut squash</li>
          <li><strong>Occasional treats:</strong> bell peppers, blueberries, mango (small amounts)</li>
          <li><strong>Avoid:</strong> iceberg lettuce (no nutrition), spinach (binds calcium), avocado (toxic), citrus fruits</li>
        </ul>

        <h3>Supplements</h3>
        <ul>
          <li><strong>Calcium without D3:</strong> Dust insects at every feeding</li>
          <li><strong>Calcium with D3:</strong> 2-3 times per week</li>
          <li><strong>Multivitamin:</strong> Once per week</li>
        </ul>

        <h2>Common Health Issues in Southern California</h2>

        <h3>Metabolic Bone Disease (MBD)</h3>
        <p>The #1 health issue in pet bearded dragons. Caused by insufficient UVB, inadequate calcium supplementation, or both. Signs include trembling, rubbery jaw, swollen limbs, inability to stand, and lethargy. <a href="signs-bearded-dragon-needs-vet.html">Learn more about warning signs</a>. MBD is treatable if caught early but can cause permanent damage if ignored.</p>

        <h3>Parasites</h3>
        <p>Both internal parasites (coccidia, pinworms) and external parasites (mites) are common, especially in newly purchased bearded dragons from pet stores. We recommend a fecal test at every annual wellness exam.</p>

        <h3>Respiratory Infections</h3>
        <p>Caused by incorrect temperatures, excessive humidity, or poor ventilation. Signs include open-mouth breathing, mucus around the nose or mouth, and wheezing. Requires veterinary treatment with appropriate antibiotics.</p>

        <h3>Dehydration</h3>
        <p>Southern California's dry climate can contribute to dehydration. Offer water through a shallow dish (some beardies drink from dishes, many don't), regular misting, and hydrating vegetables. Soaking your beardie in lukewarm water 2-3 times per week for 15-20 minutes helps with hydration and shedding.</p>

        <h2>When to See a Vet</h2>
        <p>We recommend an <strong>annual wellness exam</strong> for all bearded dragons, even if they seem healthy. During the exam, we'll check weight, body condition, mouth, eyes, skin, and vent. We'll also review your entire husbandry setup and recommend any adjustments.</p>

        <p>See a vet <strong>immediately</strong> if your bearded dragon shows any of these signs:</p>
        <ul>
          <li>Not eating for more than 1-2 weeks (outside of brumation)</li>
          <li>Significant weight loss</li>
          <li>Swollen or rubbery limbs</li>
          <li>Black beard that won't go away</li>
          <li>Open-mouth breathing or mucus discharge</li>
          <li>Lethargy or inability to hold its body up</li>
          <li>Any lumps, bumps, or swelling</li>
        </ul>

        <p>South Pasadena Animal Hospital is located at <strong>3116 W Main St, Alhambra, CA 91801</strong>. We provide comprehensive <a href="../reptile-vet-alhambra.html">reptile veterinary care</a> including wellness exams, bloodwork, fecal testing, X-rays, and husbandry consultations. Call <a href="tel:6264411314">(626) 441-1314</a> to schedule your bearded dragon's appointment.</p>
""",
        "related_cards": [
            related_card("signs-bearded-dragon-needs-vet.html", "#E8F5E9 0%,#C8E6C9 100%", "🦎", "tag-reptile", "REPTILE", "Signs Your Bearded Dragon Needs to See a Vet"),
            related_card("exotic-pet-first-vet-visit.html", "#FCE4EC 0%,#F8BBD0 100%", "🐾", "tag-exotic", "ALL EXOTICS", "What to Expect at Your Exotic Pet's First Vet Visit"),
        ],
        "cta_text": "Book a Reptile Wellness Exam in Alhambra",
    },

    # ── BLOG 10: Foods Toxic to Pet Birds ──
    {
        "file": "foods-toxic-to-pet-birds.html",
        "title": "5 Foods That Are Toxic to Pet Birds (and What to Feed Instead)",
        "meta_desc": "Some common household foods are deadly to pet birds. Learn which 5 foods to never feed your parrot, cockatiel, or parakeet — and healthy alternatives from a bird vet in Alhambra.",
        "keywords": "foods toxic to birds, toxic food for parrots, what can birds eat, parrot diet, cockatiel diet, bird safe foods, avocado toxic to birds, chocolate toxic to birds, bird vet Alhambra, what to feed pet bird",
        "og_desc": "5 common foods that are toxic to pet birds plus safe alternatives. Essential reading for parrot, cockatiel, and parakeet owners from a bird vet in Alhambra.",
        "schema_headline": "5 Foods That Are Toxic to Pet Birds (and What to Feed Instead)",
        "schema_desc": "A veterinary guide to the most dangerous foods for pet birds, including avocado, chocolate, caffeine, and safe alternatives.",
        "breadcrumb_name": "Foods Toxic to Pet Birds",
        "tag_class": "tag-bird",
        "tag_text": "BIRD",
        "date_text": "April 1, 2026 &middot; 6 min read",
        "h1": "5 Foods That Are Toxic to Pet Birds (and What to Feed Instead)",
        "content": """
        <p>Birds are curious creatures, and many pet bird owners in Alhambra and the San Gabriel Valley enjoy sharing snacks with their feathered companions. While sharing fresh fruits and vegetables can be a healthy part of your bird's diet, there are several common household foods that are <strong>extremely dangerous — even fatal — to birds</strong>.</p>

        <p>Here are the five most important foods to keep away from your parrot, cockatiel, conure, parakeet, or any pet bird.</p>

        <h2>1. Avocado — Deadly to Birds</h2>
        <p>This is the number one food that every bird owner must know about. <strong>All parts of the avocado — fruit, pit, skin, and leaves — contain persin</strong>, a fungicidal toxin that causes severe cardiac distress in birds. Even a small amount can cause difficulty breathing, fluid accumulation around the heart, and death within 12-24 hours.</p>
        <p>There is no antidote for avocado poisoning in birds. If your bird has consumed any avocado, contact a vet immediately.</p>
        <p><strong>Feed instead:</strong> Mango, papaya, or banana — tropical fruits that are safe and most birds love.</p>

        <h2>2. Chocolate</h2>
        <p>Chocolate contains theobromine and caffeine, both of which are toxic to birds. Even a small nibble of chocolate can cause vomiting, diarrhea, increased heart rate, hyperactivity, tremors, seizures, and death. Dark chocolate and baking chocolate are the most dangerous, but all chocolate should be considered off-limits.</p>
        <p><strong>Feed instead:</strong> Blueberries, strawberries, or pomegranate seeds — naturally sweet and packed with antioxidants.</p>

        <h2>3. Caffeine</h2>
        <p>Coffee, tea, energy drinks, and caffeinated sodas are dangerous for birds. Caffeine causes cardiac arrhythmias, hyperactivity, increased heart rate, and can be fatal even in small amounts. Birds are much smaller than humans, so even a few sips from your coffee cup can deliver a dangerously concentrated dose.</p>
        <p><strong>Feed instead:</strong> Fresh water is all your bird needs to drink. For a treat, try offering a shallow dish of room-temperature chamomile tea (decaffeinated and unsweetened) — some birds enjoy bathing in it.</p>

        <h2>4. Onions and Garlic</h2>
        <p>Onions contain sulfur compounds that can rupture red blood cells in birds, leading to hemolytic anemia. Garlic, while less toxic than onions, contains allicin which can also cause irritation to the mouth, crop, and digestive tract. Both raw and cooked forms are dangerous, and the effects can be cumulative — meaning small exposures over time can add up to serious problems.</p>
        <p><strong>Feed instead:</strong> Bell peppers (all colors) are an excellent alternative — they're packed with vitamin A and vitamin C, and most birds love them. Sweet potato (cooked) is another safe, nutritious option.</p>

        <h2>5. Salt and High-Sodium Foods</h2>
        <p>Birds have very small bodies and even a small amount of excess salt can disrupt their electrolyte balance, leading to dehydration, kidney failure, and death. Common high-sodium foods to avoid include chips, pretzels, crackers, processed meats, and salted nuts.</p>
        <p><strong>Feed instead:</strong> Unsalted almonds, walnuts, or raw pumpkin seeds (in moderation — nuts are high in fat). Fresh snap peas, broccoli florets, and corn on the cob are also great low-sodium options that provide satisfying crunch.</p>

        <h2>Bonus: Other Foods to Avoid</h2>
        <ul>
          <li><strong>Fruit pits and apple seeds:</strong> Contain trace amounts of cyanide compounds. Remove all pits and seeds before offering fruit.</li>
          <li><strong>Alcohol:</strong> Even tiny amounts can cause organ failure in birds.</li>
          <li><strong>Mushrooms:</strong> Can cause liver failure in some species.</li>
          <li><strong>Xylitol (sugar-free sweetener):</strong> Found in sugar-free gum, candies, and some peanut butters. Toxic to birds.</li>
          <li><strong>Raw beans:</strong> Contain hemagglutinin, which is toxic. Always cook beans thoroughly before offering them.</li>
        </ul>

        <h2>What a Healthy Bird Diet Looks Like</h2>
        <p>A balanced diet for most pet parrots, cockatiels, and conures should include:</p>
        <ul>
          <li><strong>High-quality pellets:</strong> Should make up 60-70% of the diet. Pellets are nutritionally complete and prevent the selective eating that happens with seed-only diets.</li>
          <li><strong>Fresh vegetables (daily):</strong> Dark leafy greens (kale, Swiss chard, dandelion greens), bell peppers, carrots, sweet potato, broccoli, snap peas.</li>
          <li><strong>Fresh fruits (in moderation):</strong> Berries, mango, papaya, melon, banana, apple (without seeds). Fruit is high in sugar, so keep it to about 10% of the diet.</li>
          <li><strong>Seeds and nuts (as treats only):</strong> Sunflower seeds, safflower seeds, almonds, and walnuts in small amounts. Seeds are high in fat and should not be the primary diet.</li>
        </ul>
        <p>Transitioning a bird from a seed-only diet to pellets takes patience. Our veterinarians at SPAH in Alhambra can guide you through the process safely during a <a href="../bird-vet-alhambra.html">bird wellness exam</a>.</p>

        <h2>What to Do If Your Bird Eats Something Toxic</h2>
        <p>If you suspect your bird has eaten any of the foods listed above:</p>
        <ul>
          <li><strong>Don't wait for symptoms.</strong> Birds metabolize food quickly and can decline rapidly.</li>
          <li><strong>Call your vet immediately.</strong> Contact South Pasadena Animal Hospital at <a href="tel:6264411314">(626) 441-1314</a> during business hours.</li>
          <li><strong>Note what was eaten, how much, and when.</strong> This helps your vet assess the severity.</li>
          <li><strong>Do NOT induce vomiting.</strong> Birds cannot vomit safely the way dogs can. Attempting to make a bird vomit can cause aspiration and death.</li>
        </ul>

        <p>For after-hours emergencies, contact your nearest emergency animal hospital. We're located at <strong>3116 W Main St, Alhambra, CA 91801</strong> and are open Monday through Friday, 8 AM to 6 PM.</p>
""",
        "related_cards": [
            related_card("bird-feather-plucking.html", "#E3F2FD 0%,#BBDEFB 100%", "🐦", "tag-bird", "BIRD", "Why Is My Bird Pulling Out Its Feathers?"),
            related_card("exotic-pet-first-vet-visit.html", "#FCE4EC 0%,#F8BBD0 100%", "🐾", "tag-exotic", "ALL EXOTICS", "What to Expect at Your Exotic Pet's First Vet Visit"),
        ],
        "cta_text": "Book a Bird Wellness Exam in Alhambra",
    },
]


# ─── Build HTML Template ─────────────────────────────────────────────

TEMPLATE = """{head_start}
  <title>{title}</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.spah.la/blog/{file}" />
{og}
{schema}
{breadcrumb}
{styles}
</head>
<body>
{nav}

  <!-- BREADCRUMB -->
  <div class="max-w-3xl mx-auto px-6 pt-6">
    <p class="font-body text-xs text-muted">
      <a href="../index.html" class="hover:text-brand transition-colors">Home</a>
      <span class="mx-1">/</span>
      <a href="index.html" class="hover:text-brand transition-colors">Blog</a>
      <span class="mx-1">/</span>
      <span class="text-dark/60">{breadcrumb_name}</span>
    </p>
  </div>

  <!-- ARTICLE -->
  <article class="max-w-3xl mx-auto px-6 pt-8 pb-16">
    <span class="tag {tag_class}">{tag_text}</span>
    <p class="font-body text-muted text-xs mt-3 mb-4">{date_text}</p>
    <h1 class="font-display text-3xl sm:text-4xl font-bold text-dark mb-8" style="letter-spacing:-0.02em;line-height:1.2;">{h1}</h1>
    <div class="prose">
{content}
    </div>
  </article>

  <!-- RELATED ARTICLES -->
  <section class="py-16 bg-warm">
    <div class="max-w-3xl mx-auto px-6">
      <h2 class="font-display text-2xl font-bold text-dark text-center mb-8">Related Articles</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
{related}
      </div>
    </div>
  </section>

  <!-- CTA -->
{cta}

{footer}"""


# ─── Generate Files ──────────────────────────────────────────────────

for b in blogs:
    url = f"https://www.spah.la/blog/{b['file']}"
    html = TEMPLATE.format(
        head_start=HEAD_START,
        title=b["title"],
        meta_desc=b["meta_desc"],
        keywords=b["keywords"],
        file=b["file"],
        og=og_meta(b["title"], b["og_desc"], url),
        schema=blog_schema(b["schema_headline"], b["schema_desc"], url),
        breadcrumb=breadcrumb_schema(b["breadcrumb_name"]),
        styles=STYLES_AND_FONTS,
        nav=NAV,
        breadcrumb_name=b["breadcrumb_name"],
        tag_class=b["tag_class"],
        tag_text=b["tag_text"],
        date_text=b["date_text"],
        h1=b["h1"],
        content=b["content"],
        related="\n".join(b["related_cards"]),
        cta=cta_section(b["cta_text"]),
        footer=FOOTER,
    )
    filepath = os.path.join(BLOG_DIR, b["file"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: blog/{b['file']}")

print(f"\nDone! Generated {len(blogs)} Alhambra-focused blog posts.")
