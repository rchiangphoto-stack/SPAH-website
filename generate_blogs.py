"""Generate blog posts 2-5 for SPAH website."""
import os

BLOG_DIR = r"C:\Users\rchia\Documents\SPAH-website\blog"

# Shared template parts
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

def blog_schema(headline, desc, url):
    return f"""  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BlogPosting","headline":"{headline}","description":"{desc}","datePublished":"2026-03-31","dateModified":"2026-03-31","author":{{"@type":"Organization","name":"South Pasadena Animal Hospital","url":"https://www.spah.la"}},"publisher":{{"@type":"Organization","name":"South Pasadena Animal Hospital","url":"https://www.spah.la","logo":{{"@type":"ImageObject","url":"https://www.spah.la/images/spah-logo.png"}}}},"mainEntityOfPage":"{url}"}}
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
        <a href="index.html" class="nav-link text-brand font-body font-bold text-sm tracking-wide">BLOG</a>
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
      <a href="index.html" class="text-brand font-body font-bold text-sm tracking-wide py-3">BLOG</a>
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
              <a href="index.html" class="font-body text-brand font-bold text-sm">Blog</a>
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
        <a href="../contact.html" class="font-body text-dark/60 text-xs hover:text-dark transition-colors duration-200">Privacy Policy</a>
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

def cta_section(heading, desc, btn_text):
    return f"""  <section class="py-16 text-center" style="background:linear-gradient(135deg,#5A7FA6,#7A9E8E);">
    <div class="max-w-2xl mx-auto px-6 text-white">
      <h2 class="font-display text-3xl font-bold mb-4">{heading}</h2>
      <p class="font-body text-white/80 text-lg mb-6" style="line-height:1.7;">{desc}</p>
      <div class="flex flex-wrap gap-4 justify-center">
        <a href="https://southpasah.usw2.ezyvet.com/external/portal/main/login?id=2" target="_blank" class="bg-white text-brand font-body font-bold rounded-full px-8 py-3 hover:bg-warm transition-colors duration-200">{btn_text}</a>
        <a href="tel:6264411314" class="border-2 border-white/50 text-white font-body font-bold rounded-full px-8 py-3 hover:bg-white/10 transition-colors duration-200">(626) 441-1314</a>
      </div>
    </div>
  </section>"""

# ============================================================
# BLOG 2: Guinea Pig Sneezing
# ============================================================
blog2_content = """
      <p>Guinea pigs sneeze. It's a normal part of being a guinea pig. A little &ldquo;achoo&rdquo; after sniffing some hay dust or encountering a new scent is nothing to worry about. But when sneezing becomes frequent &mdash; or comes with other symptoms like discharge or appetite changes &mdash; it could be a sign of an upper respiratory infection. And in guinea pigs, URIs can become serious fast.</p>
      <p>Here's how to tell the difference between a normal sneeze and something that needs a vet visit.</p>

      <h2>Why Guinea Pigs Sneeze (Perfectly Normal Reasons)</h2>
      <ul>
        <li><strong>Dust from hay or bedding</strong> &mdash; especially dusty timothy hay or wood shavings</li>
        <li><strong>New cleaning products</strong> or strong scents nearby (candles, air fresheners, perfume)</li>
        <li><strong>Dry air</strong> from air conditioning or heaters</li>
        <li><strong>Occasional irritant</strong> &mdash; just like humans sneeze sometimes for no reason</li>
      </ul>
      <p><strong>Key point:</strong> Occasional sneezing with no other symptoms is usually nothing to worry about. If your guinea pig sneezes a few times, eats normally, and acts like their usual self, they're most likely fine.</p>

      <h2>Signs of an Upper Respiratory Infection (URI)</h2>
      <p>When sneezing is more than just sneezing, you'll typically notice additional symptoms:</p>
      <ul>
        <li><strong>Frequent sneezing</strong> &mdash; multiple times per hour or throughout the day</li>
        <li><strong>Nasal discharge</strong> &mdash; clear at first, may turn thick, white, yellow, or green</li>
        <li><strong>Crusty or watery eyes</strong></li>
        <li><strong>Audible breathing</strong> &mdash; clicking, wheezing, or crackling sounds</li>
        <li><strong>Loss of appetite or weight loss</strong></li>
        <li><strong>Lethargy</strong> &mdash; less active, hiding more, not wheek-ing for food</li>
        <li><strong>Puffed-up or hunched posture</strong></li>
      </ul>
      <p>If you notice <strong>any combination</strong> of these, schedule a vet visit. URIs in guinea pigs can progress to pneumonia within days.</p>

      <h2>What Causes Respiratory Infections in Guinea Pigs?</h2>
      <ul>
        <li><strong>Bacterial infections:</strong> <em>Bordetella bronchiseptica</em> and <em>Streptococcus pneumoniae</em> are the most common culprits</li>
        <li><strong>Poor ventilation</strong> in the cage or enclosure</li>
        <li><strong>Cold or drafty environments</strong> (below 65&deg;F)</li>
        <li><strong>Stress</strong> from overcrowding, new cage mates, or environmental changes</li>
        <li><strong>Vitamin C deficiency</strong> &mdash; guinea pigs cannot produce their own vitamin C, and a deficiency weakens their immune system</li>
        <li><strong>Exposure to sick animals</strong></li>
      </ul>
      <p><strong>Important note:</strong> Bordetella can be transmitted from rabbits to guinea pigs. If you house them together, be aware of this cross-species infection risk.</p>

      <h2>Can a Guinea Pig URI Be Fatal?</h2>
      <p>Yes. Untreated upper respiratory infections can progress to pneumonia, which can be fatal in guinea pigs. Because guinea pigs are prey animals, they instinctively hide illness until they're very sick. By the time symptoms are obvious, the infection may already be advanced.</p>
      <p>Early treatment with appropriate antibiotics dramatically improves outcomes. This is why we always recommend seeing a vet sooner rather than later when respiratory symptoms appear.</p>

      <h2>How Vets Diagnose and Treat Guinea Pig URIs</h2>
      <ul>
        <li><strong>Physical exam:</strong> listening to lungs with a stethoscope, checking discharge, body weight</li>
        <li><strong>Culture and sensitivity testing</strong> may be recommended for severe or recurring infections</li>
        <li><strong>Treatment typically includes:</strong> antibiotics safe for guinea pigs, anti-inflammatories for comfort, nebulization in severe cases, supportive care (fluids, syringe feeding if not eating)</li>
      </ul>
      <p><strong>Critical safety note:</strong> Some antibiotics that are safe for dogs and cats can be <strong>fatal</strong> to guinea pigs. Certain classes of antibiotics disrupt the delicate gut flora that guinea pigs depend on. Never use leftover medications from another pet. Always see a vet who is experienced with guinea pigs.</p>
      <p>At <a href="../about.html">SPAH</a>, we regularly treat guinea pigs and know which medications are safe for them.</p>

      <h2>Preventing Respiratory Infections</h2>
      <ul>
        <li><strong>Use dust-free bedding</strong> &mdash; paper-based bedding like Carefresh is ideal. Avoid cedar and pine shavings (the oils irritate respiratory passages).</li>
        <li><strong>Keep the cage clean</strong> &mdash; spot clean daily, full bedding change weekly</li>
        <li><strong>Ensure good ventilation</strong> without direct drafts</li>
        <li><strong>Maintain room temperature</strong> between 65&ndash;75&deg;F</li>
        <li><strong>Provide daily vitamin C</strong> &mdash; bell peppers, leafy greens, or a supplement. Don't rely on vitamin C drops in water &mdash; they degrade within hours.</li>
        <li><strong>Quarantine new guinea pigs</strong> for 2&ndash;3 weeks before introducing them to existing pets</li>
        <li><strong>Avoid housing guinea pigs with rabbits</strong> (Bordetella risk)</li>
        <li><strong>Annual <a href="../services.html">wellness exams</a></strong> help catch issues early</li>
      </ul>

      <h2>When to Call the Vet</h2>
      <p>Call or book an appointment if your guinea pig has:</p>
      <ul>
        <li>Sneezing plus any discharge (nose or eyes)</li>
        <li>Audible breathing sounds (clicking, wheezing, crackling)</li>
        <li>Not eaten for more than 12 hours (guinea pigs need to eat continuously &mdash; GI slowdown is also a risk)</li>
        <li>Rapid weight loss</li>
        <li>Significant behavior change (hiding, not responding to treats)</li>
      </ul>
      <p>When in doubt, it's always better to check. A quick exam can either catch something early or give you peace of mind. Check our <a href="../pricing.html">pricing page</a> for transparent exam costs.</p>

      <p>Guinea pigs are wonderful pets, but they need an owner who knows what to watch for. A sneeze here and there is just part of guinea pig life. But changes in frequency, appetite, or energy should always be taken seriously. At South Pasadena Animal Hospital in Alhambra, we see guinea pigs and other small mammals and are always happy to help if something seems off.</p>"""

blog2_related = related_card("signs-bearded-dragon-needs-vet.html", "#E8F5E9,#C8E6C9", "&#129422;", "tag-reptile", "Reptile Care", "Signs Your Bearded Dragon Needs a Vet") + "\n" + related_card("rabbit-gi-stasis.html", "#F3E5F5,#E1BEE7", "&#128048;", "tag-rabbit", "Rabbit Care", "Rabbit GI Stasis: Symptoms &amp; Treatment")

# ============================================================
# BLOG 3: Rabbit GI Stasis
# ============================================================
blog3_content = """
      <p>GI stasis is one of the most common &mdash; and most dangerous &mdash; conditions in pet rabbits. When a rabbit's digestive system slows down or stops, it can become life-threatening within 24 to 48 hours. The good news: if caught early, GI stasis is very treatable. And with the right diet and care, it's largely preventable.</p>

      <h2>What Is GI Stasis?</h2>
      <p>Gastrointestinal stasis is the slowing or complete stoppage of the digestive system. When motility decreases, food and gas build up in the stomach and intestines. Harmful bacteria begin to overgrow, producing painful gas and potentially releasing toxins into the bloodstream.</p>
      <p>The rabbit stops eating because of the discomfort, which makes everything worse &mdash; creating a dangerous downward cycle. In veterinary terms, this condition is also called &ldquo;ileus.&rdquo;</p>

      <h2>What Causes GI Stasis?</h2>
      <ul>
        <li><strong>Not enough fiber (hay)</strong> &mdash; this is the #1 cause. Rabbits need unlimited hay to keep the gut moving.</li>
        <li><strong>Dehydration</strong> &mdash; not drinking enough water</li>
        <li><strong>Stress</strong> &mdash; new environments, bonding issues, loud noises, predator exposure (even a dog barking nearby)</li>
        <li><strong>Pain from another condition</strong> &mdash; dental disease, urinary issues, arthritis</li>
        <li><strong>Sudden diet changes</strong></li>
        <li><strong>Lack of exercise</strong> &mdash; rabbits in small cages are more prone</li>
        <li><strong>Post-surgery recovery</strong></li>
        <li><strong>Secondary to other illnesses</strong></li>
      </ul>

      <h2>Symptoms to Watch For</h2>
      <ul>
        <li><strong>Not eating</strong> &mdash; the most important early sign. Even a few hours of not eating is significant for rabbits.</li>
        <li><strong>Small, dry, or misshapen droppings</strong> &mdash; or no droppings at all</li>
        <li><strong>Hunched posture</strong> &mdash; sitting in a &ldquo;loaf&rdquo; position with eyes partially closed</li>
        <li><strong>Teeth grinding (bruxism)</strong> &mdash; a sign of pain in rabbits (different from gentle tooth purring, which indicates contentment)</li>
        <li><strong>Bloated or tense belly</strong></li>
        <li><strong>Lethargy</strong> &mdash; not moving, not responding to favorite treats</li>
        <li><strong>Pressing belly to cool surfaces</strong> &mdash; trying to relieve discomfort</li>
      </ul>
      <p><strong>Important:</strong> Rabbits are prey animals and hide pain instinctively. If your rabbit is showing ANY of these signs, take it seriously. Don't wait to see if it resolves on its own.</p>

      <h2>Why GI Stasis Is an Emergency</h2>
      <p>A rabbit's digestive system is designed to be constantly moving. When it stops:</p>
      <ul>
        <li>Bacteria multiply rapidly, producing dangerous toxins</li>
        <li>Gas buildup causes severe pain, which causes the rabbit to stop eating, which worsens the stasis</li>
        <li>Liver damage (hepatic lipidosis) can begin within 24 hours if the rabbit isn't eating</li>
        <li>Without treatment, GI stasis can be fatal in 24&ndash;48 hours</li>
      </ul>
      <p>This is <strong>not</strong> a &ldquo;wait and see&rdquo; situation. If your rabbit hasn't eaten in 12 hours and is showing other symptoms, call a vet. You can reach us at <a href="tel:6264411314">(626) 441-1314</a>.</p>

      <h2>How Vets Treat GI Stasis</h2>
      <ul>
        <li><strong>Fluid therapy</strong> (subcutaneous or IV) to rehydrate and get the gut moving</li>
        <li><strong>Pain management</strong> &mdash; critical, because pain causes the rabbit to stop eating</li>
        <li><strong>Gut motility drugs</strong> (like cisapride or metoclopramide) to restart digestive movement</li>
        <li><strong>Syringe feeding</strong> with Critical Care or similar recovery food to keep calories and fiber coming in</li>
        <li><strong>Simethicone</strong> for gas relief</li>
        <li><strong>X-rays or ultrasound</strong> to check for true blockages (which require different treatment than stasis)</li>
        <li><strong>Gentle abdominal massage</strong> &mdash; your vet can show you how to do this at home</li>
      </ul>
      <p>In most cases, with prompt treatment, rabbits recover well. Treatment is much more straightforward &mdash; and less expensive &mdash; when caught early. See our <a href="../pricing.html">pricing page</a> for transparent costs.</p>

      <h2>Prevention: Diet Is Everything</h2>
      <p>The vast majority of GI stasis cases are preventable with proper diet and care:</p>
      <ul>
        <li><strong>Unlimited grass hay</strong> &mdash; timothy hay for adults, alfalfa for babies under 6 months. Hay should make up 80%+ of the diet.</li>
        <li><strong>Fresh leafy greens daily</strong> &mdash; romaine, cilantro, parsley, basil (about 1 cup per 2 lbs body weight)</li>
        <li><strong>Limited pellets</strong> &mdash; &frac14; cup per 5 lbs body weight for adults. Many rabbit owners overfeed pellets, which reduces hay consumption.</li>
        <li><strong>Fresh water always available</strong> &mdash; bowls are preferred over bottles (rabbits drink more from bowls)</li>
        <li><strong>Avoid</strong> sugary treats, seeds, nuts, cereal, bread, and yogurt drops</li>
        <li><strong>Exercise</strong> &mdash; at least 3&ndash;4 hours of free-roam time daily</li>
        <li><strong>Reduce stress</strong> where possible</li>
        <li><strong>Regular <a href="../services.html">vet checkups</a></strong> &mdash; dental problems are a common hidden cause of GI stasis, and we can catch them during a wellness exam</li>
      </ul>

      <h2>A Note About RHDV2</h2>
      <p>While we're discussing rabbit health: Rabbit Hemorrhagic Disease Virus 2 (RHDV2) is a highly contagious, often fatal virus that has been confirmed in California. It spreads through direct contact, insects, or contaminated surfaces &mdash; and even indoor rabbits can be at risk.</p>
      <p>There is a vaccine available. At SPAH, we can discuss whether the RHDV2 vaccine is appropriate for your rabbit during a wellness visit. It's a conversation worth having, especially for rabbits in Southern California.</p>

      <p>GI stasis is scary, but it's also one of the most preventable conditions in pet rabbits. A hay-heavy diet, plenty of water, daily exercise, and regular vet visits go a long way. If your rabbit stops eating or shows signs of discomfort, don't wait. At <a href="../about.html">South Pasadena Animal Hospital</a> in Alhambra, we see rabbits regularly and are ready to help.</p>"""

blog3_related = related_card("guinea-pig-sneezing.html", "#FFF3E0,#FFE0B2", "&#128057;", "tag-small-mammal", "Small Mammal", "Guinea Pig Sneezing: When to Worry") + "\n" + related_card("bird-feather-plucking.html", "#E3F2FD,#BBDEFB", "&#129436;", "tag-bird", "Bird Care", "Why Is My Bird Pulling Out Feathers?")

# ============================================================
# BLOG 4: Bird Feather Plucking
# ============================================================
blog4_content = """
      <p>Feather plucking &mdash; also called feather destructive behavior (FDB) &mdash; is one of the most common reasons bird owners bring their pets to a vet. If your parrot, cockatoo, African grey, or other pet bird is pulling out its own feathers, it's a sign that something isn't right. The challenge is figuring out whether the cause is medical, behavioral, or both.</p>
      <p>At <a href="../about.html">South Pasadena Animal Hospital</a>, we see birds regularly and take a thorough approach to identifying the root cause. Here's what you need to know.</p>

      <h2>Understanding Feather Plucking</h2>
      <ul>
        <li>Ranges from mild (barbering feather tips) to severe (plucking down to bare skin or self-mutilation)</li>
        <li>More common in certain species: African greys, cockatoos, macaws, eclectus parrots, and Quaker parrots</li>
        <li>Can start suddenly or develop gradually over weeks or months</li>
        <li>Feather plucking is a <strong>symptom</strong>, not a diagnosis &mdash; the first step is always identifying the underlying cause</li>
      </ul>

      <h2>Medical Causes (Rule These Out First)</h2>
      <p>Before assuming feather plucking is behavioral, it's critical to rule out medical causes. Many plucking birds we see have a medical component that, once treated, significantly reduces the behavior.</p>
      <ul>
        <li><strong>Skin infections</strong> (bacterial, fungal, or yeast)</li>
        <li><strong>External parasites</strong> (mites, lice &mdash; less common in indoor birds but possible)</li>
        <li><strong>Allergies</strong> (food or environmental)</li>
        <li><strong>Nutritional deficiency</strong> &mdash; especially vitamin A, calcium, or amino acids from an all-seed diet</li>
        <li><strong>Liver or kidney disease</strong> &mdash; can cause skin irritation and feather quality changes</li>
        <li><strong>Heavy metal toxicity</strong> (zinc from cage hardware, lead from paint or curtain weights)</li>
        <li><strong>Thyroid issues</strong> (especially in budgies and parakeets)</li>
        <li><strong>Psittacine Beak and Feather Disease (PBFD)</strong> &mdash; a viral condition causing progressive feather loss</li>
        <li><strong>Pain from any source</strong> &mdash; birds may pluck over an area that hurts</li>
      </ul>
      <p>A vet exam with bloodwork can help identify or rule out these causes quickly.</p>

      <h2>Behavioral Causes</h2>
      <ul>
        <li><strong>Boredom / lack of stimulation</strong> &mdash; parrots are highly intelligent and need daily mental enrichment</li>
        <li><strong>Stress</strong> &mdash; changes in environment, new people, construction noise, moved cage location</li>
        <li><strong>Loneliness</strong> &mdash; too much time alone. Parrots are flock animals.</li>
        <li><strong>Sexual frustration / hormonal behavior</strong> &mdash; especially during breeding season</li>
        <li><strong>Sleep deprivation</strong> &mdash; birds need 10&ndash;12 hours of quiet, dark sleep per night</li>
        <li><strong>Fear</strong> &mdash; of objects, sounds, other pets, or even a new toy</li>
        <li><strong>Learned behavior</strong> &mdash; sometimes plucking starts for a medical reason and continues as a habit after the medical issue resolves</li>
        <li><strong>Over-bonding</strong> with one person (especially common in cockatoos)</li>
      </ul>

      <h2>Species Most Commonly Affected</h2>
      <ul>
        <li><strong>African Grey Parrots</strong> &mdash; highly intelligent but prone to anxiety and over-bonding</li>
        <li><strong>Cockatoos</strong> &mdash; extremely social and emotionally demanding; pluck when they don't get enough attention</li>
        <li><strong>Macaws</strong> &mdash; need significant space and enrichment</li>
        <li><strong>Eclectus Parrots</strong> &mdash; particularly sensitive to dietary issues; an all-seed diet almost always leads to problems</li>
        <li><strong>Quaker Parrots</strong> &mdash; hormonal plucking is common</li>
        <li><strong>Cockatiels and budgies</strong> can also pluck, though it's less common</li>
      </ul>

      <h2>What Happens During a Vet Visit for Feather Plucking</h2>
      <ul>
        <li><strong>Full physical exam</strong> &mdash; checking skin, remaining feathers, body condition, weight</li>
        <li><strong>Discussion</strong> of diet, environment, sleep schedule, social interaction, and any recent changes</li>
        <li><strong>Blood tests</strong> &mdash; complete blood count (CBC) and chemistry panel to check organ function</li>
        <li><strong>Skin scraping or culture</strong> if infection is suspected</li>
        <li><strong>Gram stain</strong> of choana (throat) and vent to check for bacterial or yeast imbalances</li>
        <li><strong>X-rays</strong> if organ disease is suspected</li>
      </ul>
      <p>The goal is always to rule out medical causes first, then address behavioral factors. At SPAH, we take a thorough approach because the answer is often a combination of both.</p>

      <h2>Treatment Options</h2>
      <ul>
        <li><strong>For medical causes:</strong> appropriate medication (antibiotics, antifungals, anti-parasitic), dietary correction, supplementation</li>
        <li><strong>Diet overhaul:</strong> converting from seed-based to pellet-based diet with fresh vegetables and fruits. This alone can dramatically improve feather quality.</li>
        <li><strong>Environmental enrichment:</strong> foraging toys, puzzle feeders, rotating toys weekly, safe chewing materials (natural wood, paper, palm leaves)</li>
        <li><strong>Sleep schedule:</strong> 10&ndash;12 hours of uninterrupted darkness every night. Cover the cage in a quiet room.</li>
        <li><strong>More socialization:</strong> increased interaction time. Consider whether a second bird might help (this isn't always the answer, though).</li>
        <li><strong>Protective collar:</strong> in severe self-mutilation cases, a collar or vest may be needed temporarily while addressing underlying causes</li>
        <li><strong>Behavior modification:</strong> positive reinforcement when NOT plucking; avoid reacting to plucking behavior</li>
      </ul>
      <p><strong>Note:</strong> Feather plucking that has gone on for years may have caused permanent follicle damage. Feathers may not fully regrow even after the cause is addressed. Early intervention leads to the best outcomes.</p>

      <h2>What NOT to Do</h2>
      <ul>
        <li><strong>Don't spray bitter apple</strong> or deterrents on feathers &mdash; it doesn't address the cause and can increase stress</li>
        <li><strong>Don't yell or punish</strong> your bird for plucking &mdash; negative attention is still attention and can reinforce the behavior</li>
        <li><strong>Don't assume it's &ldquo;just behavioral&rdquo;</strong> without a vet exam &mdash; many plucking birds have an underlying medical issue</li>
        <li><strong>Don't wait months</strong> hoping it resolves on its own &mdash; early treatment makes a real difference</li>
      </ul>

      <p>Feather plucking can be frustrating, but with the right approach &mdash; starting with a vet exam, then addressing diet, environment, and enrichment &mdash; many birds improve significantly. At South Pasadena Animal Hospital in Alhambra, we see birds of all kinds and are happy to help figure out what's going on with your feathered friend. Check our <a href="../pricing.html">pricing page</a> for transparent exam costs.</p>"""

blog4_related = related_card("exotic-pet-first-vet-visit.html", "#FCE4EC,#F8BBD0", "&#129446;", "tag-exotic", "Exotic Pets", "Your Exotic Pet's First Vet Visit") + "\n" + related_card("signs-bearded-dragon-needs-vet.html", "#E8F5E9,#C8E6C9", "&#129422;", "tag-reptile", "Reptile Care", "Signs Your Bearded Dragon Needs a Vet")

# ============================================================
# BLOG 5: Exotic Pet First Vet Visit
# ============================================================
blog5_content = """
      <p>Congratulations on your new pet! Whether you just brought home a bearded dragon, a guinea pig, a rabbit, a parrot, or a ball python, one of the most important things you can do is schedule a wellness exam within the first 1&ndash;2 weeks.</p>
      <p>Even if your new pet looks perfectly healthy, exotic animals are very good at hiding illness. Many arrive from pet stores or breeders with undetected parasites or infections. Here's a complete walkthrough of what to expect so you can feel prepared.</p>

      <h2>Why the First Vet Visit Matters</h2>
      <ul>
        <li>Many exotic pets from pet stores have parasites, respiratory infections, or nutritional deficiencies that aren't visible yet</li>
        <li>An initial exam creates a <strong>baseline</strong> for your pet's health &mdash; weight, body condition, organ function</li>
        <li>Your vet can review your husbandry setup (cage, lighting, diet) and catch common mistakes before they cause problems</li>
        <li>Prevention is always easier and less expensive than treating a sick pet later</li>
      </ul>
      <p>Think of it like a new-car inspection: everything might be fine, but you want to know for sure.</p>

      <h2>How to Choose a Vet for Your Exotic Pet</h2>
      <p>Not all veterinary clinics see exotic animals. Before booking, call ahead and ask:</p>
      <ul>
        <li>&ldquo;Do you see [your species] regularly?&rdquo;</li>
        <li>&ldquo;Do you have diagnostic equipment for exotic pets?&rdquo;</li>
        <li>&ldquo;What is the cost of an initial exam?&rdquo;</li>
      </ul>
      <p>At SPAH, we see reptiles, birds, rabbits, guinea pigs, hamsters, and other small mammals. Our vets have extensive experience with exotic animals and we have the diagnostic equipment to properly evaluate them. See our <a href="../pricing.html">transparent pricing</a>.</p>

      <h2>What to Bring to the Appointment</h2>
      <ul>
        <li><strong>Your pet</strong> in an appropriate carrier &mdash; small mammals in a pet carrier with hay, reptiles in a ventilated container with a warm towel, birds in a small travel cage</li>
        <li><strong>A fresh stool sample</strong> if possible (collected within 24 hours) &mdash; saves time on parasite testing</li>
        <li><strong>Photos of your pet's enclosure</strong> &mdash; lighting, substrate, food setup, cage layout. Your vet will want to review this.</li>
        <li><strong>A list of what you're feeding</strong> &mdash; brand names, supplements, treats</li>
        <li><strong>Any paperwork</strong> from the breeder or pet store</li>
        <li><strong>A list of questions</strong> &mdash; no question is too basic, especially for new exotic pet owners</li>
      </ul>

      <h2>What the Vet Will Do (By Species)</h2>

      <h3>Reptiles (Bearded Dragons, Snakes, Geckos, Turtles)</h3>
      <ul>
        <li>Full physical exam: eyes, mouth, skin, shell (for turtles/tortoises), vent, body condition</li>
        <li>Weight and length measurement</li>
        <li>Fecal test for parasites (extremely common in reptiles from pet stores)</li>
        <li>Husbandry review: UVB lighting, basking and cool-side temperatures, humidity, substrate, diet</li>
        <li>Discussion of calcium supplementation and vitamin D3</li>
      </ul>

      <h3>Birds (Parrots, Cockatiels, Finches, Budgies)</h3>
      <ul>
        <li>Physical exam: feather quality, beak and nail condition, eyes, nares (nostrils), body weight</li>
        <li>Gram stain of choana and/or vent to check for bacterial or yeast imbalances</li>
        <li>Wing and nail trim if needed</li>
        <li>Discussion of diet &mdash; if your bird is on a seed-based diet, we'll likely recommend transitioning to pellets</li>
        <li>Beak trim if overgrown (we offer this at SPAH)</li>
      </ul>

      <h3>Rabbits</h3>
      <ul>
        <li>Full exam: teeth (dental disease is extremely common in rabbits), ears, eyes, skin, body condition</li>
        <li>Fecal test for parasites</li>
        <li>Discussion of diet: hay intake, greens, pellet portions</li>
        <li>Nail trim</li>
        <li>Discussion of spay/neuter (reduces cancer risk and behavioral issues significantly)</li>
        <li>RHDV2 vaccine discussion (available in California)</li>
      </ul>

      <h3>Guinea Pigs &amp; Small Mammals</h3>
      <ul>
        <li>Physical exam: teeth, skin, ears, weight, body condition</li>
        <li>Fecal test</li>
        <li>Discussion of vitamin C intake (guinea pigs can't produce their own &mdash; this is critical)</li>
        <li>Bedding and cage setup review</li>
        <li>Social needs discussion (guinea pigs should ideally be in pairs)</li>
      </ul>

      <h2>Common Tests and What They Check</h2>
      <ul>
        <li><strong>Fecal exam:</strong> internal parasites (worms, coccidia, flagellates) &mdash; very common first finding in new exotic pets</li>
        <li><strong>Bloodwork (CBC + chemistry):</strong> organ function, infection markers, anemia, nutritional status</li>
        <li><strong>Gram stain:</strong> bacterial/yeast balance (mainly for birds)</li>
        <li><strong>X-rays:</strong> bone density, organ size, respiratory issues</li>
      </ul>
      <p>Not every pet needs every test. Your vet will recommend based on the exam findings and your pet's species.</p>

      <h2>How Often Should Exotic Pets See a Vet?</h2>
      <ul>
        <li><strong>Annual wellness exam</strong> for all exotic pets</li>
        <li><strong>Every 6 months</strong> for senior animals</li>
        <li><strong>Any time</strong> you notice changes in appetite, behavior, droppings, or appearance</li>
        <li><strong>Before introducing</strong> a new animal to an existing pet</li>
      </ul>

      <h2>Tips for a Stress-Free Visit</h2>
      <ul>
        <li><strong>Keep the carrier covered</strong> during transport &mdash; darkness reduces stress for most species</li>
        <li><strong>Avoid temperature extremes</strong> &mdash; bring reptiles in an insulated container in cool weather; run the car's heat or A/C first</li>
        <li><strong>Don't feed birds</strong> 1&ndash;2 hours before the visit (reduces regurgitation risk from stress)</li>
        <li><strong>Bring a towel or fleece blanket</strong> for small mammals to hide in</li>
        <li><strong>Stay calm</strong> &mdash; your pet picks up on your energy</li>
      </ul>

      <p>Your exotic pet's first vet visit sets the foundation for a long, healthy life. Whether you're a first-time reptile owner or you've had birds for years, we're here to help you give your pet the best care possible. At <a href="../about.html">South Pasadena Animal Hospital</a> in Alhambra, we see exotic pets every day and treat every patient like family. <a href="../services.html">Learn more about our services</a>.</p>"""

blog5_related = related_card("signs-bearded-dragon-needs-vet.html", "#E8F5E9,#C8E6C9", "&#129422;", "tag-reptile", "Reptile Care", "Signs Your Bearded Dragon Needs a Vet") + "\n" + related_card("guinea-pig-sneezing.html", "#FFF3E0,#FFE0B2", "&#128057;", "tag-small-mammal", "Small Mammal", "Guinea Pig Sneezing: When to Worry")

# ============================================================
# BUILD ALL 4 FILES
# ============================================================
blogs = [
    {
        "file": "guinea-pig-sneezing.html",
        "title": "Guinea Pig Sneezing: When to Worry and When It's Normal | SPAH Blog",
        "meta_desc": "Guinea pig sneezing? Learn when it's normal and when it could be a serious upper respiratory infection. Advice from the vets at SPAH in Alhambra, CA.",
        "keywords": "guinea pig sneezing, guinea pig upper respiratory infection, guinea pig vet, exotic vet near me, guinea pig sick symptoms, small mammal vet Alhambra",
        "og_desc": "When is guinea pig sneezing normal vs. a sign of a serious URI? A vet's guide.",
        "schema_headline": "Guinea Pig Sneezing: When to Worry and When It's Normal",
        "schema_desc": "Learn when guinea pig sneezing is normal versus a sign of upper respiratory infection.",
        "breadcrumb_name": "Guinea Pig Sneezing",
        "tag_bg": "#FFF3E0", "tag_color": "#E65100", "tag_text": "Small Mammal Care",
        "date_text": "March 31, 2026 &middot; 7 min read",
        "h1": "Guinea Pig Sneezing: When to Worry and When It's Normal",
        "content": blog2_content,
        "related": blog2_related,
        "cta_heading": "Concerned about your guinea pig?",
        "cta_desc": "We see guinea pigs, rabbits, and other small mammals at our Alhambra clinic. Book online or call us.",
        "cta_btn": "Book an Exotic Pet Exam",
    },
    {
        "file": "rabbit-gi-stasis.html",
        "title": "Rabbit GI Stasis: Symptoms, Treatment &amp; Prevention | SPAH Blog",
        "meta_desc": "Rabbit not eating? GI stasis can be fatal within 24-48 hours. Learn the symptoms, treatment, and prevention from the vets at SPAH in Alhambra, CA.",
        "keywords": "rabbit GI stasis, rabbit not eating, rabbit stomach problems, rabbit vet Alhambra, rabbit emergency signs, rabbit digestive issues",
        "og_desc": "GI stasis can kill a rabbit in 24-48 hours. Know the signs and how to prevent it.",
        "schema_headline": "Rabbit GI Stasis: Symptoms, Treatment and Prevention",
        "schema_desc": "GI stasis is one of the most dangerous conditions in pet rabbits. Learn the symptoms, treatment, and prevention.",
        "breadcrumb_name": "Rabbit GI Stasis",
        "tag_bg": "#F3E5F5", "tag_color": "#7B1FA2", "tag_text": "Rabbit Care",
        "date_text": "March 31, 2026 &middot; 8 min read",
        "h1": "Rabbit GI Stasis: Symptoms, Treatment &amp; Prevention",
        "content": blog3_content,
        "related": blog3_related,
        "cta_heading": "Rabbit not eating?",
        "cta_desc": "GI stasis can be an emergency. If your rabbit is showing symptoms, call us right away or book an appointment.",
        "cta_btn": "Book a Rabbit Exam",
    },
    {
        "file": "bird-feather-plucking.html",
        "title": "Why Is My Bird Pulling Out Its Feathers? | SPAH Blog",
        "meta_desc": "Bird feather plucking can be medical or behavioral. Learn the common causes and what to do from the vets at South Pasadena Animal Hospital in Alhambra.",
        "keywords": "bird feather plucking, parrot plucking feathers, bird vet near me, avian vet Alhambra, bird self mutilation, why bird pulling feathers",
        "og_desc": "Feather plucking in birds: medical vs behavioral causes and what to do about it.",
        "schema_headline": "Why Is My Bird Pulling Out Its Feathers?",
        "schema_desc": "Feather plucking can be medical or behavioral. Learn the causes and treatment options.",
        "breadcrumb_name": "Bird Feather Plucking",
        "tag_bg": "#E3F2FD", "tag_color": "#1565C0", "tag_text": "Bird Care",
        "date_text": "March 31, 2026 &middot; 8 min read",
        "h1": "Why Is My Bird Pulling Out Its Feathers?",
        "content": blog4_content,
        "related": blog4_related,
        "cta_heading": "Worried about your bird?",
        "cta_desc": "We see parrots, cockatiels, finches, and other pet birds at our Alhambra clinic. Book online or give us a call.",
        "cta_btn": "Book an Avian Exam",
    },
    {
        "file": "exotic-pet-first-vet-visit.html",
        "title": "What to Expect at Your Exotic Pet's First Vet Visit | SPAH Blog",
        "meta_desc": "New reptile, bird, or small mammal? Here's what happens at the first vet visit, what to bring, and what it costs. From the vets at SPAH in Alhambra.",
        "keywords": "exotic pet vet visit, first vet visit exotic pet, exotic vet Alhambra, exotic pet wellness exam, new exotic pet owner, reptile vet visit, bird vet visit",
        "og_desc": "New exotic pet? Here's exactly what to expect at the first vet visit and what to bring.",
        "schema_headline": "What to Expect at Your Exotic Pet's First Vet Visit",
        "schema_desc": "A complete guide to your exotic pet's first veterinary wellness exam.",
        "breadcrumb_name": "Exotic Pet First Vet Visit",
        "tag_bg": "#FCE4EC", "tag_color": "#C62828", "tag_text": "Exotic Pets",
        "date_text": "March 31, 2026 &middot; 9 min read",
        "h1": "What to Expect at Your Exotic Pet's First Vet Visit",
        "content": blog5_content,
        "related": blog5_related,
        "cta_heading": "New exotic pet? Let's get them started right.",
        "cta_desc": "We see reptiles, birds, rabbits, guinea pigs, hamsters, and more at our Alhambra clinic. Book your pet's first wellness exam.",
        "cta_btn": "Book a Wellness Exam",
    },
]

for b in blogs:
    url = f"https://www.spah.la/blog/{b['file']}"
    html = f"""{HEAD_START}
  <title>{b['title']}</title>
  <meta name="description" content="{b['meta_desc']}" />
  <meta name="keywords" content="{b['keywords']}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}" />
{og_meta(b['title'], b['og_desc'], url)}
{blog_schema(b['schema_headline'], b['schema_desc'], url)}
{breadcrumb_schema(b['breadcrumb_name'])}
{STYLES_AND_FONTS}
</head>
<body>

{NAV}

  <div class="max-w-3xl mx-auto px-6 pt-6">
    <nav class="font-body text-sm text-dark/50">
      <a href="../index.html" class="hover:text-brand">Home</a> <span class="mx-2">/</span>
      <a href="index.html" class="hover:text-brand">Blog</a> <span class="mx-2">/</span>
      <span class="text-dark/70">{b['breadcrumb_name']}</span>
    </nav>
  </div>

  <article class="max-w-3xl mx-auto px-6 py-12">
    <div class="mb-8">
      <span class="inline-block px-3 py-1 rounded-full text-xs font-bold tracking-widest uppercase" style="background:{b['tag_bg']};color:{b['tag_color']};">{b['tag_text']}</span>
      <p class="font-body text-dark/50 text-sm mt-3">{b['date_text']}</p>
    </div>
    <h1 class="font-display text-3xl sm:text-4xl font-bold text-dark mb-6" style="letter-spacing:-0.02em;line-height:1.2;">{b['h1']}</h1>
    <div class="prose">
{b['content']}
    </div>
  </article>

  <section class="py-12 bg-warm">
    <div class="max-w-5xl mx-auto px-6">
      <h2 class="font-display text-2xl font-bold text-dark mb-8 text-center">Related Articles</h2>
      <div class="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
{b['related']}
      </div>
    </div>
  </section>

{cta_section(b['cta_heading'], b['cta_desc'], b['cta_btn'])}

{FOOTER}"""

    filepath = os.path.join(BLOG_DIR, b['file'])
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {filepath}")

print("All 4 blog posts generated!")
