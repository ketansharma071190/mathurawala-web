#!/usr/bin/env python3
"""
Mathurawala Content Drop 04 — weeks 7-8 post creatives.
4 posts: Bedai Sabji, Kulhad Lassi, Hot Jalebi, Aloo Tikki Chaat.
Uses new real photos from assets/real/ folder.
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
WHITE  = (255, 255, 255)

W, H = 1080, 1350  # feed portrait

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

def centered(draw, txt, fnt, y, color, w=W):
    bb = draw.textbbox((0,0), txt, font=fnt)
    x = (w - (bb[2]-bb[0])) // 2
    draw.text((x, y), txt, font=fnt, fill=color)

def mor_pankh(base_img, size=180, pos="top-right"):
    try:
        src = Image.open(A("new","logo-light.png")).convert("RGBA")
        s = size / max(src.size)
        src = src.resize((int(src.size[0]*s), int(src.size[1]*s)), Image.LANCZOS)
        margin = 28
        if pos == "top-right":
            x = base_img.size[0] - src.size[0] - margin
            y = margin
        else:
            x = margin
            y = margin
        alpha = Image.new("RGBA", base_img.size, (0,0,0,0))
        alpha.paste(src, (x, y), src)
        result = Image.alpha_composite(base_img, alpha)
        base_img.paste(result, (0,0))
    except Exception as e:
        print(f"  mor_pankh skip: {e}")

def photo_poster(photo_path, kicker, headline, subline, footer_note="",
                 photo_h_frac=0.62, tint_alpha=155, kicker_teal=False):
    """Dark-overlay photo top + cream text box bottom."""
    base = Image.new("RGBA", (W, H), NAVYD)

    photo_h = int(H * photo_h_frac)
    photo = cover_crop(photo_path, W, photo_h).convert("RGBA")
    dark = Image.new("RGBA", photo.size, NAVYD + (tint_alpha,))
    photo = Image.alpha_composite(photo, dark)
    base.paste(photo.convert("RGB"), (0, 0))

    panel_y = photo_h - 40
    panel = Image.new("RGBA", (W, H - panel_y), CREAM + (255,))
    base.paste(panel, (0, panel_y), panel)

    draw = ImageDraw.Draw(base)
    draw.line([(60, panel_y + 32), (W-60, panel_y + 32)], fill=GOLD2, width=2)

    f_k = f_sans(28)
    kicker_col = TEAL if kicker_teal else GOLD
    centered(draw, kicker.upper(), f_k, panel_y + 46, kicker_col)

    f_h = f_serif(82)
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

    INK2 = (51, 72, 95)
    f_s = f_geoi(44)
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

    draw.line([(60, H-64), (W-60, H-64)], fill=GOLD2, width=1)

    f_fn = f_sans(30)
    centered(draw, footer_note if footer_note else "Mathurawala · Baner, Pune", f_fn, H-56, GOLD)

    base_rgba = base.convert("RGBA")
    mor_pankh(base_rgba, size=200, pos="top-right")
    return base_rgba

def save(img, name):
    out = A(f"post-d4-{name}.jpg")
    img.convert("RGB").save(out, "JPEG", quality=93)
    print(f"  saved {out}")

if __name__ == "__main__":
    print("Building Content Drop 04 creatives...")

    # 1. Bedai Sabji — morning identity post
    save(photo_poster(
        A("real","real-bedai-sabji.jpg"),
        kicker="Mathura ka asli nashta",
        headline="Bedai Sabji",
        subline="Urad ki puri. Dhime aloo-tamatar ki sabji. Sirf Mathura mein aise banti hai.",
        footer_note="Mathurawala · Pure veg · No onion, no garlic",
        tint_alpha=140,
        kicker_teal=True,
    ), "bedai-sabji")

    # 2. Kulhad Lassi — afternoon / summer / lifestyle
    save(photo_poster(
        A("real","real-kulhad-lassi.jpg"),
        kicker="Baner ka asli swad",
        headline="Kulhad Lassi",
        subline="Thick. Fresh. Mathura wali richness. Koi mix nahi. Roz tayaar.",
        footer_note="Mathurawala · Baner, Pune",
        tint_alpha=145,
    ), "kulhad-lassi")

    # 3. Hot Jalebi — evening treat / Friday
    save(photo_poster(
        A("real","real-jalebi.jpg"),
        kicker="Made live · Kadhai se seedha",
        headline="Hot Jalebi",
        subline="Crisp. Juicy. Kesar ka rang. Frozen kabhi nahi. Roz fresh kadhai mein.",
        footer_note="Mathurawala · Khao toh asli khao",
        tint_alpha=148,
    ), "hot-jalebi")

    # 4. Aloo Tikki Chaat — evening / weekend crowd-puller
    save(photo_poster(
        A("real","real-aloo-tikki.jpg"),
        kicker="Evening chaat · Baner ka favourite",
        headline="Aloo Tikki Chaat",
        subline="Crisp tikki. Dahi. Saunth. Sev. Ek plate mein sab kuch asli.",
        footer_note="Mathurawala · Bharat's original food",
        tint_alpha=150,
        kicker_teal=True,
    ), "aloo-tikki-chaat")

    print("Done. 4 Drop 04 posts saved as post-d4-*.jpg")
