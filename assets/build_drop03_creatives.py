#!/usr/bin/env python3
"""
Mathurawala Content Drop 03 — weeks 5-6 post creatives.
4 posts: Morning Nashta, Heritage/no-onion, Mathura Peda gifting, Bedai Sabji close-up.
Same photo_poster style as festival creatives.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
def A(*p): return os.path.join(HERE, *p)

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
MAROON = (138, 45, 42)
WHITE  = (255, 255, 255)

W, H = 1080, 1350  # feed portrait

SERIF   = "/System/Library/Fonts/Supplemental/Didot.ttc"
SERIF_G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_GB= "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF_GI= "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS_F  = "/System/Library/Fonts/HelveticaNeue.ttc"
ARIAL_U = "/Library/Fonts/Arial Unicode.ttf"

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

def centered(draw, txt, fnt, y, color, w=W):
    bb = draw.textbbox((0,0), txt, font=fnt)
    x = (w - (bb[2]-bb[0])) // 2
    draw.text((x, y), txt, font=fnt, fill=color)

def mor_pankh(base_img, size=180, pos="top-right"):
    src = Image.open(A("new","logo-light.png")).convert("RGBA")
    w0, h0 = src.size
    crop = src.crop((int(w0*0.86), 0, w0, int(h0*0.62)))
    px = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r,g,b,a = px[x,y]
            if a < 20: continue
            if (max(r,g,b)-min(r,g,b)) < 26 and min(r,g,b) > 150:
                px[x,y] = (r,g,b,0)
    crop = crop.crop(crop.getbbox())
    ratio = size / crop.height
    fth = crop.resize((int(crop.width*ratio), size), Image.LANCZOS)
    fw, fh = fth.size
    bw, bh = base_img.size
    if pos == "top-right":   px_pos = (bw-fw+24, -14)
    elif pos == "top-left":  px_pos = (-14, -14)
    else:                    px_pos = (bw-fw+24, bh-fh+14)
    base_img.paste(fth, px_pos, fth)

def vgrad(w, h, top_col, bot_col, top_a=255, bot_a=255):
    g = Image.new("RGBA", (w, h), (0,0,0,0))
    px = g.load()
    for y in range(h):
        t = y / (h-1)
        r = int(top_col[0]*(1-t) + bot_col[0]*t)
        gg = int(top_col[1]*(1-t) + bot_col[1]*t)
        b = int(top_col[2]*(1-t) + bot_col[2]*t)
        a = int(top_a*(1-t) + bot_a*t)
        for x in range(w):
            px[x,y] = (r,gg,b,a)
    return g

def photo_poster(photo_path, kicker, headline, subline, footer_note="",
                 photo_h_frac=0.62, tint_alpha=160, kicker_teal=False):
    """Dark-overlay photo top + cream text box bottom."""
    base = Image.new("RGBA", (W, H), NAVYD)

    # photo
    photo_h = int(H * photo_h_frac)
    photo = cover_crop(photo_path, W, photo_h).convert("RGBA")
    dark = Image.new("RGBA", photo.size, NAVYD + (tint_alpha,))
    photo = Image.alpha_composite(photo, dark)
    base.paste(photo.convert("RGB"), (0, 0))

    # cream panel bottom
    panel_y = photo_h - 40
    panel = Image.new("RGBA", (W, H - panel_y), CREAM + (255,))
    base.paste(panel, (0, panel_y), panel)

    # gold top rule on cream panel
    draw = ImageDraw.Draw(base)
    draw.line([(60, panel_y + 32), (W-60, panel_y + 32)], fill=GOLD2, width=2)

    # kicker
    f_k = f_sans(28)
    kicker_col = TEAL if kicker_teal else GOLD
    centered(draw, kicker.upper(), f_k, panel_y + 46, kicker_col)

    # headline (Didot serif, navy)
    f_h = f_serif(82)
    # word-wrap headline if it fits, else split manually
    lines = []
    words = headline.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        bb = draw.textbbox((0,0), test, font=f_h)
        if bb[2]-bb[0] > W-100 and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line: lines.append(line)

    y_h = panel_y + 86
    for ln in lines:
        bb = draw.textbbox((0,0), ln, font=f_h)
        x = (W-(bb[2]-bb[0]))//2
        draw.text((x, y_h), ln, font=f_h, fill=NAVY)
        y_h += bb[3]-bb[1] + 8

    # subline (italic Georgia, ink2)
    INK2 = (51, 72, 95)
    f_s = f_geoi(44)
    # split at 50 chars
    sub_lines = []
    words2 = subline.split()
    line2 = ""
    for w2 in words2:
        test2 = (line2 + " " + w2).strip()
        bb2 = draw.textbbox((0,0), test2, font=f_s)
        if bb2[2]-bb2[0] > W-120 and line2:
            sub_lines.append(line2)
            line2 = w2
        else:
            line2 = test2
    if line2: sub_lines.append(line2)

    y_s = y_h + 16
    for ln2 in sub_lines:
        bb2 = draw.textbbox((0,0), ln2, font=f_s)
        x2 = (W-(bb2[2]-bb2[0]))//2
        draw.text((x2, y_s), ln2, font=f_s, fill=INK2)
        y_s += bb2[3]-bb2[1] + 8

    # bottom gold rule
    draw.line([(60, H-64), (W-60, H-64)], fill=GOLD2, width=1)

    # footer note or Mathurawala wordmark
    f_fn = f_sans(30)
    centered(draw, footer_note if footer_note else "Mathurawala · Baner, Pune", f_fn, H-56, GOLD)

    # mor pankh on photo (top-right)
    base_rgba = base.convert("RGBA")
    mor_pankh(base_rgba, size=200, pos="top-right")

    return base_rgba

def save(img, name):
    out = A(f"post-d3-{name}.jpg")
    img.convert("RGB").save(out, "JPEG", quality=93)
    print(f"  saved {out}")

if __name__ == "__main__":
    print("Building Content Drop 03 creatives...")

    # 1. Morning Nashta
    save(photo_poster(
        A("exact-kachori-sabji.jpg"),
        kicker="9 AM · Baner, Pune",
        headline="Mathura ka asli nashta",
        subline="Kachori. Bedai. Jalebi. Kulhad lassi. Har subah, tayaar.",
        footer_note="Mathurawala · Open from 9 AM",
        tint_alpha=140,
    ), "morning-nashta")

    # 2. Bedai Sabji close-up / identity marker
    save(photo_poster(
        A("exact-bedai-sabji.jpg"),
        kicker="Mathura Specials",
        headline="Bedai Sabji",
        subline="Urad dal ka puri. Dhire pakaye aloo-tamatar ki sabji. Mathura ke haathon se.",
        footer_note="Mathurawala · Pure veg · No onion, no garlic",
        tint_alpha=145,
        kicker_teal=True,
    ), "bedai-identity")

    # 3. Heritage/no-onion education post (paani poori)
    save(photo_poster(
        A("exact-paani-poori.jpg"),
        kicker="Braj heritage · Why no onion, no garlic?",
        headline="Shuddh Braj ka swad",
        subline="3,000 saal pehle se. Prasad jaisi shuddhai. Swaad mein koi compromise nahi.",
        footer_note="Mathurawala · Bharat's original food",
        tint_alpha=150,
    ), "no-onion-heritage")

    # 4. Mathura Peda gifting
    save(photo_poster(
        A("peda.jpg"),
        kicker="Gifting · Mathura Peda",
        headline="Jo gift mein original ho",
        subline="Khoya se bana Mathura Peda. Rs 700/kg. Har tayohar, har puja, har shuruaat.",
        footer_note="Order on WhatsApp: +91 93563 26855",
        tint_alpha=155,
    ), "peda-gifting")

    print("Done. 4 Drop 03 posts saved as post-d3-*.jpg")
