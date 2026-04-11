"""
Generate 5 species-specific landing pages for SPAH.
Each page targets "[species] vet Alhambra" and related keywords.
Design matches the existing geo pages (vet-alhambra.html template).
"""

import os

OUTPUT_DIR = r"C:\Users\rchia\Documents\SPAH-website"

# ─── Shared HTML Parts ───────────────────────────────────────────────

NOTICE_BANNER = '''  <!-- NOTICE BANNER -->
  <div class="text-center py-2 px-4 text-sm font-body font-bold tracking-wide" style="background: #FDDDE6; color: #2A3442;">
    Sorry, we are not accepting new clients at this time except <strong>exotics appointments</strong>. &nbsp;<a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank" class="underline hover:no-underline" style="color:#5A7FA6;">Book now&nbsp;&rarr;</a>
  </div>'''

NAV = '''  <!-- NAV -->
  <nav class="sticky top-0 z-50 bg-warm/95 backdrop-blur-sm border-b border-sky/20" style="box-shadow: 0 2px 12px rgba(90,127,166,0.08);">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-center gap-10 relative">
      <div class="hidden md:flex items-center gap-8">
        <a href="index.html"    class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">HOME</a>
        <a href="about.html"    class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">ABOUT US</a>
        <a href="services.html" class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">SERVICES</a>
      </div>
      <a href="index.html">
        <img src="images/spah-logo-new.png"
             alt="South Pasadena Animal Hospital logo -- veterinarian serving Alhambra and South Pasadena" class="h-[70px]" />
      </a>
      <div class="hidden md:flex items-center gap-8">
        <a href="pricing.html"  class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">PRICING</a>
        <a href="contact.html"  class="nav-link text-dark/70 hover:text-brand font-body text-sm tracking-wide transition-colors duration-200">CONTACT</a>
        <a href="https://spah.koala.health/" target="_blank" class="nav-link text-terra font-body text-sm tracking-wide font-bold">PHARMACY &nearr;</a>
      </div>
      <button id="menuBtn" class="md:hidden absolute right-6 text-dark" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
    <div id="mobileMenu" class="hidden md:hidden px-6 pb-4 flex-col gap-4 bg-warm border-t border-sky/20">
      <a href="index.html"    class="text-dark/70 font-body text-sm tracking-wide py-3">HOME</a>
      <a href="about.html"    class="text-dark/70 font-body text-sm tracking-wide py-3">ABOUT US</a>
      <a href="services.html" class="text-dark/70 font-body text-sm tracking-wide py-3">SERVICES</a>
      <a href="pricing.html"  class="text-dark/70 font-body text-sm tracking-wide py-3">PRICING</a>
      <a href="contact.html"  class="text-dark/70 font-body text-sm tracking-wide py-3">CONTACT</a>
      <a href="https://spah.koala.health/" target="_blank" class="text-terra font-body text-sm font-bold py-3">PHARMACY &nearr;</a>
    </div>
  </nav>'''

FOOTER = '''  <!-- FOOTER -->
  <footer class="bg-sky/15 pt-12 pb-[84px] md:pb-6">
    <div class="max-w-6xl mx-auto px-6">
      <div class="pb-8 mb-8 border-b border-dark/10">
        <div class="mb-8">
          <img src="images/spah-logo-new-lg.png"
               alt="South Pasadena Animal Hospital logo -- veterinary clinic near Alhambra and South Pasadena" class="h-[77px] mb-4" />
          <p class="font-body text-dark text-sm leading-relaxed max-w-lg" style="line-height:1.7;">Compassionate, comprehensive care for pets of all shapes and sizes. Proudly serving Alhambra, South Pasadena, San Marino, Highland Park, Altadena, and greater Los Angeles.</p>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-2 gap-6 max-w-lg">
          <div>
            <h4 class="font-body font-bold tracking-widest text-xs uppercase text-dark/80 mb-4">Quick Links</h4>
            <div class="flex flex-col gap-2">
              <a href="index.html"    class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Home</a>
              <a href="about.html"    class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">About Us</a>
              <a href="services.html" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Services</a>
              <a href="contact.html"  class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Contact</a>
              <a href="https://spah.koala.health/" target="_blank" class="font-body text-terra font-bold text-sm hover:text-brand transition-colors duration-200">Online Pharmacy &nearr;</a>
              <a href="blog/"         class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">Blog</a>
            </div>
          </div>
          <div>
            <h4 class="font-body font-bold tracking-widest text-xs uppercase text-dark/80 mb-4">Contact</h4>
            <div class="flex flex-col gap-2">
              <p class="font-body text-dark text-sm">3116 W Main St<br />Alhambra, CA 91801</p>
              <a href="tel:6264411314"      class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">(626) 441-1314</a>
              <a href="mailto:info@spah.la" class="font-body text-dark text-sm hover:text-brand transition-colors duration-200">info@spah.la</a>
              <div class="flex gap-3 mt-1">
                <a href="https://www.instagram.com/southpasah" target="_blank" rel="noopener noreferrer" aria-label="Instagram" class="text-dark/60 hover:text-brand transition-colors duration-200">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
                </a>
                <a href="https://www.tiktok.com/@southpasah" target="_blank" rel="noopener noreferrer" aria-label="TikTok" class="text-dark/60 hover:text-brand transition-colors duration-200">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 0 0-.79-.05A6.34 6.34 0 0 0 3.15 15a6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.34-6.34V8.75a8.18 8.18 0 0 0 4.76 1.52V6.84a4.83 4.83 0 0 1-1-.15z"/></svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-col md:flex-row justify-between items-center gap-3">
        <p class="font-body text-dark/60 text-xs">&copy; 2026 South Pasadena Animal Hospital. Est. 2023.</p>
        <a href="contact.html" class="font-body text-dark/60 text-xs hover:text-dark transition-colors duration-200">Privacy Policy</a>
      </div>
      <p class="font-body text-center mt-2" style="font-size:9px;color:rgba(42,52,66,0.08);letter-spacing:0.02em;">Serving: <a href="vet-alhambra.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Alhambra</a> &middot; <a href="vet-south-pasadena.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">South Pasadena</a> &middot; <a href="exotic-vet-pasadena.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Pasadena</a> &middot; <a href="vet-highland-park.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Highland Park</a> &middot; <a href="vet-san-gabriel.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">San Gabriel</a> &middot; <a href="vet-monterey-park.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Monterey Park</a> &middot; <a href="vet-san-marino.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">San Marino</a> &middot; <a href="vet-rosemead.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Rosemead</a> &middot; <a href="vet-eagle-rock.html" style="color:rgba(42,52,66,0.08);" class="no-underline hover:underline">Eagle Rock</a></p>
    </div>
  </footer>'''

MOBILE_JS = '''  <script>
    document.getElementById('menuBtn').addEventListener('click', () => {
      const menu = document.getElementById('mobileMenu');
      menu.classList.toggle('hidden');
      menu.classList.toggle('flex');
    });
  </script>'''

STICKY_CTA = '''  <!-- Sticky Mobile CTA Bar -->
  <div id="sticky-cta" class="md:hidden" style="position:fixed;bottom:0;left:0;right:0;z-index:40;transform:translateY(100%);transition:transform 0.4s cubic-bezier(0.4,0,0.2,1);">
    <div style="background:rgba(255,255,255,0.97);backdrop-filter:blur(12px);border-top:1px solid rgba(90,127,166,0.12);padding:10px 16px;display:flex;gap:10px;align-items:center;box-shadow:0 -2px 16px rgba(42,52,66,0.08);">
      <a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank"
         style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:#5A7FA6;color:white;font-family:'Lato',sans-serif;font-weight:700;font-size:0.9rem;letter-spacing:0.03em;border-radius:9999px;padding:14px 0;text-decoration:none;box-shadow:0 2px 8px rgba(90,127,166,0.25);-webkit-tap-highlight-color:transparent;">
        Book Appointment
      </a>
      <a href="tel:6264411314"
         style="display:flex;align-items:center;justify-content:center;width:50px;height:50px;border-radius:9999px;background:#EDF3F0;color:#7A9E8E;flex-shrink:0;-webkit-tap-highlight-color:transparent;"
         aria-label="Call (626) 441-1314">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.362 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
      </a>
    </div>
  </div>
  <script>
    (function() {
      var bar = document.getElementById('sticky-cta');
      if (!bar || window.innerWidth >= 768) return;
      var shown = false;
      window.addEventListener('scroll', function() {
        if (window.scrollY > 300 && !shown) { shown = true; bar.style.transform = 'translateY(0)'; }
        else if (window.scrollY <= 300 && shown) { shown = false; bar.style.transform = 'translateY(100%)'; }
      }, { passive: true });
    })();
  </script>'''

USERWAY = '''<!-- UserWay Accessibility Widget -->
<style>
  .userway_buttons_wrapper,.uwy.userway_buttons_wrapper,.uwy{left:16px!important;right:auto!important;top:16px!important;bottom:auto!important;transition:opacity .3s ease!important;}
</style>
<script src="https://cdn.userway.org/widget.js" data-account="s8qKqbCCo7" data-position="4" defer></script>
<script>
(function(){
  var scrollTimer;
  function setUWOpacity(v){
    document.querySelectorAll('.userway_buttons_wrapper,.uwy').forEach(function(el){el.style.opacity=v;});
  }
  window.addEventListener('scroll',function(){
    setUWOpacity('0');
    clearTimeout(scrollTimer);
    scrollTimer=setTimeout(function(){if(window.scrollY<10)setUWOpacity('1');},300);
  },{passive:true});
  setTimeout(function(){if(window.scrollY>10)setUWOpacity('0');},2000);
})();
</script>'''

INLINE_STYLES = '''  <style>
    body { font-family: 'Lato', sans-serif; background: #FAFAF8; color: #2A3442; }
    h1, h2, h3, h4 { font-family: 'Playfair Display', serif; }
    .card-shadow { box-shadow: 0 2px 4px rgba(90,127,166,0.06), 0 8px 24px rgba(90,127,166,0.10); }
    .btn-primary { background: #5A7FA6; color: white; border-radius: 9999px; padding: 0.75rem 2rem; font-family: 'Lato', sans-serif; font-weight: 700; letter-spacing: 0.04em; transition: background 0.2s ease, transform 0.2s ease; }
    .btn-primary:hover { background: #4A6D92; transform: scale(1.03); }
    .nav-link { position: relative; }
    .nav-link::after { content: ''; position: absolute; bottom: -2px; left: 0; right: 0; height: 2px; background: #7A9E8E; transform: scaleX(0); transform-origin: left; transition: transform 0.25s ease; }
    .nav-link:hover::after { transform: scaleX(1); }
  </style>'''

# ─── Species Page Definitions ────────────────────────────────────────

species_pages = [
    # ── 1. REPTILE VET ──
    {
        "file": "reptile-vet-alhambra.html",
        "slug": "reptile-vet-alhambra",
        "title": "Reptile Vet in Alhambra, CA | Bearded Dragons, Geckos & More | SPAH",
        "meta_desc": "Looking for a reptile vet in Alhambra? South Pasadena Animal Hospital provides veterinary care for bearded dragons, geckos, turtles, tortoises, and snakes. Call (626) 441-1314.",
        "keywords": "reptile vet Alhambra, reptile vet near me, bearded dragon vet Alhambra, gecko vet Alhambra, turtle vet Alhambra, snake vet Alhambra, tortoise vet Los Angeles, reptile veterinarian San Gabriel Valley, lizard vet near me, chameleon vet Alhambra",
        "og_title": "Reptile Vet in Alhambra, CA | Bearded Dragons, Geckos, Turtles & Snakes | SPAH",
        "og_desc": "South Pasadena Animal Hospital treats bearded dragons, geckos, turtles, tortoises, snakes, and other reptiles in Alhambra. Book a reptile wellness exam today.",
        "breadcrumb_name": "Reptile Vet in Alhambra",
        "hero_label": "REPTILE VETERINARY CARE",
        "h1": "Your Reptile Vet in Alhambra",
        "hero_desc": "Finding a vet who truly understands reptiles can be a challenge. At South Pasadena Animal Hospital, our veterinarians have years of hands-on experience with bearded dragons, leopard geckos, ball pythons, tortoises, chameleons, and more. From routine wellness exams and husbandry consultations to illness diagnosis and treatment, we provide the kind of knowledgeable, compassionate reptile care that's hard to find in the San Gabriel Valley.",
        "why_heading": "Why Reptile Owners in Alhambra Choose SPAH",
        "why_cards": [
            {
                "icon_bg": "#EDF3F0", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
                "title": "Reptile-Experienced Veterinarians",
                "text": "Our vets have cared for hundreds of reptiles — from common bearded dragons to rare monitor lizards. We understand the unique physiology, metabolic needs, and disease patterns of cold-blooded pets."
            },
            {
                "icon_bg": "#F7EDE5", "icon_stroke": "#A8673A",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#A8673A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
                "title": "Husbandry Guidance Included",
                "text": "Lighting, heating, humidity, diet — we review your entire setup at every visit. Most reptile health issues are husbandry-related, and fixing the environment is often the best medicine."
            },
            {
                "icon_bg": "#D6DFED", "icon_stroke": "#5A7FA6",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#5A7FA6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                "title": "In-House Diagnostics for Reptiles",
                "text": "We run bloodwork, fecal tests, and X-rays on-site so we can diagnose issues quickly. No waiting days for outside lab results — we get answers while you're still here."
            },
            {
                "icon_bg": "#D4E5D9", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
                "title": "Transparent, Fair Pricing",
                "text": 'We publish our prices online so you know what to expect before your visit. No surprise fees — just honest, affordable reptile vet care. <a href="pricing.html" class="text-brand hover:underline">View our prices</a>.'
            },
        ],
        "species_section_heading": "Reptiles We Commonly Treat",
        "species_list": [
            {"name": "Bearded Dragons", "desc": "Wellness exams, metabolic bone disease screening, husbandry reviews, parasite testing, and appetite issues."},
            {"name": "Leopard & Crested Geckos", "desc": "Eye problems, stuck shed, tail loss, weight monitoring, and nutritional support."},
            {"name": "Ball Pythons & Other Snakes", "desc": "Respiratory infections, mite treatment, feeding issues, pre-purchase health checks."},
            {"name": "Turtles & Tortoises", "desc": "Shell rot, respiratory illness, beak and nail trims, metabolic bone disease, hibernation guidance."},
            {"name": "Chameleons", "desc": "Eye infections, MBD prevention, hydration assessment, supplementation advice."},
            {"name": "Monitor Lizards & Tegus", "desc": "Wellness checkups, wound care, nutritional counseling for large lizards."},
        ],
        "faq_heading": "Reptile Vet FAQ — Alhambra",
        "faqs": [
            {"q": "Do reptiles need annual vet visits?", "a": "Yes. Reptiles are excellent at hiding illness, so an annual wellness exam with bloodwork can catch problems like metabolic bone disease, parasites, or organ issues before they become serious. We recommend at least one checkup per year for all reptiles."},
            {"q": "How much does a reptile vet visit cost?", "a": 'Our reptile wellness exam fee is published on our <a href="pricing.html" class="text-brand hover:underline">pricing page</a>. Additional diagnostics like bloodwork or X-rays are quoted before we proceed, so there are no surprises.'},
            {"q": "What should I bring to my reptile's first vet visit?", "a": "Bring your reptile in a secure, ventilated carrier with a heat source (hand warmer wrapped in a towel works well). Also bring photos of their enclosure, a list of their diet, and any supplements you use. This helps us assess their husbandry along with their health."},
            {"q": "Can you treat my bearded dragon for metabolic bone disease?", "a": "Absolutely. MBD is one of the most common conditions we see in bearded dragons. Treatment typically involves calcium and vitamin D3 supplementation, UVB lighting correction, and dietary adjustments. Early detection leads to the best outcomes."},
            {"q": "Do you see reptiles on a walk-in basis?", "a": "We recommend booking an appointment to ensure your reptile gets the time and attention it deserves. Call (626) 441-1314 or book online. We do our best to accommodate same-day requests when available."},
        ],
        "related_blogs": [
            {"url": "blog/signs-bearded-dragon-needs-vet.html", "title": "Signs Your Bearded Dragon Needs to See a Vet"},
        ],
        "seo_heading": "Your Local Reptile Veterinarian in Alhambra",
        "seo_content": """<p>If you have been searching for a reptile vet in Alhambra or the greater San Gabriel Valley, South Pasadena Animal Hospital is here to help. Located at 3116 West Main Street in Alhambra, our clinic is one of the few in the area that provides comprehensive veterinary care for reptiles alongside dogs, cats, and other exotic pets. Whether you have a bearded dragon that has stopped eating, a gecko with stuck shed, or a ball python with a respiratory infection, our veterinarians have the training and hands-on experience to diagnose and treat a wide range of reptile health conditions.</p>

        <p>Reptile medicine requires a different approach than traditional small animal practice. Reptiles have unique metabolic needs that are closely tied to their environment — temperature gradients, UVB lighting, humidity levels, and diet all play a critical role in their health. That is why every reptile visit at SPAH includes a thorough husbandry review alongside the physical examination. We often find that small adjustments to the enclosure setup can resolve or prevent many common health problems, from metabolic bone disease in bearded dragons to respiratory issues in snakes and chameleons.</p>

        <p>Our in-house diagnostic capabilities include reptile bloodwork, fecal parasite screening, and digital X-rays, allowing us to get answers quickly without referring you to a distant facility. We also provide <a href="services.html" class="text-brand hover:underline">surgical services</a> for reptiles when needed, including mass removals and egg-binding interventions. For pricing information, visit our <a href="pricing.html" class="text-brand hover:underline">pricing page</a> where all fees are published upfront.</p>

        <p>Pet owners from across the San Gabriel Valley — including Pasadena, <a href="vet-san-gabriel.html" class="text-brand hover:underline">San Gabriel</a>, <a href="vet-monterey-park.html" class="text-brand hover:underline">Monterey Park</a>, Rosemead, Temple City, and <a href="vet-highland-park.html" class="text-brand hover:underline">Highland Park</a> — bring their reptiles to SPAH because quality reptile veterinary care is genuinely hard to find locally. If your scaly companion needs a checkup or you are concerned about a health issue, <a href="contact.html" class="text-brand hover:underline">reach out to us</a> to schedule a reptile appointment.</p>""",
        "cta_heading": "Ready to Book a Reptile Exam?",
    },

    # ── 2. BIRD VET ──
    {
        "file": "bird-vet-alhambra.html",
        "slug": "bird-vet-alhambra",
        "title": "Bird Vet in Alhambra, CA | Parrots, Cockatiels & Parakeets | SPAH",
        "meta_desc": "Need an avian vet in Alhambra? South Pasadena Animal Hospital provides veterinary care for parrots, cockatiels, parakeets, finches, and other pet birds. Call (626) 441-1314.",
        "keywords": "bird vet Alhambra, avian vet near me, parrot vet Alhambra, cockatiel vet Los Angeles, parakeet vet near me, bird veterinarian San Gabriel Valley, avian vet Pasadena, bird vet near me, conure vet Alhambra, bird wellness exam",
        "og_title": "Bird Vet in Alhambra, CA | Parrots, Cockatiels, Conures & More | SPAH",
        "og_desc": "South Pasadena Animal Hospital treats parrots, cockatiels, conures, parakeets, finches, and other pet birds in Alhambra. Book an avian wellness exam today.",
        "breadcrumb_name": "Bird Vet in Alhambra",
        "hero_label": "AVIAN VETERINARY CARE",
        "h1": "Your Bird Vet in Alhambra",
        "hero_desc": "Birds are intelligent, sensitive creatures that require a vet who understands their unique anatomy and behavior. At South Pasadena Animal Hospital, our veterinarians provide comprehensive care for parrots, cockatiels, conures, parakeets, finches, canaries, and other companion birds. From annual wellness exams and beak trims to illness diagnosis and feather-plucking consultations, we give your feathered family member the attentive care they deserve.",
        "why_heading": "Why Bird Owners in Alhambra Choose SPAH",
        "why_cards": [
            {
                "icon_bg": "#EDF3F0", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
                "title": "Experienced with Companion Birds",
                "text": "From tiny finches to large macaws, our vets understand avian physiology, behavior, and the subtle signs that indicate illness in birds — who are notorious for hiding symptoms until they're seriously sick."
            },
            {
                "icon_bg": "#F7EDE5", "icon_stroke": "#A8673A",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#A8673A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>',
                "title": "Low-Stress Bird Handling",
                "text": "We know that vet visits can be stressful for birds. Our team uses gentle restraint techniques and keeps exam times efficient to minimize anxiety for your feathered companion."
            },
            {
                "icon_bg": "#D6DFED", "icon_stroke": "#5A7FA6",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#5A7FA6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                "title": "On-Site Avian Diagnostics",
                "text": "We perform bloodwork, fecal gram stains, crop washes, and X-rays in-house for quick results. Rapid diagnosis is critical for birds since they can decline fast."
            },
            {
                "icon_bg": "#D4E5D9", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
                "title": "Transparent Pricing",
                "text": 'No surprise bills. Our exam fees and common services are posted online so you can plan your visit with confidence. <a href="pricing.html" class="text-brand hover:underline">View our prices</a>.'
            },
        ],
        "species_section_heading": "Birds We Commonly Treat",
        "species_list": [
            {"name": "Cockatiels & Cockatoos", "desc": "Wellness exams, feather plucking evaluation, respiratory issues, beak and nail trims, nutritional counseling."},
            {"name": "Parrots & Macaws", "desc": "Annual checkups, behavioral consultations, blood panels, Psittacosis testing, wing trims."},
            {"name": "Conures & Lovebirds", "desc": "Wellness exams, feather condition assessment, crop issues, egg-binding evaluation."},
            {"name": "Parakeets (Budgies)", "desc": "Respiratory infections, mite infestations, tumor screening, nutritional guidance."},
            {"name": "Finches & Canaries", "desc": "Air sac mite treatment, respiratory support, wellness monitoring, leg band issues."},
            {"name": "Doves & Pigeons", "desc": "Canker treatment, respiratory disease, wellness exams, parasite screening."},
        ],
        "faq_heading": "Bird Vet FAQ — Alhambra",
        "faqs": [
            {"q": "Do pet birds need annual vet checkups?", "a": "Yes. Birds are prey animals and instinctively hide illness. An annual exam with bloodwork can catch diseases like liver problems, infections, or nutritional deficiencies before visible symptoms appear. Early detection saves lives."},
            {"q": "Why is my bird plucking its feathers?", "a": 'Feather plucking can be caused by medical issues (skin infections, liver disease, hormonal imbalances) or behavioral factors (stress, boredom, improper lighting). A thorough vet exam is the first step to finding the cause. Read our <a href="blog/bird-feather-plucking.html" class="text-brand hover:underline">guide to feather plucking</a> for more information.'},
            {"q": "How should I transport my bird to the vet?", "a": "Use a small, secure travel carrier or cage with a towel draped over it to reduce stress. Avoid temperature extremes — keep the car comfortable. Bring a sample of your bird's current food and a photo of their cage setup for the vet to review."},
            {"q": "Do you offer wing and nail trims for birds?", "a": "Yes, we provide wing trims, nail trims, and beak trims as part of our avian services. These can be done during a wellness exam or as a standalone grooming visit."},
            {"q": "What are signs my bird is sick?", "a": "Watch for fluffed feathers, sitting on the cage floor, decreased appetite, tail bobbing while breathing, nasal discharge, changes in droppings (color, consistency, volume), or unusual quietness. If you notice any of these, schedule a vet visit promptly."},
        ],
        "related_blogs": [
            {"url": "blog/bird-feather-plucking.html", "title": "Why Is My Bird Pulling Out Its Feathers?"},
        ],
        "seo_heading": "Your Local Avian Veterinarian in Alhambra",
        "seo_content": """<p>Finding a qualified bird vet in Alhambra and the San Gabriel Valley is not easy. Most general practice veterinary clinics focus exclusively on dogs and cats, leaving bird owners with few options nearby. South Pasadena Animal Hospital at 3116 West Main Street in Alhambra is proud to be one of the few local clinics that provides veterinary care for companion birds alongside our traditional small animal practice.</p>

        <p>Avian medicine requires an understanding of how birds differ from mammals — from their unique respiratory systems and hollow bones to their rapid metabolisms and tendency to mask symptoms of illness. Our veterinarians take the time to perform thorough physical exams, review diet and environment, and recommend appropriate diagnostics when needed. Whether your cockatiel has a respiratory wheeze, your parrot is plucking feathers, or your parakeet needs its first wellness exam, we approach each case with the knowledge and care your bird deserves.</p>

        <p>Our in-house diagnostic capabilities allow us to run avian bloodwork, perform fecal gram stains, take digital X-rays, and conduct crop washes — all without sending samples to an outside lab and waiting days for results. This is especially important for birds, who can deteriorate quickly once symptoms become apparent. We also offer <a href="services.html" class="text-brand hover:underline">grooming services</a> including wing, nail, and beak trims.</p>

        <p>Bird owners travel to SPAH from across the region, including Pasadena, <a href="vet-south-pasadena.html" class="text-brand hover:underline">South Pasadena</a>, <a href="vet-san-gabriel.html" class="text-brand hover:underline">San Gabriel</a>, Monterey Park, Arcadia, and <a href="vet-highland-park.html" class="text-brand hover:underline">Highland Park</a>, because quality avian veterinary care is genuinely rare in the area. If you are looking for a bird vet you can trust, <a href="contact.html" class="text-brand hover:underline">contact us</a> to schedule your bird's appointment.</p>""",
        "cta_heading": "Ready to Book a Bird Exam?",
    },

    # ── 3. RABBIT VET ──
    {
        "file": "rabbit-vet-alhambra.html",
        "slug": "rabbit-vet-alhambra",
        "title": "Rabbit Vet in Alhambra, CA | Wellness, GI Stasis & RHDV2 | SPAH",
        "meta_desc": "Looking for a rabbit vet in Alhambra? South Pasadena Animal Hospital provides wellness exams, GI stasis treatment, RHDV2 vaccines, dental care, and spay/neuter for rabbits. Call (626) 441-1314.",
        "keywords": "rabbit vet Alhambra, rabbit vet near me, bunny vet Alhambra, rabbit veterinarian Los Angeles, RHDV2 vaccine rabbit, GI stasis rabbit vet, rabbit spay neuter Alhambra, rabbit dental care, bunny vet San Gabriel Valley, exotic vet rabbit",
        "og_title": "Rabbit Vet in Alhambra, CA | Wellness Exams, GI Stasis & Dental Care | SPAH",
        "og_desc": "South Pasadena Animal Hospital provides comprehensive rabbit veterinary care in Alhambra — wellness exams, GI stasis treatment, RHDV2 vaccination, dental, and spay/neuter.",
        "breadcrumb_name": "Rabbit Vet in Alhambra",
        "hero_label": "RABBIT VETERINARY CARE",
        "h1": "Your Rabbit Vet in Alhambra",
        "hero_desc": "Rabbits are wonderful companions, but they need a vet who understands their unique digestive system, dental structure, and behavioral needs. At South Pasadena Animal Hospital, we provide comprehensive rabbit care — from annual wellness exams and RHDV2 vaccinations to GI stasis treatment, dental checks, and spay/neuter surgery. Our team treats every bunny with the gentle, knowledgeable care they deserve.",
        "why_heading": "Why Rabbit Owners in Alhambra Choose SPAH",
        "why_cards": [
            {
                "icon_bg": "#EDF3F0", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
                "title": "Rabbit-Savvy Veterinarians",
                "text": "Our vets understand rabbit-specific anatomy and medicine — from their continuously growing teeth and sensitive GI tracts to safe anesthesia protocols for spay/neuter procedures."
            },
            {
                "icon_bg": "#F7EDE5", "icon_stroke": "#A8673A",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#A8673A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg>',
                "title": "RHDV2 Vaccination Available",
                "text": "Rabbit Hemorrhagic Disease Virus 2 (RHDV2) is a deadly threat in California. We carry the RHDV2 vaccine to protect your bunny from this highly contagious and often fatal disease."
            },
            {
                "icon_bg": "#D6DFED", "icon_stroke": "#5A7FA6",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#5A7FA6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
                "title": "GI Stasis Urgent Care",
                "text": "GI stasis is the number one emergency in rabbits and can be fatal within 24-48 hours. We diagnose and treat GI stasis aggressively with fluid therapy, motility drugs, and pain management."
            },
            {
                "icon_bg": "#D4E5D9", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
                "title": "Transparent Pricing",
                "text": 'No hidden fees. We publish our exam and service prices so rabbit owners can plan ahead. <a href="pricing.html" class="text-brand hover:underline">View our prices</a>.'
            },
        ],
        "species_section_heading": "Rabbit Services We Offer",
        "species_list": [
            {"name": "Wellness Exams", "desc": "Comprehensive nose-to-tail checkups including weight, teeth, heart, lungs, gut sounds, and overall condition assessment."},
            {"name": "RHDV2 Vaccination", "desc": "Protection against Rabbit Hemorrhagic Disease Virus 2, which is present in California and can be fatal even in indoor rabbits."},
            {"name": "GI Stasis Treatment", "desc": "Aggressive treatment including subcutaneous fluids, gut motility medications, pain relief, syringe feeding support, and monitoring."},
            {"name": "Dental Checks & Molar Trims", "desc": "Rabbit teeth grow continuously. We check for malocclusion, spurs, and overgrown molars that cause pain and eating difficulties."},
            {"name": "Spay & Neuter", "desc": "Safe rabbit spay and neuter procedures using rabbit-appropriate anesthesia protocols. Spaying females prevents uterine cancer, which affects up to 80% of unspayed does."},
            {"name": "Parasite Screening", "desc": "Fecal testing for coccidia and other parasites, plus treatment for E. cuniculi and fur mites."},
        ],
        "faq_heading": "Rabbit Vet FAQ — Alhambra",
        "faqs": [
            {"q": "How often should my rabbit see a vet?", "a": "At least once a year for a wellness exam. Rabbits over 5 years old should be seen every 6 months since they're more prone to dental disease, arthritis, and other age-related conditions."},
            {"q": "What is GI stasis and why is it so dangerous?", "a": 'GI stasis occurs when a rabbit\'s digestive system slows or stops completely. Without treatment, it can be fatal within 24-48 hours. Signs include not eating, no droppings, lethargy, and a hunched posture. If you suspect GI stasis, call us immediately. Read our <a href="blog/rabbit-gi-stasis.html" class="text-brand hover:underline">complete guide to rabbit GI stasis</a>.'},
            {"q": "Does my indoor rabbit need the RHDV2 vaccine?", "a": "Yes. RHDV2 can be carried on shoes, clothing, and even by insects, meaning indoor rabbits are still at risk. The vaccine is the only reliable protection and is recommended for all pet rabbits in California."},
            {"q": "Should I spay or neuter my rabbit?", "a": "Absolutely. Spaying prevents uterine cancer (which affects up to 80% of unspayed female rabbits by age 5) and reduces territorial behavior. Neutering males reduces spraying and aggression. Both procedures are done safely at our clinic."},
            {"q": "What should I feed my rabbit?", "a": "A rabbit's diet should be 80% unlimited timothy hay, supplemented with fresh leafy greens (romaine, cilantro, parsley) and a small amount of high-quality pellets. Avoid seeds, nuts, and sugary treats. We review diet at every visit."},
        ],
        "related_blogs": [
            {"url": "blog/rabbit-gi-stasis.html", "title": "Rabbit GI Stasis: Symptoms, Treatment & Prevention"},
        ],
        "seo_heading": "Your Local Rabbit Veterinarian in Alhambra",
        "seo_content": """<p>Finding a rabbit-savvy vet in Alhambra and the San Gabriel Valley takes effort. Many general veterinary practices see rabbits infrequently and may not be up to date on the latest rabbit medicine, including RHDV2 vaccination protocols and safe anesthesia techniques for rabbit surgery. At South Pasadena Animal Hospital, located at 3116 West Main Street in Alhambra, rabbit care is a regular part of our practice and our veterinarians are well-versed in the unique health needs of these beloved pets.</p>

        <p>Rabbits are herbivores with a complex, sensitive digestive system that requires a high-fiber diet and consistent gut motility. GI stasis — a condition where the gut slows or stops — is the most common emergency we see in rabbits and can be life-threatening within a day or two if untreated. Our team is experienced in recognizing and treating GI stasis quickly with aggressive supportive care. We also focus heavily on prevention, counseling rabbit owners on proper diet, exercise, and stress management at every visit.</p>

        <p>Dental disease is another major concern in rabbits. Their teeth grow continuously throughout life, and misaligned teeth can develop painful spurs that prevent eating. We perform dental exams at every wellness visit and offer molar trims when needed. We also provide <a href="services.html" class="text-brand hover:underline">spay and neuter surgery</a> using rabbit-safe anesthesia, as well as RHDV2 vaccination to protect against this fatal virus that has been confirmed in California.</p>

        <p>Rabbit owners bring their bunnies to SPAH from across the area, including Pasadena, <a href="vet-south-pasadena.html" class="text-brand hover:underline">South Pasadena</a>, <a href="vet-san-gabriel.html" class="text-brand hover:underline">San Gabriel</a>, <a href="vet-monterey-park.html" class="text-brand hover:underline">Monterey Park</a>, Arcadia, and <a href="vet-highland-park.html" class="text-brand hover:underline">Highland Park</a>. If your rabbit needs a vet who truly understands bunny medicine, <a href="contact.html" class="text-brand hover:underline">contact us</a> to book an appointment.</p>""",
        "cta_heading": "Ready to Book a Rabbit Exam?",
    },

    # ── 4. GUINEA PIG VET ──
    {
        "file": "guinea-pig-vet-alhambra.html",
        "slug": "guinea-pig-vet-alhambra",
        "title": "Guinea Pig Vet in Alhambra, CA | Wellness & URI Treatment | SPAH",
        "meta_desc": "Need a guinea pig vet in Alhambra? South Pasadena Animal Hospital treats guinea pigs for respiratory infections, dental issues, skin problems, and wellness exams. Call (626) 441-1314.",
        "keywords": "guinea pig vet Alhambra, guinea pig vet near me, cavy vet Los Angeles, guinea pig veterinarian, guinea pig respiratory infection, guinea pig sneezing vet, guinea pig dental care, small animal vet Alhambra, exotic vet guinea pig, guinea pig wellness exam",
        "og_title": "Guinea Pig Vet in Alhambra, CA | Wellness, URI & Dental Care | SPAH",
        "og_desc": "South Pasadena Animal Hospital provides guinea pig veterinary care in Alhambra — wellness exams, respiratory infection treatment, dental checks, and nutritional guidance.",
        "breadcrumb_name": "Guinea Pig Vet in Alhambra",
        "hero_label": "GUINEA PIG VETERINARY CARE",
        "h1": "Your Guinea Pig Vet in Alhambra",
        "hero_desc": "Guinea pigs are social, vocal, and full of personality — and they deserve a vet who understands their specific health needs. At South Pasadena Animal Hospital, we provide complete guinea pig care including wellness exams, respiratory infection treatment, dental checks, skin and parasite care, and vitamin C supplementation guidance. Our team handles every guinea pig with patience and gentle hands.",
        "why_heading": "Why Guinea Pig Owners in Alhambra Choose SPAH",
        "why_cards": [
            {
                "icon_bg": "#EDF3F0", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
                "title": "Guinea Pig-Knowledgeable Vets",
                "text": "We understand guinea pig physiology — from their vitamin C requirements and continuously growing teeth to their sensitivity to certain antibiotics that are safe for other animals but dangerous for cavies."
            },
            {
                "icon_bg": "#F7EDE5", "icon_stroke": "#A8673A",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#A8673A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
                "title": "URI Detection & Treatment",
                "text": "Upper respiratory infections are the most common illness in guinea pigs and can turn serious quickly. We diagnose and treat URIs promptly with guinea pig-safe antibiotics."
            },
            {
                "icon_bg": "#D6DFED", "icon_stroke": "#5A7FA6",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#5A7FA6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                "title": "In-House Diagnostics",
                "text": "Bloodwork, X-rays, and fecal tests done on-site mean faster answers and faster treatment for your guinea pig."
            },
            {
                "icon_bg": "#D4E5D9", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
                "title": "Transparent Pricing",
                "text": 'We believe in upfront pricing with no surprises. Check our published fees before your visit. <a href="pricing.html" class="text-brand hover:underline">View our prices</a>.'
            },
        ],
        "species_section_heading": "Guinea Pig Services We Offer",
        "species_list": [
            {"name": "Wellness Exams", "desc": "Full physical assessment including weight tracking, teeth check, heart and lung auscultation, skin inspection, and diet review."},
            {"name": "Respiratory Infection Treatment", "desc": "Diagnosis and treatment of URIs caused by Bordetella, Streptococcus, and other bacteria using guinea pig-safe antibiotics."},
            {"name": "Dental Care", "desc": "Assessment for malocclusion and overgrown molars, which cause drooling, weight loss, and difficulty eating."},
            {"name": "Skin & Parasite Care", "desc": "Treatment for fungal infections (ringworm), mites, lice, and other skin conditions common in guinea pigs."},
            {"name": "Vitamin C Guidance", "desc": "Guinea pigs cannot produce their own vitamin C. We assess for deficiency (scurvy) and recommend proper supplementation."},
            {"name": "Bladder Stone Evaluation", "desc": "X-rays and treatment planning for bladder stones and sludge, which are common in guinea pigs due to calcium metabolism."},
        ],
        "faq_heading": "Guinea Pig Vet FAQ — Alhambra",
        "faqs": [
            {"q": "How often should my guinea pig see a vet?", "a": "At least once a year for a wellness exam. Guinea pigs over 4 years old should be seen every 6 months since they're more prone to dental disease, bladder stones, and tumors as they age."},
            {"q": "My guinea pig is sneezing — should I be worried?", "a": 'Occasional sneezing from dust or bedding is normal, but persistent sneezing, nasal discharge, wheezing, or crusty eyes can signal an upper respiratory infection that needs veterinary treatment. Read our <a href="blog/guinea-pig-sneezing.html" class="text-brand hover:underline">guide to guinea pig sneezing</a> for more details.'},
            {"q": "Why are some antibiotics dangerous for guinea pigs?", "a": "Guinea pigs have a delicate gut microbiome, and certain antibiotics (like amoxicillin and penicillin) can destroy beneficial gut bacteria, causing fatal diarrhea. Our vets only use guinea pig-safe antibiotics and are well aware of which medications to avoid."},
            {"q": "Does my guinea pig need vitamin C supplements?", "a": "Yes. Unlike most mammals, guinea pigs cannot synthesize vitamin C and must get it from their diet. We recommend 25-50mg of vitamin C daily through fresh veggies (bell peppers, parsley) and a liquid supplement if needed."},
            {"q": "What bedding is best for guinea pigs?", "a": "We recommend paper-based bedding (like Carefresh) or fleece liners. Avoid cedar and pine shavings, which release aromatic oils that can irritate guinea pig respiratory systems and contribute to URIs."},
        ],
        "related_blogs": [
            {"url": "blog/guinea-pig-sneezing.html", "title": "Guinea Pig Sneezing: When to Worry and When It's Normal"},
        ],
        "seo_heading": "Your Local Guinea Pig Veterinarian in Alhambra",
        "seo_content": """<p>If you are searching for a guinea pig vet in Alhambra or the San Gabriel Valley, South Pasadena Animal Hospital is here to help. Located at 3116 West Main Street in Alhambra, our clinic regularly sees guinea pigs for wellness exams, illness treatment, and preventive care. Unlike many general veterinary practices that rarely treat cavies, our veterinarians are comfortable with guinea pig medicine and understand the critical differences between guinea pig care and care for other small animals.</p>

        <p>One of the most important things to know about guinea pigs is their sensitivity to certain antibiotics. Medications that are perfectly safe for dogs, cats, and even rabbits can be fatal to guinea pigs because they disrupt the delicate bacterial balance in their gut. Our vets know which antibiotics are safe and effective for guinea pigs and never prescribe medications that could harm them. This knowledge alone is a reason many cavy owners in the area specifically seek out a guinea pig-experienced vet.</p>

        <p>Upper respiratory infections, dental disease, bladder stones, and vitamin C deficiency are among the most common health issues we treat in guinea pigs. We perform all diagnostics in-house — including bloodwork, X-rays, and fecal tests — so we can get answers and start treatment the same day. We also spend time at every visit reviewing diet, housing, and social needs, because guinea pigs thrive when their husbandry is optimized.</p>

        <p>Guinea pig owners come to SPAH from across the region, including Pasadena, <a href="vet-south-pasadena.html" class="text-brand hover:underline">South Pasadena</a>, <a href="vet-san-gabriel.html" class="text-brand hover:underline">San Gabriel</a>, <a href="vet-monterey-park.html" class="text-brand hover:underline">Monterey Park</a>, Temple City, and <a href="vet-rosemead.html" class="text-brand hover:underline">Rosemead</a>. If your guinea pig needs a checkup or is showing signs of illness, <a href="contact.html" class="text-brand hover:underline">contact us</a> to schedule an appointment.</p>""",
        "cta_heading": "Ready to Book a Guinea Pig Exam?",
    },

    # ── 5. EXOTIC VET (CATCH-ALL) ──
    {
        "file": "exotic-vet-alhambra.html",
        "slug": "exotic-vet-alhambra",
        "title": "Exotic Vet in Alhambra, CA | Reptiles, Birds, Rabbits & Small Mammals | SPAH",
        "meta_desc": "Looking for an exotic vet in Alhambra? South Pasadena Animal Hospital treats reptiles, birds, rabbits, guinea pigs, hamsters, and other exotic pets. Call (626) 441-1314.",
        "keywords": "exotic vet Alhambra, exotic vet near me, exotic animal hospital Alhambra, exotic pet vet Los Angeles, exotic veterinarian San Gabriel Valley, reptile bird rabbit vet, small mammal vet Alhambra, exotic animal vet Pasadena, unusual pet vet near me",
        "og_title": "Exotic Vet in Alhambra, CA | Reptiles, Birds, Rabbits & More | SPAH",
        "og_desc": "South Pasadena Animal Hospital is your exotic vet in Alhambra. We treat reptiles, birds, rabbits, guinea pigs, hamsters, and other exotic pets alongside dogs and cats.",
        "breadcrumb_name": "Exotic Vet in Alhambra",
        "hero_label": "EXOTIC PET VETERINARY CARE",
        "h1": "Your Exotic Vet in Alhambra",
        "hero_desc": "Not every vet sees exotic pets — but we do. At South Pasadena Animal Hospital, our veterinarians provide knowledgeable, compassionate care for reptiles, birds, rabbits, guinea pigs, hamsters, and other non-traditional companion animals alongside our dog and cat patients. Whether your pet has scales, feathers, or fur, they'll receive the same thorough attention and gentle handling at our Alhambra clinic.",
        "why_heading": "Why Exotic Pet Owners in Alhambra Choose SPAH",
        "why_cards": [
            {
                "icon_bg": "#EDF3F0", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
                "title": "True Multi-Species Practice",
                "text": "We treat reptiles, birds, rabbits, guinea pigs, hamsters, rats, and other small mammals regularly — not as a rare afterthought, but as a core part of our practice."
            },
            {
                "icon_bg": "#F7EDE5", "icon_stroke": "#A8673A",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#A8673A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="5.5" cy="8.5" r="2.5"/><circle cx="18.5" cy="8.5" r="2.5"/><circle cx="12" cy="12" r="6"/><circle cx="10" cy="11" r="0.8" fill="#A8673A"/><circle cx="14" cy="11" r="0.8" fill="#A8673A"/></svg>',
                "title": "One Vet for All Your Pets",
                "text": "Have a dog, a cat, and a bearded dragon? You don't need three different vets. We care for every member of your household under one roof."
            },
            {
                "icon_bg": "#D6DFED", "icon_stroke": "#5A7FA6",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#5A7FA6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
                "title": "In-House Diagnostics for Exotics",
                "text": "We run bloodwork, fecal tests, X-rays, and other diagnostics on-site for all species — no waiting for outside labs when your exotic pet needs answers fast."
            },
            {
                "icon_bg": "#D4E5D9", "icon_stroke": "#7A9E8E",
                "icon_svg": '<svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="#7A9E8E" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1v22"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
                "title": "Transparent Pricing",
                "text": 'No sticker shock. Our prices are published online for complete transparency. <a href="pricing.html" class="text-brand hover:underline">View our prices</a>.'
            },
        ],
        "species_section_heading": "Exotic Pets We Treat",
        "species_list": [
            {"name": "Reptiles", "desc": "Bearded dragons, leopard geckos, ball pythons, tortoises, chameleons, blue-tongue skinks, and other lizards and snakes."},
            {"name": "Birds", "desc": "Cockatiels, parrots, conures, parakeets, finches, canaries, doves, and other companion birds."},
            {"name": "Rabbits", "desc": "Wellness exams, GI stasis treatment, RHDV2 vaccination, dental care, and spay/neuter surgery."},
            {"name": "Guinea Pigs", "desc": "Respiratory infection treatment, dental checks, bladder stone evaluation, vitamin C guidance, and parasite care."},
            {"name": "Hamsters & Gerbils", "desc": "Wellness exams, tumor screening, wet tail treatment, respiratory issues, and dental checks."},
            {"name": "Rats & Mice", "desc": "Respiratory infections (mycoplasmosis), tumor evaluation, dental care, and wellness checkups."},
        ],
        "faq_heading": "Exotic Vet FAQ — Alhambra",
        "faqs": [
            {"q": "What exotic pets does SPAH treat?", "a": "We treat reptiles (bearded dragons, geckos, snakes, turtles, tortoises, chameleons), birds (parrots, cockatiels, conures, parakeets, finches), rabbits, guinea pigs, hamsters, gerbils, rats, mice, and other small exotic companions. If you're unsure whether we see your pet, give us a call."},
            {"q": "Do exotic pets need annual vet visits?", "a": "Yes. Exotic animals are very good at hiding illness, and many health conditions (metabolic bone disease in reptiles, dental disease in rabbits, respiratory infections in guinea pigs) are much easier to treat when caught early through routine exams."},
            {"q": "How much does an exotic vet visit cost?", "a": 'Our exam fees are published on our <a href="pricing.html" class="text-brand hover:underline">pricing page</a>. We always discuss costs before proceeding with any diagnostics or treatment so there are no surprises.'},
            {"q": "What should I bring to my exotic pet's first vet visit?", "a": 'Bring your pet in an appropriate secure carrier, photos of their enclosure/habitat, a list of their diet and any supplements, and any medical records from a previous vet. This helps us assess both their health and their husbandry. Read our <a href="blog/exotic-pet-first-vet-visit.html" class="text-brand hover:underline">first visit guide</a> for more tips.'},
            {"q": "Can you treat my exotic pet if it's an emergency?", "a": "During business hours (Monday-Friday, 8AM-6PM), we can assess and stabilize urgent exotic pet cases. For after-hours emergencies, we recommend contacting an emergency exotic animal hospital. Call us first and we'll help guide you."},
        ],
        "related_blogs": [
            {"url": "blog/exotic-pet-first-vet-visit.html", "title": "What to Expect at Your Exotic Pet's First Vet Visit"},
        ],
        "seo_heading": "Your Local Exotic Animal Veterinarian in Alhambra",
        "seo_content": """<p>Finding a vet who treats exotic pets in Alhambra and the San Gabriel Valley is a real challenge. The vast majority of veterinary clinics in the area focus exclusively on dogs and cats, leaving owners of reptiles, birds, rabbits, guinea pigs, and other small mammals with few options nearby. South Pasadena Animal Hospital at 3116 West Main Street in Alhambra is proud to be one of the few local clinics that welcomes exotic pets as a regular part of our practice.</p>

        <p>Exotic animal medicine is fundamentally different from dog and cat medicine. Each species has unique anatomical features, metabolic processes, dietary requirements, and disease vulnerabilities that require knowledge and hands-on experience to manage properly. Our veterinarians treat exotic pets regularly and stay current with the latest advances in reptile, avian, and small mammal medicine. Whether your bearded dragon has stopped eating, your parrot is plucking feathers, your rabbit is in GI stasis, or your guinea pig is sneezing, we have the experience and diagnostic tools to help.</p>

        <p>Our in-house laboratory and imaging capabilities mean we can run species-appropriate bloodwork, perform digital X-rays, conduct fecal parasite screenings, and analyze samples without sending them to an outside lab. This is especially critical for exotic pets, who can deteriorate quickly once symptoms are visible. We also provide <a href="services.html" class="text-brand hover:underline">surgical services</a> for exotic animals, including mass removals, spay/neuter for rabbits, and other soft tissue procedures.</p>

        <p>Exotic pet owners travel to SPAH from across the region — <a href="vet-alhambra.html" class="text-brand hover:underline">Alhambra</a>, Pasadena, <a href="vet-south-pasadena.html" class="text-brand hover:underline">South Pasadena</a>, <a href="vet-san-gabriel.html" class="text-brand hover:underline">San Gabriel</a>, <a href="vet-monterey-park.html" class="text-brand hover:underline">Monterey Park</a>, <a href="vet-rosemead.html" class="text-brand hover:underline">Rosemead</a>, Arcadia, Temple City, <a href="vet-highland-park.html" class="text-brand hover:underline">Highland Park</a>, and beyond — because quality exotic veterinary care simply is not available at most local clinics. If you have an exotic pet that needs a vet who understands their needs, <a href="contact.html" class="text-brand hover:underline">contact us</a> to schedule an appointment.</p>""",
        "cta_heading": "Ready to Book an Exotic Pet Exam?",
    },
]


# ─── HTML Template Builder ───────────────────────────────────────────

def build_page(sp):
    """Build a full species landing page from a species dict."""

    # Build why cards HTML
    why_cards_html = ""
    for c in sp["why_cards"]:
        why_cards_html += f'''
        <div class="bg-white rounded-2xl p-6 card-shadow">
          <div class="w-12 h-12 rounded-full flex items-center justify-center mb-4" style="background:{c['icon_bg']};">
            {c['icon_svg']}
          </div>
          <h3 class="font-display text-xl font-bold text-dark mb-2">{c['title']}</h3>
          <p class="font-body text-muted text-sm" style="line-height:1.7;">{c['text']}</p>
        </div>'''

    # Build species list HTML
    species_list_html = ""
    for s in sp["species_list"]:
        species_list_html += f'''
        <div class="bg-white rounded-2xl p-6 card-shadow">
          <h3 class="font-display text-lg font-bold text-dark mb-2">{s['name']}</h3>
          <p class="font-body text-muted text-sm" style="line-height:1.7;">{s['desc']}</p>
        </div>'''

    # Build FAQ HTML + schema
    faq_html = ""
    faq_schema_items = []
    for i, faq in enumerate(sp["faqs"]):
        faq_html += f'''
        <div class="bg-white rounded-2xl p-6 card-shadow">
          <h3 class="font-display text-lg font-bold text-dark mb-2">{faq['q']}</h3>
          <p class="font-body text-muted text-sm" style="line-height:1.7;">{faq['a']}</p>
        </div>'''
        # Strip HTML from FAQ answers for schema
        import re
        clean_a = re.sub(r'<[^>]+>', '', faq['a'])
        comma = "," if i < len(sp["faqs"]) - 1 else ""
        faq_schema_items.append(f'''      {{
        "@type": "Question",
        "name": "{faq['q']}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{clean_a}"
        }}
      }}{comma}''')

    faq_schema = ",\n".join(faq_schema_items)

    # Build related blog links
    blog_links_html = ""
    if sp.get("related_blogs"):
        blog_links_html = '\n  <section class="py-12 bg-white">\n    <div class="max-w-3xl mx-auto px-6 text-center">\n      <h2 class="font-display text-2xl font-bold text-dark mb-6">Related Articles</h2>\n'
        for blog in sp["related_blogs"]:
            blog_links_html += f'      <a href="{blog["url"]}" class="text-brand font-body font-bold hover:underline">{blog["title"]} &rarr;</a><br/>\n'
        blog_links_html += '    </div>\n  </section>\n'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/png" href="images/spah-logo.png" />
  <title>{sp['title']}</title>
  <meta name="description" content="{sp['meta_desc']}" />
  <meta name="keywords" content="{sp['keywords']}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://www.spah.la/{sp['slug']}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{sp['og_title']}" />
  <meta property="og:description" content="{sp['og_desc']}" />
  <meta property="og:url" content="https://www.spah.la/{sp['slug']}" />
  <meta property="og:site_name" content="South Pasadena Animal Hospital" />
  <meta property="og:image" content="https://www.spah.la/images/spah-logo.png" />
  <meta property="og:image:width" content="512" />
  <meta property="og:image:height" content="512" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{sp['title']}" />
  <meta name="twitter:description" content="{sp['meta_desc']}" />
  <meta name="twitter:image" content="https://www.spah.la/images/spah-logo.png" />
  <!-- BreadcrumbList -->
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.spah.la/"}},{{"@type":"ListItem","position":2,"name":"Services","item":"https://www.spah.la/services"}},{{"@type":"ListItem","position":3,"name":"{sp['breadcrumb_name']}","item":"https://www.spah.la/{sp['slug']}"}}]}}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "VeterinaryCare",
    "name": "South Pasadena Animal Hospital",
    "url": "https://www.spah.la",
    "telephone": "+16264411314",
    "email": "info@spah.la",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "3116 W Main St",
      "addressLocality": "Alhambra",
      "addressRegion": "CA",
      "postalCode": "91801",
      "addressCountry": "US"
    }},
    "geo": {{
      "@type": "GeoCoordinates",
      "latitude": 34.1161,
      "longitude": -118.1500
    }},
    "areaServed": [
      {{ "@type": "City", "name": "Alhambra" }},
      {{ "@type": "City", "name": "South Pasadena" }},
      {{ "@type": "City", "name": "Pasadena" }},
      {{ "@type": "City", "name": "San Gabriel" }},
      {{ "@type": "City", "name": "Monterey Park" }},
      {{ "@type": "City", "name": "Highland Park" }}
    ],
    "openingHoursSpecification": [
      {{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"],
        "opens": "08:00",
        "closes": "18:00"
      }}
    ],
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "126",
      "bestRating": "5",
      "worstRating": "1"
    }},
    "priceRange": "$$",
    "sameAs": ["https://www.instagram.com/southpasah/"]
  }}
  </script>
  <link rel="stylesheet" href="css/styles.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet" />
{INLINE_STYLES}
</head>
<body>

{NOTICE_BANNER}

{NAV}

  <!-- HERO -->
  <section class="py-20 text-center relative overflow-hidden" style="background: linear-gradient(135deg, #EFF4F9 0%, #EDF3F0 100%);">
    <div style="position:absolute;top:-60px;left:50%;transform:translateX(-50%);width:600px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(122,158,142,0.12) 0%,transparent 70%);pointer-events:none;"></div>
    <div class="relative z-10 max-w-3xl mx-auto px-6">
      <span class="text-sage font-body text-xs font-bold tracking-widest uppercase">{sp['hero_label']}</span>
      <h1 class="font-display text-2xl sm:text-4xl md:text-5xl font-bold text-dark mt-3" style="letter-spacing:-0.03em;">{sp['h1']}</h1>
      <p class="font-body text-muted text-lg mt-5 max-w-2xl mx-auto" style="line-height:1.7;">
        {sp['hero_desc']}
      </p>
      <div class="flex flex-wrap gap-4 justify-center mt-8">
        <a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank"
           class="btn-primary">Book an Appointment</a>
        <a href="tel:6264411314" class="border-2 border-brand/40 text-brand font-body font-bold rounded-full px-8 py-3 hover:bg-brand/5 transition-colors duration-200">Call (626) 441-1314</a>
      </div>
    </div>
  </section>

  <!-- WHY CHOOSE SPAH -->
  <section class="py-20 bg-warm">
    <div class="max-w-5xl mx-auto px-6">
      <h2 class="font-display text-3xl font-bold text-dark text-center mb-12" style="letter-spacing:-0.02em;">{sp['why_heading']}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{why_cards_html}
      </div>
    </div>
  </section>

  <!-- CLINIC PHOTO -->
  <section class="py-8 bg-warm">
    <div class="max-w-5xl mx-auto px-6">
      <div class="rounded-2xl overflow-hidden my-8">
        <img src="images/spah-clinic-aerial.jpg" alt="South Pasadena Animal Hospital veterinary clinic on Main Street in Alhambra, CA" class="w-full" loading="lazy" />
      </div>
    </div>
  </section>

  <!-- SPECIES / SERVICES LIST -->
  <section class="py-20" style="background: linear-gradient(180deg, #EFF4F9 0%, #FAFAF8 100%);">
    <div class="max-w-5xl mx-auto px-6">
      <h2 class="font-display text-3xl font-bold text-dark text-center mb-12" style="letter-spacing:-0.02em;">{sp['species_section_heading']}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{species_list_html}
      </div>
      <div class="text-center mt-10">
        <a href="services.html" class="text-brand font-body font-bold hover:underline transition-colors duration-200">View All Services &rarr;</a>
      </div>
    </div>
  </section>

  <!-- LOCATION -->
  <section class="py-20 bg-warm">
    <div class="max-w-5xl mx-auto px-6">
      <h2 class="font-display text-3xl font-bold text-dark text-center mb-6" style="letter-spacing:-0.02em;">Conveniently Located on Main Street</h2>
      <p class="font-body text-muted text-lg text-center max-w-2xl mx-auto mb-10" style="line-height:1.7;">
        Visit us at 3116 W Main St in Alhambra, just west of the Fremont Avenue intersection. Easy street parking is available right out front.
      </p>
      <div class="mb-8">
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3302.5!2d-118.15!3d34.0881!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x80c2c5a78f18df43%3A0x937fc9c6ac0f1e94!2sSouth%20Pasadena%20Animal%20Hospital!5e0!3m2!1sen!2sus!4v1" width="100%" height="300" style="border:0;border-radius:16px;" allowfullscreen loading="lazy" title="SPAH location in Alhambra"></iframe>
      </div>
      <div class="bg-white rounded-2xl p-6 card-shadow max-w-md mx-auto text-center">
        <h3 class="font-display text-xl font-bold text-dark mb-3">Hours</h3>
        <div class="font-body text-muted text-sm space-y-1" style="line-height:1.7;">
          <p><span class="font-bold text-dark">Monday &ndash; Friday:</span> 8:00 AM &ndash; 1:00 PM &amp; 2:00 PM &ndash; 6:00 PM</p>
          <p><span class="font-bold text-dark">Saturday &ndash; Sunday:</span> Closed</p>
        </div>
      </div>
    </div>
  </section>

{blog_links_html}
  <!-- FAQ -->
  <section class="py-20" style="background: linear-gradient(180deg, #EFF4F9 0%, #FAFAF8 100%);">
    <div class="max-w-3xl mx-auto px-6">
      <h2 class="font-display text-3xl font-bold text-dark text-center mb-10" style="letter-spacing:-0.02em;">{sp['faq_heading']}</h2>
      <div class="space-y-6">{faq_html}
      </div>
    </div>
  </section>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{faq_schema}
    ]
  }}
  </script>

  <!-- CTA -->
  <section class="py-16 text-center" style="background: linear-gradient(135deg, #5A7FA6 0%, #7A9E8E 100%);">
    <div class="max-w-2xl mx-auto px-6 text-white">
      <h2 class="font-display text-3xl font-bold mb-4">{sp['cta_heading']}</h2>
      <p class="font-body text-white/80 mb-8" style="line-height:1.7;">Schedule your pet's appointment online in under a minute, or give us a call and our team will find a time that works for you.</p>
      <div class="flex flex-wrap gap-4 justify-center">
        <a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank"
           class="bg-white text-brand font-body font-bold rounded-full px-8 py-3 hover:bg-warm transition-colors duration-200">Book Online</a>
        <a href="tel:6264411314" class="border-2 border-white/50 text-white font-body font-bold rounded-full px-8 py-3 hover:bg-white/10 transition-colors duration-200">(626) 441-1314</a>
      </div>
    </div>
  </section>

  <!-- LOCAL SEO CONTENT -->
  <section class="py-10 border-t border-gray-50">
    <div class="max-w-4xl mx-auto px-6">
      <h2 class="font-display text-xl font-bold text-dark/50 mb-6">{sp['seo_heading']}</h2>
      <div class="font-body text-xs text-dark/40 space-y-4" style="line-height:1.9;">
        {sp['seo_content']}
      </div>
    </div>
  </section>

{FOOTER}

{MOBILE_JS}
{STICKY_CTA}
{USERWAY}
</body>
</html>'''

    return html


# ─── Generate All Pages ──────────────────────────────────────────────

for sp in species_pages:
    html = build_page(sp)
    filepath = os.path.join(OUTPUT_DIR, sp["file"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Created: {sp['file']}")

print(f"\nDone! Generated {len(species_pages)} species landing pages.")
