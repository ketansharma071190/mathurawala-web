#!/usr/bin/env python3
"""
Mathurawala Instagram Highlight Cover images.
5 covers: Menu, Made Live, Gifting, Reviews, Our Story
Output: 1080x1080 JPG. Displayed as circles on IG profile — keep key content center 60%.
Brand: navy bg, gold accent, mor-pankh motif, Georgia serif.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
def A(*p): return os.path.join(HERE, *p)

# palette
CREAM  = (246, 234, 203)
CREAM2 = (251, 243, 223)
PAPER  = (254, 251, 243)
NAVY   = (16, 36, 60)
NAVYD  = (9, 21, 36)
NAVYL  = (22, 48, 80)
TEAL   = (21, 131, 126)
TEAL2  = (30, 163, 154)
GOLD   = (201, 138, 30)
GOLD2  = (224, 165, 46)
GOLDL  = (239, 199, 114)
WHITE  = (255, 255, 255)

W = H = 1080

SERIF   = "/System/Library/Fonts/Supplemental/Didot.ttc"
SERIF_G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_GB= "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF_GI= "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS_F  = "/System/Library/Fonts/HelveticaNeue.ttc"

def font(path, size, idx=0):
    try:    return ImageFont.truetype(path, size, index=idx)
    except: return ImageFont.truetype(SERIF_G, size)

def f_serif(sz):  return font(SERIF, sz, 1)
def f_geob(sz):   return font(SERIF_GB, sz)
def f_geo(sz):    return font(SERIF_G, sz)
def f_geoi(sz):   return font(SERIF_GI, sz)
def f_sans(sz):   return font(SANS_F, sz, 0)

def cover_crop(path, tw, th):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    s = max(tw/iw, th/ih)
    img = img.resize((int(iw*s)+1, int(ih*s)+1), Image.LANCZOS)
    iw, ih = img.size
    return img.crop(((iw-tw)//2, (ih-th)//2, (iw-tw)//2+tw, (ih-th)//2+th))

def centered_text(draw, txt, fnt, y, color, w=W):
    bb = draw.textbbox((0,0), txt, font=fnt)
    x = (w - (bb[2]-bb[0])) // 2
    draw.text((x, y), txt, font=fnt, fill=color)

def mor_pankh_accent(base_img, size=220, pos="top-right"):
    """Paste the coloured mor-pankh from logo-light.png as a decorative accent."""
    src = Image.open(A("new","logo-light.png")).convert("RGBA")
    w0, h0 = src.size
    crop = src.crop((int(w0*0.86), 0, w0, int(h0*0.62)))
    px = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r,g,b,a = px[x,y]
            if a < 20: continue
            mx, mn = max(r,g,b), min(r,g,b)
            if (mx-mn) < 26 and mn > 150:
                px[x,y] = (r,g,b,0)
    crop = crop.crop(crop.getbbox())
    ratio = size / crop.height
    feather = crop.resize((int(crop.width*ratio), size), Image.LANCZOS)
    fw, fh = feather.size
    bw, bh = base_img.size
    if pos == "top-right":
        px_pos = (bw - fw + 30, -20)
    elif pos == "bottom-right":
        px_pos = (bw - fw + 30, bh - fh + 20)
    else:
        px_pos = (bw - fw - 20, 30)
    base_img.paste(feather, px_pos, feather)

def gold_line(draw, y, margin=80):
    draw.line([(margin, y), (W-margin, y)], fill=GOLD2, width=2)

def save(img, name):
    out = A(f"highlight-{name}.jpg")
    img.convert("RGB").save(out, "JPEG", quality=94)
    print(f"  saved {out}")

# ---- COVER BUILDER ----
def make_cover(photo_path, label, hindi_sub, tint_opacity=0.72):
    """Dark navy base with a dim food photo in top 55%, gold label at bottom."""
    base = Image.new("RGBA", (W, H), NAVYD)

    # food photo in top half, darkened
    if photo_path and os.path.exists(photo_path):
        photo = cover_crop(photo_path, W, int(H*0.62))
        photo = photo.convert("RGBA")
        # darken overlay
        dark = Image.new("RGBA", photo.size, NAVYD + (int(tint_opacity*255),))
        photo = Image.alpha_composite(photo.convert("RGBA"), dark)
        base.paste(photo, (0, 0))

    # bottom gradient fill to ensure text readability
    grad_h = int(H * 0.52)
    for dy in range(grad_h):
        t = dy / grad_h
        a = int(255 * (0.1 + 0.9 * t))
        draw_tmp = ImageDraw.Draw(base)
        draw_tmp.line([(0, H-grad_h+dy), (W, H-grad_h+dy)], fill=NAVYD + (a,))

    draw = ImageDraw.Draw(base)

    # gold horizontal rules as decorative frame
    gold_line(draw, H - 310)

    # hindi/Braj subtitle
    if hindi_sub:
        f = f_geoi(46)
        bb = draw.textbbox((0,0), hindi_sub, font=f)
        x = (W - (bb[2]-bb[0])) // 2
        draw.text((x, H-295), hindi_sub, font=f, fill=GOLDL)

    # main label — large Didot bold
    f = f_serif(164)
    bb = draw.textbbox((0,0), label, font=f)
    lw = bb[2]-bb[0]
    lh = bb[3]-bb[1]
    ly = H - 295 + 60
    draw.text(((W-lw)//2, ly), label, font=f, fill=CREAM)

    gold_line(draw, H - 100)

    # "Mathurawala" wordmark tiny at very bottom
    f2 = f_sans(32)
    centered_text(draw, "Mathurawala", f2, H - 82, GOLDL + (180,))

    # mor-pankh accent top-right
    mor_pankh_accent(base.convert("RGBA") if base.mode == "RGBA" else base, size=160, pos="top-right")

    return base

ARIAL_UNI = "/Library/Fonts/Arial Unicode.ttf"
def f_arial(sz): return font(ARIAL_UNI, sz)

def draw_stars(draw, x, y, count=4, half=1, size=64):
    """Draw filled/outline star shapes using Arial which supports unicode stars."""
    fnt = f_arial(size)
    stars_str = "★" * count + "☆" * half
    draw.text((x, y), stars_str, font=fnt, fill=GOLD2)

def make_reviews_cover():
    """Text-only: 4.2 stars centered, big number, gold stars, tagline."""
    base = Image.new("RGBA", (W, H), NAVYD)
    draw = ImageDraw.Draw(base)

    # subtle circle motif in bg
    for r in [340, 410, 480]:
        draw.ellipse([(W//2-r, H//2-r), (W//2+r, H//2+r)],
                     outline=NAVYL+(80,), width=1)

    # 4.2 big number
    f_big = f_serif(300)
    num = "4.2"
    bb = draw.textbbox((0,0), num, font=f_big)
    x = (W - (bb[2]-bb[0])) // 2
    draw.text((x, H//2 - 290), num, font=f_big, fill=CREAM)

    # stars using Arial (supports unicode stars)
    f_star = f_arial(72)
    stars = "★ ★ ★ ★ ☆"
    bb2 = draw.textbbox((0,0), stars, font=f_star)
    sx = (W - (bb2[2]-bb2[0])) // 2
    draw.text((sx, H//2 + 40), stars, font=f_star, fill=GOLD2)

    # "700+ reviews"
    f_sub = f_geo(52)
    sub = "700+ Google reviews"
    bb3 = draw.textbbox((0,0), sub, font=f_sub)
    draw.text(((W-(bb3[2]-bb3[0]))//2, H//2 + 130), sub, font=f_sub, fill=CREAM2+(200,))

    gold_line(draw, H-310)

    f_label = f_geoi(48)
    centered_text(draw, "Pune's most-loved chaat", f_label, H-290, GOLDL)

    f_main = f_serif(164)
    bb4 = draw.textbbox((0,0), "Reviews", font=f_main)
    draw.text(((W-(bb4[2]-bb4[0]))//2, H-230), "Reviews", font=f_main, fill=CREAM)

    gold_line(draw, H-100)
    f_wm = f_sans(32)
    centered_text(draw, "Mathurawala", f_wm, H-82, GOLDL+(180,))

    mor_pankh_accent(base, size=160, pos="top-right")
    return base

def feather_large(size):
    """Same as feather() but returns the coloured mor-pankh for large-format use."""
    src = Image.open(A("new","logo-light.png")).convert("RGBA")
    w0, h0 = src.size
    crop = src.crop((int(w0*0.86), 0, w0, int(h0*0.62)))
    px = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r,g,b,a = px[x,y]
            if a < 20: continue
            mx, mn = max(r,g,b), min(r,g,b)
            if (mx-mn) < 26 and mn > 150:
                px[x,y] = (r,g,b,0)
    crop = crop.crop(crop.getbbox())
    ratio = size / crop.height
    return crop.resize((int(crop.width*ratio), size), Image.LANCZOS)

def make_story_cover():
    """Large centered mor-pankh feather + 'Our Story' label."""
    base = Image.new("RGBA", (W, H), NAVYD)

    # large centred feather (the brand soul)
    fth = feather_large(480)
    fw, fh = fth.size
    px = (W - fw) // 2
    py = int(H * 0.04)
    base.paste(fth, (px, py), fth)

    # subtle gold radial glow under feather
    glow = Image.new("RGBA", (W, H), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    cx, cy = W//2, py + fh//2
    for r in range(260, 10, -8):
        a = int(22 * (1 - r/260))
        gd.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=GOLD+(a,))
    base = Image.alpha_composite(base.convert("RGBA"), glow)
    draw = ImageDraw.Draw(base)

    gold_line(draw, H-310)
    f_sub = f_geoi(46)
    centered_text(draw, "Est. Mathura, since time immemorial", f_sub, H-295, GOLDL)
    f_main = f_serif(128)
    bb = draw.textbbox((0,0), "Our Story", font=f_main)
    draw.text(((W-(bb[2]-bb[0]))//2, H-230), "Our Story", font=f_main, fill=CREAM)
    gold_line(draw, H-100)
    f_wm = f_sans(32)
    centered_text(draw, "Mathurawala", f_wm, H-82, GOLDL+(180,))

    return base

def make_made_live_cover():
    """'Made Live' cover — kachori photo + hands cooking label."""
    return make_cover(
        A("new","kachori-sabji.jpg"),
        "Made Live",
        "har roz, Mathura ke haathon se",
        tint_opacity=0.65
    )

if __name__ == "__main__":
    print("Building Mathurawala IG Highlight Covers...")

    covers = [
        ("menu",       make_cover(A("new","kachori-sabji.jpg"), "Menu", "Braj ki asli recipe")),
        ("made-live",  make_made_live_cover()),
        ("gifting",    make_cover(A("peda.jpg"), "Gifting", "Mathura Peda aur hampers")),
        ("reviews",    make_reviews_cover()),
        ("our-story",  make_story_cover()),
    ]

    for name, img in covers:
        save(img, name)

    print("Done. 5 highlight covers saved as highlight-*.jpg in assets/")
