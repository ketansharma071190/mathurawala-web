#!/usr/bin/env python3
"""
Patch all braj-kitchen hub pages with the new header/footer/fab
matching the main index.html. Uses bk- prefixed classes to stay
clean alongside the existing styles.css hub content styles.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = [
    "index.html", "bedai-sabji.html", "kachori-sabji.html",
    "mathura-peda.html", "sattvik-food.html",
    "chappan-bhog.html", "janmashtami-bhog.html",
]

NEW_STYLE = """
<style>
/* ---- new nav / footer override (bk- prefix, no conflict with styles.css) ---- */
:root{--bk-cream:#F6EACB;--bk-navy:#10243C;--bk-navy-d:#0B1B2E;--bk-teal:#15837E;--bk-gold:#C98A1E;--bk-gold2:#E0A52E;}
.site-header{display:none!important}
header{position:sticky;top:0;z-index:60;background:rgba(246,234,203,.92);backdrop-filter:blur(8px);border-bottom:1px solid rgba(21,131,126,.18)}
.bk-nav{display:flex;align-items:center;justify-content:space-between;height:76px;gap:20px;max-width:1200px;margin:0 auto;padding:0 28px}
.bk-brand img{height:46px;width:auto;display:block}
.bk-menu{display:flex;gap:24px}
.bk-menu a{color:var(--bk-navy);font-weight:600;font-size:15px;text-decoration:none}
.bk-menu a:hover{color:var(--bk-teal)}
.bk-btn{display:inline-block;padding:11px 20px;border-radius:40px;font-weight:600;font-size:14px;background:var(--bk-gold2);color:var(--bk-navy);border:none;text-decoration:none;transition:.2s}
.bk-btn:hover{background:var(--bk-gold)}
.bk-hamburger{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:8px;margin:-8px}
.bk-hamburger span{width:24px;height:2.5px;background:var(--bk-navy);border-radius:2px;transition:.25s}
.bk-menu-order{display:none}
#navtog:checked~.bk-hamburger span:nth-child(1){transform:translateY(7.5px) rotate(45deg)}
#navtog:checked~.bk-hamburger span:nth-child(2){opacity:0}
#navtog:checked~.bk-hamburger span:nth-child(3){transform:translateY(-7.5px) rotate(-45deg)}
.bk-footer{position:relative;background:var(--bk-navy-d);color:#9fb0c4;padding:50px 0 36px;text-align:center;overflow:hidden;margin-top:0}
.bk-footer-sil{position:absolute;left:0;right:0;bottom:0;width:100%;opacity:.16;filter:brightness(1.7)}
.bk-footer-wrap{position:relative;max-width:1200px;margin:0 auto;padding:0 28px}
.bk-footer-logo{height:56px;width:auto;margin:0 auto 16px;display:block}
.bk-footer-links{margin:8px 0 14px;display:flex;gap:22px;justify-content:center;flex-wrap:wrap;font-size:14px;font-weight:600}
.bk-footer-links a{color:#9fb0c4;text-decoration:none}.bk-footer-links a:hover{color:var(--bk-gold2)}
.bk-footer-social{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin:6px 0 4px}
.bk-footer-social a{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#cdd8e6;border:1px solid rgba(255,255,255,.18);padding:9px 17px;border-radius:30px;transition:.2s;text-decoration:none}
.bk-footer-social a:hover{border-color:var(--bk-gold2);color:var(--bk-gold2)}
.bk-footer-social svg{width:16px;height:16px;flex:none}
.bk-footer-fine{font-size:12.5px;color:#69809a;margin-top:12px}
.site-footer{display:none!important}
.fab{position:fixed;right:18px;bottom:18px;z-index:80;width:56px;height:56px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,.28);text-decoration:none}
.fab:hover{transform:scale(1.06)}
.fab svg{width:30px;height:30px;fill:#fff}
@media(max-width:700px){
 .bk-menu{display:none;flex-direction:column;position:fixed;top:76px;left:0;right:0;background:rgba(246,234,203,.98);backdrop-filter:blur(10px);padding:20px 28px 28px;gap:18px;border-bottom:1px solid rgba(21,131,126,.2);z-index:59}
 #navtog:checked~.bk-menu{display:flex}
 .bk-hamburger{display:flex}
 .bk-menu-order{display:inline-flex!important}
 .bk-btn.bk-nav-order{display:none}
}
</style>
"""

NEW_HEADER = """<header>
 <div class="bk-nav">
  <a class="bk-brand" href="../index.html" aria-label="Mathurawala home"><img loading="lazy" decoding="async" src="../assets/new/logo-clean.png" alt="Mathurawala" /></a>
  <input type="checkbox" id="navtog" hidden>
  <nav class="bk-menu">
   <a href="../index.html#food">Food</a>
   <a href="../menu.html">Menu</a>
   <a href="../index.html#gifting">Gifting</a>
   <a href="../gallery.html">Gallery</a>
   <a href="../braj-kitchen/index.html" style="color:var(--bk-teal)">Braj Kitchen</a>
   <a href="../index.html#franchise">Franchise</a>
   <a href="../index.html#visit">Visit</a>
   <a class="bk-btn bk-menu-order" href="https://wa.me/919356326855?text=Radhe%20Radhe%20Mathurawala%2C%20I%20want%20to%20order%20for%20pickup.">Order on WhatsApp</a>
  </nav>
  <a class="bk-btn bk-nav-order" href="https://wa.me/919356326855?text=Radhe%20Radhe%20Mathurawala%2C%20I%20want%20to%20order%20for%20pickup.">Order on WhatsApp</a>
  <label for="navtog" class="bk-hamburger" aria-label="Open menu"><span></span><span></span><span></span></label>
 </div>
</header>"""

NEW_FOOTER = """<footer class="bk-footer">
 <img loading="lazy" decoding="async" class="bk-footer-sil" src="../assets/new/temple-silhouette.png" alt="" aria-hidden="true" />
 <div class="bk-footer-wrap">
  <img loading="lazy" decoding="async" class="bk-footer-logo" src="../assets/new/logo-light.png" alt="Mathurawala" />
  <div class="bk-footer-links">
   <a href="../index.html">Home</a><a href="../menu.html">Menu</a><a href="../index.html#gifting">Gifting</a><a href="../gallery.html">Gallery</a><a href="../braj-kitchen/index.html">Braj Kitchen</a><a href="../index.html#franchise">Franchise</a><a href="../index.html#visit">Visit</a>
  </div>
  <div class="bk-footer-social">
   <a href="https://www.instagram.com/mathurawalaofficial/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.5" cy="6.5" r="1.2" fill="currentColor" stroke="none"/></svg>Instagram</a>
   <a href="https://www.zomato.com/pune/mathurawala-baner" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11l8.5-1.5L20 11M5 11v8h14v-8M9 19v-5h6v5"/></svg>Zomato</a>
   <a href="https://www.google.com/maps/search/?api=1&query=Mathurawala+Baner+Pune" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.5 7-12A7 7 0 0 0 5 10c0 5.5 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>Google reviews</a>
  </div>
  <div class="bk-footer-fine">Bharat's original food, from the world's oldest living kitchen.<br>Baner, Pune · Pure vegetarian · Made live, no preservatives · Radhe Radhe 🙏</div>
 </div>
</footer>

<a class="fab" href="https://wa.me/919356326855?text=Radhe%20Radhe%2C%20I%20want%20to%20order%20for%20pickup." aria-label="Order on WhatsApp" target="_blank" rel="noopener"><svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20zm4.6-5.9c-.25-.13-1.5-.74-1.7-.82-.23-.08-.4-.13-.56.13-.17.25-.64.82-.79.99-.14.17-.29.19-.54.06-.25-.13-1.06-.39-2-1.24-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.39.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.85-.2-.48-.4-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.5-.61 1.71-1.21.21-.59.21-1.1.15-1.21-.06-.11-.23-.17-.48-.3z"/></svg></a>"""


def patch(filename):
    path = os.path.join(HERE, filename)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    # 1. Inject new style block before </head>
    if "bk-nav" not in src:
        src = src.replace("</head>", NEW_STYLE + "\n</head>", 1)

    # 2. Replace old header block
    # Match <header ...> ... </header> (the site-header block)
    src = re.sub(
        r'<header[^>]*class="site-header"[^>]*>.*?</header>',
        NEW_HEADER, src, flags=re.DOTALL
    )

    # 3. Replace old footer block
    src = re.sub(
        r'<footer[^>]*class="site-footer"[^>]*>.*?</footer>',
        NEW_FOOTER, src, flags=re.DOTALL
    )

    # 4. Remove any leftover fab if already patched (avoid duplicates)
    src = re.sub(r'\n<a class="fab".*?</a>', "", src, flags=re.DOTALL)

    # 5. Fix old logo reference to brand-original-logo.png -> logo-clean.png in brand link
    src = src.replace("../assets/brand-original-logo.png", "../assets/new/logo-clean.png")

    # 6. Remove old data-header script block if present
    src = re.sub(r'<script[^>]*>.*?data-header.*?</script>', "", src, flags=re.DOTALL)

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"patched {filename}")


for page in PAGES:
    patch(page)

print("all hub pages patched")
