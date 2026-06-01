#!/usr/bin/env python3
"""
Mathurawala festival creatives.
Brand: cream/navy/teal/gold + mor-pankh. Fraunces-style serif (Didot/Georgia) headlines.
Outputs 1080x1080 / 1080x1350 JPGs to this folder.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
def A(*p): return os.path.join(HERE, *p)

# ---- palette ----
CREAM  = (246, 234, 203)
CREAM2 = (251, 243, 223)
PAPER  = (254, 251, 243)
NAVY   = (16, 36, 60)
NAVYD  = (9, 21, 36)
TEAL   = (21, 131, 126)
TEAL2  = (30, 163, 154)
GOLD   = (201, 138, 30)
GOLD2  = (224, 165, 46)
GOLDL  = (239, 199, 114)
MAROON = (138, 45, 42)
WHITE  = (255, 255, 255)

# ---- fonts ----
SERIF   = "/System/Library/Fonts/Supplemental/Didot.ttc"          # high-contrast display serif
SERIF_G = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_GB= "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
SERIF_GI= "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS    = "/System/Library/Fonts/Supplemental/Futura.ttc"
SANS_F  = "/System/Library/Fonts/HelveticaNeue.ttc"

def font(path, size, idx=0):
    try:
        return ImageFont.truetype(path, size, index=idx)
    except Exception:
        return ImageFont.truetype(SERIF_G, size)

def f_serif(sz):   return font(SERIF, sz, 1)   # Didot bold
def f_serif_r(sz): return font(SERIF, sz, 0)   # Didot regular
def f_geo(sz):     return font(SERIF_G, sz)
def f_geob(sz):    return font(SERIF_GB, sz)
def f_geoi(sz):    return font(SERIF_GI, sz)
def f_sans(sz):    return font(SANS_F, sz, 0)

# ---- feather motif (extracted coloured mor-pankh from logo-light.png) ----
def feather(h):
    src = Image.open(A("new","logo-light.png")).convert("RGBA")
    # the coloured feather sits top-right; crop generously
    w0, h0 = src.size  # 2200x400
    crop = src.crop((int(w0*0.86), 0, w0, int(h0*0.62)))
    # keep only coloured (non-white) px so we drop the white wordmark fragments
    px = crop.load()
    cw, ch = crop.size
    for y in range(ch):
        for x in range(cw):
            r,g,b,a = px[x,y]
            if a < 20:
                continue
            mx, mn = max(r,g,b), min(r,g,b)
            sat = (mx-mn)
            # white-ish wordmark px -> drop; coloured feather -> keep
            if sat < 26 and mn > 150:
                px[x,y] = (r,g,b,0)
    crop = crop.crop(crop.getbbox())
    ratio = h / crop.height
    return crop.resize((int(crop.width*ratio), h), Image.LANCZOS)

# ---- helpers ----
def cover(img, tw, th):
    iw, ih = img.size
    s = max(tw/iw, th/ih)
    img = img.resize((int(iw*s)+1, int(ih*s)+1), Image.LANCZOS)
    iw, ih = img.size
    return img.crop(((iw-tw)//2, (ih-th)//2, (iw-tw)//2+tw, (ih-th)//2+th))

def vgrad(w, h, top, bot, top_a=255, bot_a=255):
    g = Image.new("RGBA",(1,h))
    for y in range(h):
        t=y/(h-1)
        g.putpixel((0,y),(int(top[0]+(bot[0]-top[0])*t),int(top[1]+(bot[1]-top[1])*t),
                           int(top[2]+(bot[2]-top[2])*t),int(top_a+(bot_a-top_a)*t)))
    return g.resize((w,h))

def text_w(d,s,fnt,ls=0):
    if ls==0:
        return d.textlength(s,font=fnt)
    return sum(d.textlength(c,font=fnt)+ls for c in s)-ls if s else 0

def draw_ls(d,xy,s,fnt,fill,ls):
    x,y=xy
    for c in s:
        d.text((x,y),c,font=fnt,fill=fill); x+=d.textlength(c,font=fnt)+ls

def wrap(d,s,fnt,maxw):
    out,line=[],""
    for wd in s.split():
        t=(line+" "+wd).strip()
        if d.textlength(t,font=fnt)<=maxw: line=t
        else:
            if line: out.append(line)
            line=wd
    if line: out.append(line)
    return out

def centered(d, lines, fnt, cx, y, fill, lh, shadow=None):
    for ln in lines:
        w=d.textlength(ln,font=fnt)
        if shadow:
            d.text((cx-w/2+shadow[0], y+shadow[1]), ln, font=fnt, fill=shadow[2])
        d.text((cx-w/2, y), ln, font=fnt, fill=fill); y+=lh
    return y

def kicker(d, cx, y, s, color, shadow=False):
    fk=f_sans(23)
    ls=7
    w=text_w(d,s.upper(),fk,ls)
    # flanking rules
    d.line([(cx-w/2-58,y+15),(cx-w/2-22,y+15)],fill=color,width=2)
    d.line([(cx+w/2+22,y+15),(cx+w/2+58,y+15)],fill=color,width=2)
    if shadow:
        draw_ls(d,(cx-w/2+1,y+1),s.upper(),fk,(0,0,0,160),ls)
    draw_ls(d,(cx-w/2,y),s.upper(),fk,color,ls)
    return y

def dotrow(d, cx, y, color):
    # small mor-pankh-eye dot ornament
    d.ellipse([cx-4,y-4,cx+4,y+4],fill=color)
    d.ellipse([cx-26,y-2,cx-22,y+2],fill=color)
    d.ellipse([cx+22,y-2,cx+26,y+2],fill=color)

def place_logo(canvas, light=True, h=58, y=None, cx=None):
    lg=Image.open(A("new","logo-light.png" if light else "logo-clean.png")).convert("RGBA")
    r=h/lg.height
    lg=lg.resize((int(lg.width*r),h),Image.LANCZOS)
    W,Hc=canvas.size
    if cx is None: cx=W//2
    if y is None: y=Hc-h-64
    canvas.alpha_composite(lg,(cx-lg.width//2,y))

def paste_feather(canvas, h, xy, alpha=255, flip=False):
    f=feather(h)
    if flip: f=ImageOps.mirror(f)
    if alpha<255:
        a=f.split()[3].point(lambda v:int(v*alpha/255)); f.putalpha(a)
    canvas.alpha_composite(f,xy)

def save(canvas, name):
    canvas.convert("RGB").save(A(name),"JPEG",quality=92)
    print("wrote",name,canvas.size)

# ====================================================================
# 1. RAKSHA BANDHAN — Malai Ghewar (typographic, navy+gold festive)
# ====================================================================
def rakhi():
    W,H=1080,1350
    c=Image.new("RGBA",(W,H),NAVY+(255,))
    # warm radial glow center
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W//2-560,H//2-560,W//2+560,H//2+560],fill=70)
    glow=glow.filter(ImageFilter.GaussianBlur(180))
    warm=Image.new("RGBA",(W,H),GOLD2+(255,)); c=Image.composite(warm,c,glow)
    d=ImageDraw.Draw(c)
    # thin gold inner frame
    d.rectangle([40,40,W-40,H-40],outline=GOLD2,width=2)
    d.rectangle([52,52,W-52,H-52],outline=(GOLD2[0],GOLD2[1],GOLD2[2]),width=1)
    cx=W//2
    paste_feather(c, 150, (cx-66, 132), alpha=255)
    y=320
    y=kicker(d,cx,y,"Rakhi · 28 August",GOLDL); y+=58
    big=f_serif(150)
    y=centered(d,["Bhai ka"],f_serif_r(74),cx,y,CREAM,84);
    centered(d,["GHEWAR"],big,cx,y,GOLD2,150)
    y+=176
    centered(d,["aaya hai."],f_serif_r(74),cx,y,CREAM,84); y+=126
    sub=f_geoi(33)
    for ln in ["Mathura ka malai ghewar, kesar, rabdi","aur chandi ke saath. Sirf Sawan bhar."]:
        w=d.textlength(ln,font=sub); d.text((cx-w/2,y),ln,font=sub,fill=(206,217,230)); y+=46
    y+=30
    dotrow(d,cx,y,TEAL2); y+=46
    # rakhi-box CTA chip
    chip="Rakhi gifting boxes · order on WhatsApp"
    fc=f_sans(25); cw=text_w(d,chip.upper(),fc,3)
    d.rounded_rectangle([cx-cw/2-30,y-2,cx+cw/2+30,y+52],radius=27,outline=GOLD2,width=2)
    draw_ls(d,(cx-cw/2,y+12),chip.upper(),fc,GOLD2,3)
    place_logo(c,light=True,h=54)
    save(c,"post-rakhi-ghewar.jpg")

# ====================================================================
# generic photo-hero poster (bottom text on gradient)
# ====================================================================
def photo_poster(name, photo, kick, kcol, line_small, line_big, big_col,
                 caption, logo_h=52, top_badge=None, big_font=120, frame=True,
                 H=1350, src_crop=None):
    W=1080
    src=Image.open(photo).convert("RGB")
    if src_crop:  # (l,t,r,b) fractions to trim baked-in captions/edges
        sw,sh=src.size
        src=src.crop((int(sw*src_crop[0]),int(sh*src_crop[1]),
                      int(sw*src_crop[2]),int(sh*src_crop[3])))
    base=cover(src,W,H).convert("RGBA")
    base=ImageEnhance.Contrast(base).enhance(1.04)
    base=ImageEnhance.Color(base).enhance(1.07)
    c=base
    # bottom dark gradient for text (taller + denser floor for kicker legibility)
    gh=int(H*0.66)
    grad=vgrad(W,gh,NAVYD,NAVYD,0,253)
    c.alpha_composite(grad,(0,H-gh))
    # extra solid floor band under the whole text block
    floor=int(H*0.40)
    c.alpha_composite(vgrad(W,floor,NAVYD,NAVYD,0,210),(0,H-floor))
    # subtle top scrim for badge legibility
    tg=vgrad(W,int(H*0.28),NAVYD,NAVYD,170,0)
    c.alpha_composite(tg,(0,0))
    d=ImageDraw.Draw(c)
    if frame:
        d.rectangle([34,34,W-34,H-34],outline=(GOLD2[0],GOLD2[1],GOLD2[2]),width=2)
    cx=W//2
    if top_badge:
        fb=f_sans(24); bw=text_w(d,top_badge.upper(),fb,5)
        by=70
        d.rounded_rectangle([cx-bw/2-26,by-4,cx+bw/2+26,by+48],radius=26,
                            fill=(MAROON[0],MAROON[1],MAROON[2],235))
        draw_ls(d,(cx-bw/2,by+10),top_badge.upper(),fb,CREAM,5)
    # text block bottom (raised to breathe above the logo)
    y=H-gh+int(gh*0.255)
    y=kicker(d,cx,y,kick,kcol,shadow=True); y+=58
    if line_small:
        centered(d,[line_small],f_serif_r(64),cx,y,CREAM,72,shadow=(2,2,(0,0,0,150))); y+=84
    bf=f_serif(big_font)
    bl=wrap(d,line_big,bf,W-150)
    y=centered(d,bl,bf,cx,y,big_col,int(big_font*1.02),shadow=(2,2,(0,0,0,150))); y+=26
    cf=f_geoi(31)
    for ln in wrap(d,caption,cf,W-200):
        w=d.textlength(ln,font=cf)
        d.text((cx-w/2+1,y+1),ln,font=cf,fill=(0,0,0,150))
        d.text((cx-w/2,y),ln,font=cf,fill=(218,227,237)); y+=42
    place_logo(c,light=True,h=logo_h)
    save(c,name)

# ====================================================================
# 2. JANMASHTAMI — the bhog (peda photo: already has bag+diya+feather)
# ====================================================================
def janmashtami_bhog():
    photo_poster("post-janmashtami-bhog.jpg", A("new","peda.png"),
        "Janmashtami · 4 September", GOLDL,
        "Mathura ka bhog,", "ab Pune mein.", GOLD2,
        "Sattvik prasad ki thali aur Mathura ka asli peda, jaisa Kanha ke ghar banta hai.",
        top_badge="The one day Bharat looks at Mathura", big_font=118,
        src_crop=(0.0,0.02,1.0,0.885))

# ====================================================================
# 5. MADE-LIVE always-on — bedai/kachori
# ====================================================================
def madelive():
    photo_poster("post-kachori-madelive.jpg", A("new-bedai-sabji.jpg"),
        "Made live · every morning", TEAL2,
        "Mathura ka", "asli nashta.", GOLD2,
        "Garam bedai, slow-cooked sabji. No machine, no frozen, bilkul ghar jaisa.",
        big_font=126)

# ====================================================================
# 6. JANMASHTAMI hamper / diaspora — premium feather box
# ====================================================================
def hamper():
    photo_poster("post-janmashtami-hamper.jpg", A("premium-box-feather.jpg"),
        "Janmashtami Prasad Hamper", GOLDL,
        "Ghar nahi ja paaye?", "Mathura bhej do.", GOLD2,
        "Peda, dhaniya panjiri aur mishri, Krishna ke sheher ka prasad, seedhe aapke parivaar tak.",
        top_badge="Ships across India", big_font=104)

# ====================================================================
# 3. JANMASHTAMI — Makhan Mishri (devotional, navy, educational)
# ====================================================================
def makhan_mishri():
    W,H=1080,1350
    c=Image.new("RGBA",(W,H),NAVYD+(255,))
    # gradient navy
    c.alpha_composite(vgrad(W,H,NAVY,NAVYD,255,255),(0,0))
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W//2-420,260,W//2+420,1100],fill=60)
    glow=glow.filter(ImageFilter.GaussianBlur(200))
    warm=Image.new("RGBA",(W,H),TEAL+(255,)); c=Image.composite(warm,c,glow)
    d=ImageDraw.Draw(c)
    d.rectangle([40,40,W-40,H-40],outline=GOLD2,width=2)
    cx=W//2
    fw=feather(150).width
    paste_feather(c,150,(cx-fw//2,140),alpha=255)
    y=360
    y=kicker(d,cx,y,"What Mathura eats on Janmashtami",TEAL2); y+=64
    centered(d,["Makhan-Mishri"],f_serif(104),cx,y,GOLD2,112); y+=150
    centered(d,["Kanha ka favourite."],f_serif_r(58),cx,y,CREAM,70); y+=130
    body=("White butter aur mishri, yahi Krishna ko sabse "
          "pyaara bhog hai. Iss Janmashtami, hum wahi banayenge, "
          "Mathura ke tareeke se. Bina pyaaz, bina lehsun, pure sattvik.")
    cf=f_geo(34)
    for ln in wrap(d,body,cf,W-260):
        w=d.textlength(ln,font=cf); d.text((cx-w/2,y),ln,font=cf,fill=(205,216,228)); y+=50
    y+=26
    dotrow(d,cx,y,GOLD2); y+=50
    tag="Bhog series · 1 of 8"
    ft=f_sans(24); tw=text_w(d,tag.upper(),ft,4)
    draw_ls(d,(cx-tw/2,y),tag.upper(),ft,(150,166,184),4)
    place_logo(c,light=True,h=54)
    save(c,"post-janmashtami-makhan-mishri.jpg")

# ====================================================================
# 4. GANESH CHATURTHI — Modak (Pune-local, square, teal+gold)
# ====================================================================
def modak():
    W,H=1080,1080
    c=Image.new("RGBA",(W,H),TEAL+(255,))
    c.alpha_composite(vgrad(W,H,(26,150,143),(15,95,91),255,255),(0,0))
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W//2-460,H//2-460,W//2+460,H//2+460],fill=66)
    glow=glow.filter(ImageFilter.GaussianBlur(160))
    warm=Image.new("RGBA",(W,H),GOLD2+(255,)); c=Image.composite(warm,c,glow)
    d=ImageDraw.Draw(c)
    d.rectangle([38,38,W-38,H-38],outline=CREAM,width=2)
    cx=W//2
    paste_feather(c,118,(cx-52,108),alpha=255)
    y=258
    y=kicker(d,cx,y,"Ganesh Chaturthi · 14 September",CREAM); y+=52
    centered(d,["Bappa ke liye,"],f_serif_r(60),cx,y,CREAM,72); y+=92
    centered(d,["MODAK"],f_serif(168),cx,y,(255,247,225),168); y+=196
    centered(d,["ghee mein, haath se banaye."],f_geoi(34),cx,y,(238,228,205),48); y+=92
    chip="Pune ka apna tyohaar · Mathura ka swad"
    fc=f_sans(24); cw=text_w(d,chip.upper(),fc,3)
    d.rounded_rectangle([cx-cw/2-28,y-2,cx+cw/2+28,y+50],radius=26,outline=CREAM,width=2)
    draw_ls(d,(cx-cw/2,y+13),chip.upper(),fc,CREAM,3)
    place_logo(c,light=True,h=50)
    save(c,"post-ganesh-modak.jpg")

if __name__=="__main__":
    rakhi()
    janmashtami_bhog()
    makhan_mishri()
    modak()
    madelive()
    hamper()
    print("done")
