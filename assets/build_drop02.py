#!/usr/bin/env python3
"""
Content Drop 02 — weeks 3-4 always-on social creatives.
Four posts: Chole Bhature, Aloo Tikki Chaat, Mathura Peda, Sattvik/no-onion educational.
"""
import build_festival_creatives as B
A=B.A; GOLD2=B.GOLD2; GOLDL=B.GOLDL; TEAL2=B.TEAL2; CREAM=B.CREAM
NAVY=B.NAVY; NAVYD=B.NAVYD; TEAL=B.TEAL; MAROON=B.MAROON

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import os


def chole_bhature():
    """Chole Bhature — the revenue king post. Bold, satisfying."""
    B.photo_poster(
        "post-d2-chole-bhature.jpg",
        A("latest-chole-bhature.jpg"),
        "Ek plate jo sab kuch keh de",
        GOLDL,
        "Mast, bhari-bhari,",
        "Chole Bhature.",
        GOLD2,
        "Phulli hui bhature, ghanton ka pakaya hua chole. Pune mein yahi plate sabse zyada "
        "banti hai. Ek baar khao, baar baar aao.",
        big_font=114
    )


def aloo_tikki():
    """Aloo Tikki Chaat — evening counter, chaat culture post."""
    B.photo_poster(
        "post-d2-aloo-tikki.jpg",
        A("new-aloo-tikki.jpg"),
        "Shaam ke baad, Baner mein",
        TEAL2,
        "Crisp tikki,",
        "asli chaat.",
        GOLD2,
        "Crisp tikki, thick dahi, imli ki chutney, sev aur anaar. Yahi Mathura ka chaat "
        "andaaz hai. Evening ke baad outlet pe isko hi sabse zyada maanga jaata hai.",
        big_font=130
    )


def mathura_peda():
    """Mathura Peda — the heritage and gifting story. Dark, reverent."""
    W, H = 1080, 1080
    c = Image.new("RGBA", (W, H), NAVYD + (255,))
    c.alpha_composite(B.vgrad(W, H, NAVY, NAVYD, 255, 255), (0, 0))

    # warm glow from centre
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 380, H // 2 - 320, W // 2 + 380, H // 2 + 320], fill=55)
    import PIL.ImageFilter as IF
    glow = glow.filter(IF.GaussianBlur(180))
    warm = Image.new("RGBA", (W, H), (201, 138, 30, 255))
    c = Image.composite(warm, c, glow)

    d = ImageDraw.Draw(c)
    d.rectangle([38, 38, W - 38, H - 38], outline=GOLD2, width=2)
    cx = W // 2

    # feather
    fw = B.feather(130).width
    B.paste_feather(c, 130, (cx - fw // 2, 72), alpha=240)

    y = 270
    y = B.kicker(d, cx, y, "Mathura ka sabse famous meetha", GOLDL)
    y += 68
    B.centered(d, ["Mathura Peda."], B.f_serif(108), cx, y, GOLD2, 116)
    y += 150
    B.centered(d, ["Seedha khoya se, thodi si khashat,"], B.f_serif_r(44), cx, y, CREAM, 60)
    y += 68
    B.centered(d, ["aur puri Mathura ki khushboo."], B.f_serif_r(44), cx, y, CREAM, 60)
    y += 90

    body = ("Jab duniya nahi jaanti thi freeze karna, tab bhi Mathura peda "
            "banta tha. Fresh khoya, desi ghee, haath se banaya. "
            "Gifting ke liye order karein: ₹700 per kg.")
    cf = B.f_geo(31)
    for ln in B.wrap(d, body, cf, W - 240):
        w = d.textlength(ln, font=cf)
        d.text((cx - w / 2 + 1, y + 1), ln, font=cf, fill=(0, 0, 0, 140))
        d.text((cx - w / 2, y), ln, font=cf, fill=(218, 227, 237))
        y += 46
    y += 18
    B.dotrow(d, cx, y, GOLD2)

    B.place_logo(c, light=True, h=52)
    B.save(c, "post-d2-mathura-peda.jpg")


def no_onion():
    """Educational post: why no onion/garlic in Mathura's chaat. Dark typographic."""
    W, H = 1080, 1080
    c = Image.new("RGBA", (W, H), NAVYD + (255,))
    c.alpha_composite(B.vgrad(W, H, (10, 24, 42), NAVYD, 255, 255), (0, 0))

    # teal glow
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W // 2 - 340, H // 2 - 300, W // 2 + 340, H // 2 + 300], fill=50)
    import PIL.ImageFilter as IF
    glow = glow.filter(IF.GaussianBlur(160))
    tl = Image.new("RGBA", (W, H), TEAL + (255,))
    c = Image.composite(tl, c, glow)

    d = ImageDraw.Draw(c)
    d.rectangle([38, 38, W - 38, H - 38], outline=(21, 131, 126, 220), width=2)
    cx = W // 2

    # feather top
    fw = B.feather(120).width
    B.paste_feather(c, 120, (cx - fw // 2, 80), alpha=230)

    y = 260
    y = B.kicker(d, cx, y, "Braj cuisine ka ek raaz", TEAL2)
    y += 62
    B.centered(d, ["Pyaaz nahi."], B.f_serif(118), cx, y, GOLD2, 128)
    y += 140
    B.centered(d, ["Lahsun nahi."], B.f_serif(118), cx, y, GOLDL, 128)
    y += 148

    body = ("Mathura aur Vrindavan mein sadiyoon se khana banta hai "
            "bina pyaaz aur lahsun ke. Yeh koi rule nahi, yeh Braj "
            "ki pehchaan hai. Sattvik, Krishna ka bhog. "
            "Isliye hamare kachori, bedai aur chaat mein bhi nahi hoga.")
    cf = B.f_geo(30)
    for ln in B.wrap(d, body, cf, W - 240):
        w = d.textlength(ln, font=cf)
        d.text((cx - w / 2 + 1, y + 1), ln, font=cf, fill=(0, 0, 0, 130))
        d.text((cx - w / 2, y), ln, font=cf, fill=(205, 216, 228))
        y += 44
    y += 22
    B.dotrow(d, cx, y, TEAL2)
    y += 46
    tag = "Braj Kitchen · brajfood"
    ft = B.f_sans(22)
    tw = B.text_w(d, tag.upper(), ft, 5)
    B.draw_ls(d, (cx - tw / 2, y), tag.upper(), ft, (120, 148, 170), 5)

    B.place_logo(c, light=True, h=50)
    B.save(c, "post-d2-no-onion.jpg")


if __name__ == "__main__":
    chole_bhature()
    aloo_tikki()
    mathura_peda()
    no_onion()
    print("drop-02 done")
