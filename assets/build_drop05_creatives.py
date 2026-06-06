#!/usr/bin/env python3
"""Build Content Drop 05 poster creatives."""
import sys, os
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    os.system("pip install pillow -q")
    from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
REAL = os.path.join(BASE, "real")
OUT  = os.path.join(BASE, "drop05")
os.makedirs(OUT, exist_ok=True)

NAVY  = (16, 36, 60)
CREAM = (246, 234, 203)
GOLD  = (201, 138, 30)
WHITE = (255, 255, 255)
TEAL  = (21, 131, 126)

def wrap(text, max_chars):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if len(test) <= max_chars:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def photo_poster(src, title_hi, title_en, sub, out_name, kicker="Mathurawala · Baner, Pune"):
    img = Image.open(src).convert("RGB")
    W, H = 1080, 1080
    # crop to square
    iw, ih = img.size
    if iw > ih:
        off = (iw - ih) // 2
        img = img.crop((off, 0, off + ih, ih))
    else:
        img = img.crop((0, 0, iw, iw))
    img = img.resize((W, H), Image.LANCZOS)

    # gradient overlay (dark bottom)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(ov)
    for y in range(H):
        alpha = int(200 * (y / H) ** 1.5)
        draw_ov.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))

    combo = img.convert("RGBA")
    combo = Image.alpha_composite(combo, ov)
    draw = ImageDraw.Draw(combo)

    # fonts
    try:
        fnt_big   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 68)
        fnt_mid   = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 42)
        fnt_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttf", 28)
        fnt_kick  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttf", 22)
    except:
        fnt_big = fnt_mid = fnt_small = fnt_kick = ImageFont.load_default()

    # kicker pill top-right
    kb = draw.textbbox((0, 0), kicker, font=fnt_kick)
    kw = kb[2] - kb[0] + 28
    kh = kb[3] - kb[1] + 14
    draw.rounded_rectangle([W - kw - 24, 22, W - 24, 22 + kh], radius=20, fill=(*NAVY, 210))
    draw.text((W - kw - 24 + 14, 22 + 7), kicker, font=fnt_kick, fill=WHITE)

    # gold divider
    draw.rectangle([60, H - 310, 60 + 60, H - 305], fill=(*GOLD, 255))

    # Hindi title
    hi_lines = wrap(title_hi, 20)
    y = H - 295
    for ln in hi_lines:
        draw.text((60, y), ln, font=fnt_big, fill=WHITE)
        y += 74

    # English sub
    en_lines = wrap(title_en, 30)
    for ln in en_lines:
        draw.text((60, y), ln, font=fnt_mid, fill=(*CREAM, 230))
        y += 52

    # sub line
    sub_lines = wrap(sub, 44)
    y += 4
    for ln in sub_lines:
        draw.text((60, y), ln, font=fnt_small, fill=(*WHITE, 190))
        y += 36

    # Radhe Radhe at bottom right
    rr = "Khao toh asli khao"
    rb = draw.textbbox((0, 0), rr, font=fnt_kick)
    draw.text((W - (rb[2]-rb[0]) - 26, H - 38), rr, font=fnt_kick, fill=(*GOLD, 200))

    out_path = os.path.join(OUT, out_name)
    combo.convert("RGB").save(out_path, quality=93)
    print(f"  Saved: {out_path}")
    return out_path

def main():
    print("Building Drop 05 creatives...")

    # Post 1: Poori Sabji — Morning Mathura
    photo_poster(
        src=os.path.join(REAL, "real-poori-sabji.jpg"),
        title_hi="Mathura ki subah.",
        title_en="Poori Sabji, made live.",
        sub="Hot pooris, spiced sabji. Pure veg. 9 AM onwards.",
        out_name="post-d5-poori-sabji.jpg",
    )

    # Post 2: Dahi Bhalla All Day
    photo_poster(
        src=os.path.join(REAL, "real-dahi-bhalla.jpg"),
        title_hi="Subah se raat tak.",
        title_en="Dahi Bhalla, all day.",
        sub="Soft bhalla, cooling dahi, saunth. Anytime, always fresh.",
        out_name="post-d5-dahi-bhalla-allday.jpg",
    )

    # Post 3: Heritage Story — Kachori
    photo_poster(
        src=os.path.join(REAL, "real-kachori-sabji.jpg"),
        title_hi="3,000 saal purana swaad.",
        title_en="Mathura's original kachori.",
        sub="Hing, urad dal, aloo-tamatar sabji. No shortcuts.",
        out_name="post-d5-kachori-heritage.jpg",
    )

    # Post 4: Ratlami Sev
    photo_poster(
        src=os.path.join(REAL, "real-ratlami-sev.jpg"),
        title_hi="Asli Ratlami Sev.",
        title_en="Crisp, spiced, and real.",
        sub="Made the asli way. Perfect to snack, perfect to gift.",
        out_name="post-d5-ratlami-sev.jpg",
    )

    print("All done. Radhe Radhe.")

if __name__ == "__main__":
    main()
