"""Stamp a clean, readable banner on each park image.

The original GIS+Gemini renders have all labels at tiny font sizes that vanish
at 400px-wide thumbnails. This script adds a large overlay banner at the top of
each image with the park name and the neighborhood it protects.
"""
import os
from PIL import Image, ImageDraw, ImageFont

PARKS = [
    ("park-01-topanga-crest.png", "1", "Topanga Crest", "PHASE 1", "Pacific Palisades  |  Sunset Mesa  |  Castellammare"),
    ("park-02-sullivan-canyon.png", "2", "Sullivan Canyon Top", "PHASE 1", "Brentwood  |  Brentwood Park  |  Kenter Canyon"),
    ("park-03-mandeville-ridge.png", "3", "Mandeville Ridge", "PHASE 1", "Mandeville Canyon"),
    ("park-04-sepulveda-crown.png", "4", "Sepulveda Crown", "PHASE 1", "Bel-Air east of the 405  |  Casiano  |  Roscomare  |  Getty Center"),
    ("park-05-stone-canyon.png", "5", "Stone Canyon", "PHASE 1", "Bel-Air east"),
    ("park-06-beverly-glen.png", "6", "Beverly Glen Top", "PHASE 1", "Lower Beverly Glen  |  Bel-Air east  |  Holmby Hills"),
    ("park-07-fryman-upper.png", "7", "Fryman Upper", "PHASE 1", "Studio City south of Mulholland  |  Sherman Oaks east"),
    ("park-08-coldwater-canyon.png", "8", "Coldwater Canyon", "PHASE 2", "Studio City south  |  Beverly Hills north slopes  |  Benedict Canyon"),
    ("park-09-runyon-canyon.png", "9", "Runyon Canyon", "PHASE 2", "Hollywood  |  West Hollywood  |  Sunset Strip"),
    ("park-10-cahuenga-peak.png", "10", "Cahuenga Peak", "PHASE 2", "Hollywood north slope  |  Lake Hollywood  |  Toluca Lake"),
    ("park-11-will-rogers-ridge.png", "11", "Will Rogers Ridge", "PHASE 2", "Pacific Palisades east"),
    ("park-12-wilacre.png", "12", "Wilacre", "PHASE 2  -  DEMO PROJECT", "Studio City  |  Sherman Oaks east"),
]

HERE = os.path.dirname(os.path.abspath(__file__))
DARK = (28, 25, 23)
GOLD = (154, 124, 46)
BLUE = (30, 58, 95)
WHITE = (255, 255, 255)

FONT_PATH_BOLD = "C:\\Windows\\Fonts\\georgiab.ttf"
FONT_PATH_REG = "C:\\Windows\\Fonts\\georgia.ttf"


def banner(park_no, name, phase, protects, width=1376):
    h_top = 220
    img = Image.new("RGB", (width, h_top), WHITE)
    draw = ImageDraw.Draw(img)
    f_no = ImageFont.truetype(FONT_PATH_BOLD, 28)
    f_phase = ImageFont.truetype(FONT_PATH_BOLD, 22)
    f_name = ImageFont.truetype(FONT_PATH_BOLD, 88)
    f_pro_label = ImageFont.truetype(FONT_PATH_BOLD, 18)
    f_pro = ImageFont.truetype(FONT_PATH_REG, 26)

    pad = 30
    draw.text((pad, pad), f"PARK {park_no} OF 12", fill=BLUE, font=f_no)
    phase_color = BLUE if "PHASE 1" in phase and "DEMO" not in phase else (GOLD if "PHASE 2" in phase else DARK)
    if "DEMO" in phase:
        phase_color = DARK
    draw.text((width - pad, pad), phase, fill=phase_color, font=f_phase, anchor="ra")
    draw.text((pad, pad + 38), name, fill=DARK, font=f_name)
    draw.text((pad, pad + 138), "PROTECTS", fill=BLUE, font=f_pro_label)
    draw.text((pad, pad + 158), protects, fill=DARK, font=f_pro)
    bar_h = 4
    draw.rectangle((0, h_top - bar_h, width, h_top), fill=DARK)
    return img


def stack(park_file, banner_img):
    base = Image.open(os.path.join(HERE, park_file)).convert("RGB")
    if base.width != banner_img.width:
        ratio = banner_img.width / base.width
        base = base.resize((banner_img.width, int(base.height * ratio)), Image.LANCZOS)
    out = Image.new("RGB", (banner_img.width, banner_img.height + base.height), WHITE)
    out.paste(banner_img, (0, 0))
    out.paste(base, (0, banner_img.height))
    return out


def main():
    for fname, pno, name, phase, protects in PARKS:
        b = banner(pno, name, phase, protects)
        out = stack(fname, b)
        out.save(os.path.join(HERE, fname), optimize=True)
        print(f"OK {fname}: {out.size}")


if __name__ == "__main__":
    main()
