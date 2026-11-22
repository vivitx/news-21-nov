"""Draw the 21 November 2026 world-news image (1024x1024) with PIL.

Run: python3 draw.py  ->  writes entry.png next to this file.
Deterministic: fixed colours, fixed layout, no randomness, no timestamps.
The entry program (main.py) is stdlib-only and copies entry.png to the output dir;
this script is the in-session build tool that drew the image.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 232)
INK = (20, 24, 34)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREEN = (31, 111, 72)
BLUE = (24, 90, 158)
ORANGE = (204, 94, 20)
PURPLE = (94, 60, 144)
TEAL = (14, 110, 110)
GOLD = (176, 132, 16)
GREY = (90, 92, 98)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)


def f(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)


def rrect(d, box, fill, outline=None, radius=6, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill,
                        outline=outline, width=width)


def kicker(d, x, y, s, color):
    text(d, x, y, s, f(10, True), fill=color)


def headline(d, x, y, s, size, max_w, max_lines=3):
    lines = wrap(d, s, f(size, True), max_w)[:max_lines]
    yy = y
    for ln in lines:
        text(d, x, yy, ln, f(size, True), fill=INK)
        yy += size + 3
    return yy


def scene_flame(d, cx, cy, s):
    # simple flat flame: three stacked ellipses + triangle tongue
    d.polygon([(cx, cy - 26 * s), (cx + 14 * s, cy + 8 * s),
               (cx - 14 * s, cy + 8 * s)], fill=(232, 90, 20))
    d.ellipse([cx - 12 * s, cy - 6 * s, cx + 12 * s, cy + 18 * s],
              fill=(240, 160, 20))
    d.ellipse([cx - 6 * s, cy + 2 * s, cx + 6 * s, cy + 16 * s],
              fill=(250, 210, 60))


def scene_ship(d, x, y, w, h, hull=(40, 60, 90)):
    # flat ship: hull + containers + smoke
    d.polygon([(x, y + h * 0.55), (x + w, y + h * 0.55),
               (x + w * 0.85, y + h), (x + w * 0.15, y + h)], fill=hull)
    d.rectangle([x + w * 0.2, y + h * 0.28, x + w * 0.42, y + h * 0.55],
                fill=(200, 60, 40))
    d.rectangle([x + w * 0.46, y + h * 0.28, x + w * 0.68, y + h * 0.55],
                fill=(40, 120, 90))
    d.rectangle([x + w * 0.72, y + h * 0.18, x + w * 0.8, y + h * 0.55],
                fill=(230, 230, 220))


def scene_globe(d, cx, cy, r, sea=(70, 140, 190), land=(60, 150, 90)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=sea)
    d.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.1],
              fill=land)
    d.ellipse([cx + r * 0.1, cy + r * 0.15, cx + r * 0.6, cy + r * 0.6],
              fill=land)
    d.ellipse([cx - r * 0.2, cy - r * 0.15, cx + r * 0.25, cy + r * 0.2],
              fill=land)


def scene_quake(d, x, y, w, h):
    # seismograph zigzag
    pts = []
    import math
    n = 24
    for i in range(n + 1):
        px = x + w * i / n
        amp = (h * 0.42 if i in (9, 10, 11, 12, 13) else h * 0.12)
        py = y + h / 2 + (amp if i % 2 else -amp)
        pts.append((px, py))
    d.line(pts, fill=RED, width=3)
    d.line([(x, y + h / 2), (x + w, y + h / 2)], fill=GREY, width=1)


def scene_robot(d, cx, cy, s):
    d.rectangle([cx - 16 * s, cy - 12 * s, cx + 16 * s, cy + 14 * s],
                fill=(120, 130, 150))
    d.rectangle([cx - 10 * s, cy - 24 * s, cx + 10 * s, cy - 10 * s],
                fill=(160, 170, 190))
    d.ellipse([cx - 6 * s, cy - 20 * s, cx - 1 * s, cy - 15 * s], fill=RED)
    d.ellipse([cx + 1 * s, cy - 20 * s, cx + 6 * s, cy - 15 * s], fill=RED)
    d.line([(cx - 16 * s, cy), (cx - 26 * s, cy + 10 * s)], fill=INK, width=3)
    d.line([(cx + 16 * s, cy), (cx + 26 * s, cy + 10 * s)], fill=INK, width=3)


def scene_planet(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 120, 60))
    d.ellipse([cx - r, cy - r * 0.3, cx + r, cy + r * 0.3], fill=(150, 90, 40))
    d.ellipse([cx - r * 1.7, cy - r * 0.25, cx + r * 1.7, cy + r * 0.25],
              outline=(120, 120, 130), width=3)
    d.ellipse([cx + r * 1.15, cy - r * 1.15, cx + r * 1.35, cy - r * 0.95],
              fill=(220, 220, 230))


def scene_chart(d, x, y, w, h):
    pts = [(x, y + h * 0.25), (x + w * 0.3, y + h * 0.85),
           (x + w * 0.6, y + h * 0.6), (x + w, y + h * 0.15)]
    d.line(pts, fill=GREEN, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=GREEN)


def scene_ball(d, cx, cy, r):
    d.ellipse([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], fill=(150, 90, 40))
    d.line([(cx, cy - r * 0.72), (cx, cy + r * 0.72)], fill=LIGHT, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=LIGHT, width=3)


def scene_crowd(d, x, y, w, h):
    import math
    for i in range(9):
        cx = x + w * (0.1 + 0.1 * i)
        cy = y + h * (0.55 + 0.12 * math.sin(i * 1.7))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=NAVY)
        d.rectangle([cx - 7, cy + 6, cx + 7, cy + 16], fill=RED if i % 3 == 0 else BLUE)
    d.line([(x, y + h - 4), (x + w, y + h - 4)], fill=INK, width=2)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 84], fill=NAVY)
    text(d, 14, 10, "THE WORLD IN ONE DAY", f(12, True), fill=(150, 190, 240))
    text(d, 1010, 10, "DAY 325 OF 2026", f(12, True),
         fill=(150, 190, 240), anchor="ra")
    text(d, 14, 30, "Saturday 21 November 2026", f(38, True), fill=LIGHT)
    text(d, 1010, 44, "35 stories  ·  9 regions", f(14, True),
         fill=(220, 220, 220), anchor="ra")

    # ---- Stat strip -----------------------------------------------------
    stats = [("2", "tankers hit off Khasab"), ("DAY 13", "COP31, no deal yet"),
             ("11", "dead in Sinaloa raid"), ("M6.7", "Peru quake, 108 km deep"),
             ("128", "states on AI-arms rules"), ("37–12", "England beat All Blacks")]
    cw = (W - 24) / 6
    for i, (num, lab) in enumerate(stats):
        x = 12 + i * cw
        text(d, x + cw / 2, 90, num, f(20, True), fill=RED, anchor="ma")
        lines = wrap(d, lab, f(10), cw - 8)
        text(d, x + cw / 2, 114, lines[0] if lines else "", f(10),
             fill=INK, anchor="ma")

    # ---- Leads ----------------------------------------------------------
    leads = [
        ("MIDDLE EAST · WAR", RED, "Iran strikes Bahrain; tankers hit in Hormuz",
         "Bahrain says an Iranian strike set a site ablaze. Two tankers hit off Khasab.",
         "2 TANKERS", "ship"),
        ("ANTALYA · CLIMATE", GREEN, "COP31 runs into Day 13 overtime — still no deal",
         "Nearly 200 nations split over fossil fuels; the draft text omits them.",
         "DAY 13", "globe"),
        ("SINALOA · CRIME", PURPLE, "Mexico captures “El Chapo Isidro”",
         "FBI top-ten fugitive seized in Guasave; 4 soldiers and 7 gunmen killed.",
         "11 DEAD", "star"),
    ]
    lx = [12, 350, 688]
    for (kick, col, head, summ, big, kind), x in zip(leads, lx):
        rrect(d, [x, 132, x + 324, 372], fill=CARD, outline=(200, 196, 180))
        d.rectangle([x, 132, x + 324, 160], fill=col)
        text(d, x + 10, 139, kick, f(11, True), fill=LIGHT)
        sy = 168
        if kind == "ship":
            d.rectangle([x + 10, sy, x + 314, sy + 74], fill=(170, 210, 230))
            scene_ship(d, x + 30, sy + 12, 130, 46)
            scene_flame(d, x + 230, sy + 34, 1.0)
            scene_flame(d, x + 272, sy + 44, 0.7)
            text(d, x + 196, sy + 52, "KHASAB", f(10, True), fill=NAVY)
        elif kind == "globe":
            scene_globe(d, x + 70, sy + 38, 34)
            d.ellipse([x + 150, sy + 6, x + 214, sy + 70], outline=GREEN, width=4)
            text(d, x + 182, sy + 28, "13", f(24, True), fill=GREEN, anchor="ma")
            text(d, x + 240, sy + 16, "NO DEAL", f(13, True), fill=RED)
            text(d, x + 240, sy + 38, "~200 nations", f(11), fill=INK)
            text(d, x + 240, sy + 54, "split on fossil", f(11), fill=INK)
            text(d, x + 240, sy + 68, "fuels", f(11), fill=INK)
        else:
            d.ellipse([x + 36, sy + 8, x + 104, sy + 76], fill=(240, 200, 60))
            text(d, x + 70, sy + 26, "★", f(30, True), fill=PURPLE, anchor="ma")
            text(d, x + 130, sy + 14, "FBI TOP TEN", f(12, True), fill=RED)
            text(d, x + 130, sy + 34, "CAPTURED", f(16, True), fill=INK)
            text(d, x + 130, sy + 56, "Guasave, Sinaloa", f(11), fill=INK)
        yy = headline(d, x + 10, 252, head, 19, 304, 2)
        lines = wrap(d, summ, f(11), 304)
        for ln in lines[:2]:
            text(d, x + 10, yy + 2, ln, f(11), fill=GREY)
            yy += 15
        text(d, x + 10, 340, big, f(22, True), fill=col)

    # ---- Mediums --------------------------------------------------------
    mediums = [
        ("PERU · QUAKE", "M6.7 quake shakes central Peru", "00:09 UTC · 108 km deep",
         "M6.7", RED, "quake"),
        ("GULF OF FINLAND", "Drones set Russian ship Sparta II ablaze", "16 crew taken off",
         "16 SAFE", NAVY, "ship"),
        ("GENEVA · AI ARMS", "128 states agree to draft AI-weapon rules", "Rules by 2028, no ban yet",
         "128", TEAL, "robot"),
        ("EU · INDONESIA", "EU and Indonesia sign trade pact", "98.5% of EU tariff lines cut",
         "98.5%", BLUE, "pact"),
        ("SPACE · MERCURY", "BepiColombo enters orbit around Mercury", "37-min burn from 18:24 UTC",
         "18:24", GOLD, "planet"),
        ("BANDA SEA · QUAKE", "M6.8 quake off Timor-Leste, felt in Darwin", "09:42 UTC · no tsunami",
         "M6.8", RED, "quake"),
        ("MARKETS · CRYPTO", "Bitcoin hits a two-year low, then rebounds", "Low $55,250 · back over $60,000",
         "$60,190", GREEN, "chart"),
        ("BASRA · FIRE", "Power-plant fire kills four in Basra", "30+ hurt · 800 MW plant halted",
         "4 DEAD", ORANGE, "flame"),
        ("TWICKENHAM · RUGBY", "England rout the All Blacks", "Record margin at Twickenham",
         "37–12", NAVY, "ball"),
        ("FRANCE · PROTEST", "Sixth Saturday of cost-of-living marches", "Ministry count in Paris and beyond",
         "82,500", PURPLE, "crowd"),
    ]
    for i, (kick, head, summ, big, col, kind) in enumerate(mediums):
        row, c = divmod(i, 5)
        x = 12 + c * 202
        y = 380 + row * 162
        rrect(d, [x, y, x + 192, y + 154], fill=CARD, outline=(200, 196, 180))
        kicker(d, x + 8, y + 6, kick, col)
        iy = y + 24
        if kind == "quake":
            scene_quake(d, x + 10, iy, 172, 40)
        elif kind == "ship":
            d.rectangle([x + 8, iy, x + 184, iy + 40], fill=(170, 210, 230))
            scene_ship(d, x + 30, iy + 4, 110, 32)
            scene_flame(d, x + 158, iy + 18, 0.7)
        elif kind == "robot":
            scene_robot(d, x + 96, iy + 20, 0.9)
        elif kind == "pact":
            d.rectangle([x + 20, iy + 6, x + 92, iy + 34], fill=BLUE)
            text(d, x + 56, iy + 12, "EU", f(14, True), fill=LIGHT, anchor="ma")
            d.rectangle([x + 100, iy + 6, x + 172, iy + 34], fill=(200, 40, 40))
            text(d, x + 136, iy + 12, "ID", f(14, True), fill=LIGHT, anchor="ma")
            text(d, x + 96, iy + 16, "×", f(14, True), fill=INK, anchor="ma")
        elif kind == "planet":
            scene_planet(d, x + 96, iy + 20, 16)
        elif kind == "chart":
            scene_chart(d, x + 14, iy + 2, 164, 36)
        elif kind == "flame":
            scene_flame(d, x + 96, iy + 20, 1.1)
        elif kind == "ball":
            scene_ball(d, x + 96, iy + 20, 26)
        elif kind == "crowd":
            scene_crowd(d, x + 14, iy, 164, 40)
        yy = headline(d, x + 8, y + 70, head, 12, 176, 2)
        text(d, x + 8, y + 102, big, f(19, True), fill=col)
        lines = wrap(d, summ, f(10), 176)
        text(d, x + 8, y + 128, lines[0] if lines else "", f(10), fill=GREY)
        if len(lines) > 1:
            text(d, x + 8, y + 141, lines[1], f(10), fill=GREY)

    # ---- Briefs ---------------------------------------------------------
    d.rectangle([0, 704, W, 728], fill=NAVY)
    text(d, 14, 710, "ALSO ON SATURDAY 21 NOVEMBER  —  22 MORE STORIES",
         f(12, True), fill=LIGHT)
    briefs = [
        ("GAZA", "Strike on food-aid vehicle kills 3."),
        ("KYIV", "Ballistic missiles hit Kyiv; 2 hurt, homes ablaze."),
        ("UST-LUGA", "Ukrainian drones hit Russian port; NATO jets up."),
        ("BRASÍLIA", "Bolsonaro moved to intensive care, 71, stable."),
        ("WELLINGTON", "India 486/4 v NZ — Rahul 136, Gill 98, lead 118."),
        ("NIGERIA", "Funeral-boat toll reaches 24 (toll given Sat)."),
        ("MANIPUR", "Toxic alcohol kills 11; ~180 poisoned."),
        ("JAVA", "Sweet-factory fire: 3 dead, 36 missing."),
        ("WASHINGTON", "Trump confirms FBI crime-database hack."),
        ("WASHINGTON", "Trump backs a 10% credit-card cap."),
        ("DUBLIN", "Ireland beat South Africa 20–17."),
        ("TURIN", "Alcaraz beats Shelton, into ATP final."),
        ("MELBOURNE", "Australia beat England by 3 wickets, 1st T20."),
        ("OSAKA", "BTS win 5 MAMA awards; Album of the Year."),
        ("ABUJA", "CAF makes Kiswahili official; 54 back Infantino."),
        ("TAIWAN", "21 Chinese jets in patrol; 15 cross median line."),
        ("FLORIDA", "Falcon 9 launches USSF-317 at 04:20 UTC."),
        ("RIYADH", "3 Houthi missiles downed, 02:43 Sat local time."),
        ("KRYVYI RIH", "Missile strike kills 2."),
        ("DAVAO", "Air Niugini jet lands safely; 146 aboard."),
        ("DHAKA", "Dozens of garment factories shut in wage protests."),
        ("ETHIOPIA", "~700,000 displaced by fighting in the south."),
    ]
    for i, (reg, s) in enumerate(briefs):
        col = i // 11
        row = i % 11
        x = 14 + col * 506
        y = 736 + row * 15
        d.ellipse([x, y + 3, x + 7, y + 10], fill=RED)
        text(d, x + 12, y, reg + ": ", f(11, True), fill=INK)
        w0 = d.textlength(reg + ": ", font=f(11, True))
        text(d, x + 12 + w0, y, s, f(11), fill=INK)

    # ---- Bottom: timeline + date check ----------------------------------
    rrect(d, [12, 904, 612, 1012], fill=CARD, outline=(200, 196, 180))
    text(d, 22, 910, "THE DAY IN UTC", f(11, True), fill=NAVY)
    tl = [("00:09", "Peru M6.7"), ("02:00", "Sinaloa raid"),
          ("04:20", "Falcon 9"), ("05:00", "Tanker hit"),
          ("06:50", "Sparta II"), ("09:42", "Banda Sea M6.8"),
          ("13:30", "Bitcoin $60k"), ("18:24", "Mercury burn"),
          ("22:10", "COP31 pauses")]
    for i, (t, lab) in enumerate(tl):
        col = i // 5
        row = i % 5
        x = 22 + col * 300
        y = 930 + row * 15
        text(d, x, y, t, f(11, True), fill=RED)
        text(d, x + 52, y, lab, f(11), fill=INK)
    rrect(d, [622, 904, 1012, 1012], fill=(255, 248, 220),
          outline=(200, 170, 90))
    text(d, 632, 910, "DATE CHECK — LEFT OUT ON PURPOSE", f(11, True), fill=RED)
    dc = ("Friday 20 Nov: Poland missiles · Denmark expels attaché · "
          "ICJ Myanmar ruling · UK–EU deal · Wall Street sell-off · "
          "Akvan landfall. Not yet: COP31 final vote · Las Vegas GP · "
          "Alcaraz–Zverev final. Riyadh missiles shown in local time.")
    lines = wrap(d, dc, f(10), 370)
    yy = 930
    for ln in lines[:5]:
        text(d, 632, yy, ln, f(10), fill=INK)
        yy += 14

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote", os.path.join(HERE, "entry.png"),
          os.path.getsize(os.path.join(HERE, "entry.png")), "bytes")


if __name__ == "__main__":
    build()
