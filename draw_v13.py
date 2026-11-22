"""Draw the 21 November 2026 world-news image (1024x1024) — v13.

The all-flat pass, matching rank 3 (the user's chosen reference) as
closely as the genre allows. Rank 3's visual language, studied at 2x:
one flat graphic per story, the big number INSIDE the graphic, kicker
bar below the graphic, big headline, a 1-2 line deck, small sources.
No photos at all — the AI scenes are gone (the user called the images
"murahan" and rank 3 uses no photos).

Changes from v12:
- 8 new flat graphics: Mexico lead (CAPTURED stamp + $5M badge),
  Peru cross-section (mountain + dashed line + epicenter + 108-129 km),
  Sparta ship (flat hull + containers + 2 DRONES), Geneva robot
  (simple white robot + 128), Mercury planet + orbit (37 MIN BURN),
  Basra flames (4 DEAD IN FIRE), rugby field + scoreboard, France
  Eiffel Tower + 82,500. Brussels / Banda / Bitcoin keep the v12
  flat graphics, now with the big number inside.
- medium cards restructured to the rank-3 formula: 70px graphic with
  the big number inside, kicker, 2-line headline, 1-line deck (new,
  facts verified in content-2026-11-21.md), sources. The separate red
  stat line is gone.
- Gulf map + COP31 panel rescaled to the 100px lead graphic height
  (v11's versions assumed 132px and would break).
- vertical re-layout: leads 228px, mediums 162px x2, map+briefs
  176px (briefs stay 10pt, 13px rows from v12), bottom boxes + footer
  unchanged in content.
- Bitcoin big number corrected to $55,250 (the triangulated consensus
  in content-2026-11-21.md; v12 used $55,100, the bottom of the range).
Run: python3 draw_v13.py  ->  writes entry_v13.png next to this file.
Deterministic: fixed colours, fixed layout, fixed seed, no timestamps.
"""
import os
from PIL import Image, ImageDraw

from draw import (f, fs, text, headline, PAPER, INK, RED, GREEN, BLUE,
                  LIGHT, GOLD, quake_line, flame, dashed_line)
from draw_v11 import card_sq, kicker_bar
from draw_v12 import world_map_v12

W, H = 1024, 1024


def gulf_map_v13(d, x0, y0, x1, y1):
    """Clean flat Gulf, rescaled for a 100px-tall box (v11's version
    assumed 132px: its Arabia bulge crossed Iran's coast at 100px)."""
    SEA = (58, 118, 170)
    LAND = (214, 196, 158)
    LANDTXT = (96, 84, 60)
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 30), (x0 + 265, y0 + 32),
               (x0 + 235, y0 + 36), (x0 + 180, y0 + 40), (x0 + 100, y0 + 42),
               (x0 + 40, y0 + 40), (x0, y0 + 36)], fill=LAND)
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 18), (x0 + 265, y1 - 38),
               (x0 + 235, y1 - 52), (x0 + 180, y1 - 36), (x0 + 100, y1 - 28),
               (x0 + 40, y1 - 22), (x0, y1 - 24)], fill=LAND)
    bx, by = x0 + 105, y0 + 56
    d.ellipse([bx - 5, by - 3, bx + 5, by + 3], fill=LAND)
    import math
    pts = []
    for i in range(8):
        ang = math.pi * i / 4 - math.pi / 2
        rr = 8 if i % 2 == 0 else 3.5
        pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    d.polygon(pts, fill=RED)
    text(d, x0 + 14, y0 + 8, "IRAN", f(10, True), fill=LANDTXT)
    text(d, x0 + 14, y1 - 16, "ARABIA", f(9, True), fill=LANDTXT)
    text(d, bx + 14, by - 11, "BAHRAIN", f(10, True), fill=LIGHT)
    text(d, bx + 14, by + 2, "SITE ABLAZE", f(8, True), fill=LIGHT)
    chip = "2 TANKERS HIT"
    cw = len(chip) * 5 + 12
    cx0 = x1 - cw - 8
    d.rectangle([cx0, y0 + 48, cx0 + cw, y0 + 62], fill=RED)
    text(d, cx0 + cw / 2, y0 + 50, chip, f(8, True), fill=LIGHT, anchor="ma")


def cop_panel_v13(d, x0, y0, x1, y1):
    """Clean flat COP31 panel, compressed for a 100px-tall box."""
    text(d, x0, y0 + 4, "DAY 13 OF A 12-DAY SUMMIT", f(11, True), fill=INK)
    chip = "+1 DAY"
    cw = len(chip) * 5 + 12
    d.rectangle([x1 - cw, y0 + 2, x1, y0 + 16], fill=RED)
    text(d, x1 - cw / 2, y0 + 4, chip, f(8, True), fill=LIGHT, anchor="ma")
    for i, day in enumerate(range(9, 22)):
        bx = x0 + i * 23
        is21 = day == 21
        d.rectangle([bx, y0 + 22, bx + 21, y0 + 42],
                    fill=RED if is21 else LIGHT,
                    outline=(180, 176, 160))
        text(d, bx + 10.5, y0 + 28, str(day), f(9, True),
             fill=LIGHT if is21 else INK, anchor="ma")
    text(d, x0, y0 + 50, "NO DEAL", fs(15), fill=RED)
    text(d, x0 + 82, y0 + 54, "— draft omits fossil fuels", fs(12), fill=INK)
    text(d, x0, y0 + 70, "~200 nations · talks paused overnight", f(10))
    text(d, x0, y0 + 86, "EU and Pacific states reject the draft", f(10))
    d.line([x0, y1 - 4, x1, y1 - 4], fill=(200, 196, 180), width=1)


def mexico_lead_v13(d, x, iy):
    """Flat CAPTURED badge graphic for the Mexico lead (308x100)."""
    d.rectangle([x + 8, iy, x + 316, iy + 100], fill=(245, 232, 200))
    # $5M silhouette badge (left)
    d.rectangle([x + 14, iy + 16, x + 74, iy + 84], fill=LIGHT,
                outline=(180, 176, 160))
    text(d, x + 44, iy + 20, "$5M", f(13, True), fill=RED, anchor="ma")
    d.ellipse([x + 35, iy + 40, x + 53, iy + 58], fill=INK)
    d.rounded_rectangle([x + 30, iy + 60, x + 58, iy + 80], radius=8, fill=INK)
    # CAPTURED stamp (centre)
    d.rectangle([x + 92, iy + 18, x + 292, iy + 56], outline=RED, width=2)
    text(d, x + 192, iy + 24, "CAPTURED", fs(26), fill=RED, anchor="ma")
    text(d, x + 192, iy + 62, "FBI TOP TEN", f(10, True), fill=INK, anchor="ma")
    d.rectangle([x + 147, iy + 78, x + 237, iy + 94], fill=RED)
    text(d, x + 192, iy + 80, "11 DEAD", f(10, True), fill=LIGHT, anchor="ma")


def peru_v13(d, x, iy):
    """Flat quake cross-section (176x70): mountain, dashed line down
    to the epicentre, rings, 108-129 km chip."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(250, 244, 230))
    d.polygon([(x + 8, iy + 22), (x + 90, iy + 2), (x + 184, iy + 22)],
              fill=(120, 85, 50))
    d.rectangle([x + 8, iy + 22, x + 184, iy + 70], fill=(150, 115, 75))
    d.line([x + 8, iy + 40, x + 184, iy + 40], fill=(120, 90, 55), width=1)
    d.line([x + 8, iy + 56, x + 184, iy + 56], fill=(120, 90, 55), width=1)
    dashed_line(d, (x + 95, iy + 22), (x + 95, iy + 56), LIGHT, width=2)
    text(d, x + 101, iy + 26, "ONDORES", f(7, True), fill=LIGHT)
    d.ellipse([x + 85, iy + 46, x + 105, iy + 66], outline=RED, width=1)
    d.ellipse([x + 90, iy + 51, x + 100, iy + 61], outline=RED, width=1)
    d.ellipse([x + 91, iy + 52, x + 99, iy + 60], fill=RED)
    d.rectangle([x + 128, iy + 52, x + 182, iy + 66], fill=INK)
    text(d, x + 155, iy + 55, "108–129 km", f(8, True), fill=LIGHT, anchor="ma")


def sparta_v13(d, x, iy):
    """Flat cargo ship at night (176x70) + big 2 DRONES."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(18, 38, 68))
    d.polygon([(x + 14, iy + 42), (x + 100, iy + 42), (x + 92, iy + 58),
               (x + 22, iy + 58)], fill=(10, 12, 16))
    for j, col in enumerate([(210, 60, 50), (40, 90, 160), (50, 140, 80),
                             (230, 190, 60)]):
        d.rectangle([x + 20 + j * 16, iy + 34, x + 32 + j * 16, iy + 42],
                    fill=col)
    d.rectangle([x + 86, iy + 36, x + 96, iy + 42], fill=LIGHT)
    d.ellipse([x + 52, iy + 12, x + 60, iy + 20], fill=(120, 120, 120))
    d.ellipse([x + 62, iy + 8, x + 72, iy + 18], fill=(120, 120, 120))
    flame(d, x + 62, iy + 30, 0.55)
    text(d, x + 125, iy + 8, "2", fs(28), fill=LIGHT)
    text(d, x + 125, iy + 42, "DRONES", f(9, True), fill=LIGHT)


def geneva_v13(d, x, iy):
    """Flat white robot (176x70) + big 128 NATIONS."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(28, 58, 115))
    d.line([x + 42, iy + 8, x + 42, iy + 14], fill=LIGHT, width=2)
    d.ellipse([x + 40, iy + 6, x + 44, iy + 10], fill=RED)
    d.rounded_rectangle([x + 28, iy + 14, x + 56, iy + 32], radius=4, fill=LIGHT)
    d.ellipse([x + 34, iy + 21, x + 39, iy + 26], fill=RED)
    d.ellipse([x + 45, iy + 21, x + 50, iy + 26], fill=RED)
    d.rounded_rectangle([x + 24, iy + 36, x + 60, iy + 62], radius=4, fill=LIGHT)
    for j, col in enumerate([(220, 80, 60), (60, 180, 80), (60, 120, 220)]):
        d.ellipse([x + 32 + j * 8, iy + 46, x + 37 + j * 8, iy + 51], fill=col)
    d.rectangle([x + 16, iy + 40, x + 22, iy + 54], fill=LIGHT)
    d.rectangle([x + 62, iy + 40, x + 68, iy + 54], fill=LIGHT)
    text(d, x + 95, iy + 10, "128", fs(28), fill=LIGHT)
    text(d, x + 95, iy + 44, "NATIONS", f(9, True), fill=LIGHT)


def mercury_v13(d, x, iy):
    """Flat planet + orbit (176x70) + big 37 MIN BURN."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(14, 17, 26))
    for (sx, sy) in [(20, 10), (60, 8), (150, 12), (170, 30), (90, 60),
                     (30, 60), (140, 58), (110, 8)]:
        d.ellipse([x + sx - 1, iy + sy - 1, x + sx + 1, iy + sy + 1], fill=LIGHT)
    d.ellipse([x - 10, iy + 15, x + 100, iy + 55], outline=(150, 150, 160),
              width=1)
    d.ellipse([x + 28, iy + 18, x + 62, iy + 52], fill=(185, 120, 60))
    d.ellipse([x + 36, iy + 26, x + 44, iy + 34], fill=(140, 85, 40))
    d.ellipse([x + 93, iy + 18, x + 97, iy + 22], fill=LIGHT)
    text(d, x + 120, iy + 10, "37", fs(28), fill=LIGHT)
    text(d, x + 120, iy + 44, "MIN BURN", f(9, True), fill=LIGHT)


def basra_v13(d, x, iy):
    """Flat plant fire (176x70) + big 4 DEAD IN FIRE."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(35, 28, 22))
    d.rectangle([x + 14, iy + 44, x + 70, iy + 70], fill=(20, 18, 16))
    d.rectangle([x + 58, iy + 28, x + 66, iy + 70], fill=(20, 18, 16))
    flame(d, x + 35, iy + 48, 0.9)
    flame(d, x + 55, iy + 44, 1.0)
    flame(d, x + 75, iy + 50, 0.8)
    text(d, x + 120, iy + 10, "4", fs(28), fill=(240, 120, 30))
    text(d, x + 120, iy + 44, "DEAD IN FIRE", f(9, True), fill=LIGHT)


def rugby_v13(d, x, iy):
    """Flat rugby field + scoreboard (176x70)."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(45, 125, 65))
    d.rectangle([x + 12, iy + 4, x + 180, iy + 66], outline=LIGHT, width=1)
    d.line([x + 96, iy + 4, x + 96, iy + 66], fill=LIGHT, width=1)
    d.line([x + 24, iy + 18, x + 24, iy + 52], fill=LIGHT, width=2)
    d.line([x + 36, iy + 18, x + 36, iy + 52], fill=LIGHT, width=2)
    d.line([x + 24, iy + 35, x + 36, iy + 35], fill=LIGHT, width=2)
    d.ellipse([x + 73, iy + 31, x + 87, iy + 39], fill=(150, 100, 50))
    d.rectangle([x + 115, iy + 12, x + 178, iy + 58], fill=(15, 15, 15))
    text(d, x + 122, iy + 16, "ENG", f(8, True), fill=LIGHT)
    text(d, x + 171, iy + 16, "NZL", f(8, True), fill=LIGHT, anchor="ra")
    text(d, x + 146, iy + 30, "37–12", fs(16), fill=(240, 200, 60), anchor="ma")


def france_v13(d, x, iy):
    """Flat Eiffel Tower (176x70) + big 82,500 MARCHERS."""
    # Eiffel Tower as a solid silhouette: dark triangle, two white
    # platform gaps, arch cut out of the base. (Line-drawn version
    # read as a bare letter A.)
    d.polygon([(x + 42, iy + 2), (x + 18, iy + 64), (x + 66, iy + 64)],
              fill=(60, 60, 60))
    d.rectangle([x + 32, iy + 24, x + 52, iy + 28], fill=LIGHT)
    d.rectangle([x + 26, iy + 44, x + 58, iy + 48], fill=LIGHT)
    d.ellipse([x + 33, iy + 50, x + 51, iy + 78], fill=LIGHT)
    text(d, x + 95, iy + 12, "82,500", fs(24), fill=INK)
    text(d, x + 95, iy + 42, "MARCHERS", f(9, True), fill=INK)
    d.rectangle([x + 95, iy + 56, x + 105, iy + 66], fill=(30, 60, 140))
    d.rectangle([x + 105, iy + 56, x + 115, iy + 66], fill=LIGHT,
                outline=(180, 176, 160))
    d.rectangle([x + 115, iy + 56, x + 125, iy + 66], fill=(210, 40, 40))


def brussels_v13(d, x, iy):
    """Two flag circles + big 98.5% (176x70)."""
    import math
    cy = iy + 35
    ecx = x + 32
    d.ellipse([ecx - 18, cy - 18, ecx + 18, cy + 18], fill=(20, 50, 140))
    for k in range(12):
        ang = 2 * math.pi * k / 12 - math.pi / 2
        sx = ecx + 12 * math.cos(ang)
        sy = cy + 12 * math.sin(ang)
        d.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(250, 220, 60))
    icx = x + 76
    d.ellipse([icx - 18, cy - 18, icx + 18, cy + 18], fill=(210, 40, 40))
    d.pieslice([icx - 18, cy - 18, icx + 18, cy + 18], 0, 180, fill=LIGHT)
    d.ellipse([icx - 18, cy - 18, icx + 18, cy + 18],
              outline=(180, 176, 160), width=1)
    text(d, x + 105, iy + 12, "98.5%", fs(22), fill=(24, 90, 158))
    text(d, x + 105, iy + 42, "TARIFF LINES", f(8, True), fill=INK)


def banda_v13(d, x, iy):
    """Flat seismograph line + big M6.8 (176x70)."""
    quake_line(d, x + 10, iy + 14, 95, 24)
    text(d, x + 115, iy + 14, "M6.8", fs(24), fill=RED)


def bitcoin_v13(d, x, iy):
    """Flat V-chart + big $55,250 (176x70). Consensus low from the
    triangulation; v12 used $55,100, the bottom of the range."""
    pts = [(x + 12, iy + 16), (x + 50, iy + 46), (x + 85, iy + 30),
           (x + 110, iy + 14)]
    d.line(pts, fill=GREEN, width=3)
    d.ellipse([pts[1][0] - 3, pts[1][1] - 3, pts[1][0] + 3, pts[1][1] + 3],
              fill=RED)
    d.ellipse([pts[3][0] - 3, pts[3][1] - 3, pts[3][0] + 3, pts[3][1] + 3],
              fill=GREEN)
    text(d, x + 116, iy + 16, "$55,250", fs(16), fill=GREEN)
    text(d, x + 116, iy + 42, "2-YEAR LOW", f(8, True), fill=INK)


def build_v13():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead ----
    text(d, 12, 3, "THE WORLD IN ONE DAY", f(10, True))
    text(d, 512, 3, "DAY 325 OF 2026", f(10, True), fill=RED, anchor="ma")
    text(d, 1012, 3, "ALL TIMES UTC", f(10, True), anchor="ra")
    d.line([12, 16, 1012, 16], fill=INK, width=1)
    text(d, 12, 20, "Saturday 21 November 2026", fs(58), fill=INK)
    d.line([12, 90, 1012, 90], fill=INK, width=2)
    text(d, 512, 94,
         "Iran strikes Bahrain as tankers hit in Hormuz   ◆   Drones set Russian ship ablaze off Finland   ◆   COP31 deadlocked over fossil fuels",
         fs(13), anchor="ma")

    # ---- UTC timeline (visual) ----
    d.rectangle([12, 112, 104, 140], fill=INK)
    text(d, 58, 114, "THE DAY", f(10, True), fill=LIGHT, anchor="ma")
    text(d, 58, 126, "IN UTC", f(10, True), fill=LIGHT, anchor="ma")
    d.line([120, 126, 1012, 126], fill=(180, 176, 160), width=1)
    events = [
        (0.15, "00:09", "Peru M6.7"),
        (2.0, "02:00", "Sinaloa raid"),
        (4.33, "04:20", "Falcon 9"),
        (6.83, "06:50", "Sparta II"),
        (9.7, "09:42", "Banda M6.8"),
        (18.4, "18:24", "Mercury burn"),
        (22.17, "22:10", "COP31 pauses"),
    ]
    for hour, t, lab in events:
        x = 120 + hour / 24 * 892
        d.ellipse([x - 4, 122, x + 4, 130], fill=RED)
        text(d, x, 110, t, f(9, True), anchor="ma")
        text(d, x, 134, lab, f(8), anchor="ma")

    # ---- stat strip: equal columns + dividers ----
    stats = [("2", "tankers hit\noff Khasab"),
             ("11", "dead in the\nSinaloa raid"),
             ("M6.7", "Peru quake,\n108 km deep"),
             ("128", "states agree\nAI-weapon rules"),
             ("37–12", "England beat\nAll Blacks"),
             ("98.5%", "EU tariff lines\ncut in pact")]
    bounds = [12, 179, 345, 512, 679, 845, 1012]
    for i, (num, lab) in enumerate(stats):
        x = bounds[i]
        text(d, x + 4, 154, num, fs(24), fill=RED)
        nw = d.textlength(num, font=fs(24))
        lx = x + 14 + nw
        for j, ln in enumerate(lab.split("\n")):
            text(d, lx, 158 + j * 12, ln, f(9))
    for bx in bounds[1:-1]:
        d.line([bx, 152, bx, 190], fill=(200, 196, 180), width=1)
    # region bar
    regions = [("Europe 9", (50, 90, 160)), ("Middle East 4", (190, 50, 45)),
               ("Americas 6", (50, 130, 80)), ("Africa 3", (210, 130, 40)),
               ("South Asia 2", (140, 80, 170)), ("East Asia 2", (40, 150, 160)),
               ("South-East Asia 3", (180, 140, 30)), ("Oceania 2", (40, 60, 120)),
               ("Global 4", (110, 110, 110))]
    text(d, 12, 196, "STORIES BY REGION", f(9, True))
    rx = 132
    for name, col in regions:
        w = len(name) * 5 + 10
        d.rectangle([rx, 194, rx + w, 208], fill=col)
        text(d, rx + w / 2, 198, name, f(8, True), fill=LIGHT, anchor="ma")
        rx += w + 5

    # ---- leads (3) ----
    leads = [
        (1, "MIDDLE EAST · BAHRAIN / HORMUZ", "gulf",
         "Iran strikes Bahrain as tankers hit in Hormuz",
         "Bahrain says an Iranian strike set a civilian site ablaze, no one hurt. UKMTO: two tankers hit off Khasab.",
         "AL JAZEERA · REUTERS · AFP · UKMTO", RED),
        (2, "GLOBAL · COP31, ANTALYA · CLIMATE", "cop",
         "COP31 deadlocked over fossil fuels in overtime",
         "A day past deadline, talks paused overnight. EU and Pacific states reject a draft omitting fossil fuels.",
         "BBC · AFP · FRANCE 24", (50, 90, 160)),
        (3, "AMERICAS · SINALOA · SECURITY", "mexico",
         "Mexico seizes 'El Chapo Isidro' in army raid",
         "Troops seize Fausto Isidro Meza Flores; 4 soldiers and 7 gunmen killed. FBI most-wanted, $5m reward.",
         "GUARDIAN · DW · NYT · FBI", (50, 130, 80)),
    ]
    for i, (num, kick, kind, head, summ, src, col) in enumerate(leads):
        x = 12 + i * 338
        card_sq(d, [x, 214, x + 324, 442])
        kicker_bar(d, x, 214, 324, num, kick, col, h=24, fsize=10)
        sy0, sy1 = 244, 344
        if kind == "gulf":
            gulf_map_v13(d, x + 8, sy0, x + 316, sy1)
        elif kind == "cop":
            cop_panel_v13(d, x + 8, sy0, x + 316, sy1)
        else:
            mexico_lead_v13(d, x, sy0)
        yy = headline(d, x + 8, 350, head, 20, 308, 2)
        yy = headline(d, x + 8, yy + 2, summ, 10, 308, 2)
        text(d, x + 8, yy + 2, src, f(8), fill=(120, 116, 104))

    # ---- mediums (10): rank-3 formula — flat graphic with the big
    # number inside, kicker, headline, 1-line deck, sources ----
    mediums = [
        (4, "PERU · QUAKE", "peru", "Deep 6.7 quake shakes Peru",
         "Felt in Lima; no deaths.", "USGS · ABC AUSTRALIA", (50, 130, 80)),
        (5, "GULF OF FINLAND", "sparta", "Drones set Russian cargo ship ablaze",
         "16 crew taken off.", "BBC · FRANCE 24", (50, 90, 160)),
        (6, "GENEVA · AI ARMS", "robot", "UN 'killer robot' talks end, rules by 2028",
         "US, Russia, Israel opposed.", "DW · GUARDIAN · NPR", (110, 110, 110)),
        (7, "BRUSSELS · TRADE", "flags", "EU and Indonesia sign trade pact",
         "Covers 730m people.", "DW · ANTARA", (50, 90, 160)),
        (8, "MERCURY · SCIENCE", "mercury", "BepiColombo enters orbit around Mercury",
         "Ends an 8-year journey.", "ESA · JAXA · SPACE.COM", (110, 110, 110)),
        (9, "BANDA SEA · QUAKE", "banda", "Deep quake shakes Timor-Leste",
         "Felt in Darwin; no tsunami.", "USGS · ABC AUSTRALIA", (180, 140, 30)),
        (10, "CRYPTO · MARKETS", "bitcoin", "Bitcoin dives, then rebounds",
         "Back over $60,000.", "COINBASE · REUTERS", (110, 110, 110)),
        (11, "BASRA · DISASTER", "basra", "Power-plant fire kills 4 in Basra",
         "800 MW halted; 30+ hurt.", "REUTERS", (190, 50, 45)),
        (12, "TWICKENHAM", "rugby", "England beat All Blacks by record margin",
         "A record margin.", "BBC · REUTERS · STUFF", (50, 90, 160)),
        (13, "FRANCE · PROTEST", "france", "Sixth Saturday of cost-of-living marches",
         "Organisers claim 150,000.", "AFP · FRANCE 24 · LE MONDE", (50, 90, 160)),
    ]
    for i, (num, kick, kind, head, deck, src, col) in enumerate(mediums):
        x = 12 + (i % 5) * 200
        y = 448 + (i // 5) * 168
        card_sq(d, [x, y, x + 192, y + 162])
        if kind == "peru":
            peru_v13(d, x, y + 6)
        elif kind == "sparta":
            sparta_v13(d, x, y + 6)
        elif kind == "robot":
            geneva_v13(d, x, y + 6)
        elif kind == "flags":
            brussels_v13(d, x, y + 6)
        elif kind == "mercury":
            mercury_v13(d, x, y + 6)
        elif kind == "banda":
            banda_v13(d, x, y + 6)
        elif kind == "bitcoin":
            bitcoin_v13(d, x, y + 6)
        elif kind == "basra":
            basra_v13(d, x, y + 6)
        elif kind == "rugby":
            rugby_v13(d, x, y + 6)
        elif kind == "france":
            france_v13(d, x, y + 6)
        kicker_bar(d, x, y + 82, 192, num, kick, col)
        headline(d, x + 8, y + 104, head, 13, 176, 2)
        text(d, x + 8, y + 140, deck, f(9))
        text(d, x + 192 - 8, y + 153, src, f(8), fill=(120, 116, 104), anchor="ra")

    # ---- map + briefs (briefs stay 10pt from v12) ----
    card_sq(d, [12, 784, 460, 960])
    text(d, 20, 788, "WHERE IT HAPPENED", f(11, True))
    text(d, 20, 802, "pin numbers match the stories; pin colour is the region",
         f(9), fill=(120, 116, 104))
    world_map_v12(d, 20, 816, 452, 956)
    text(d, 468, 788, "ALSO ON SATURDAY 21 NOVEMBER 2026", f(11, True))
    text(d, 468, 802, "22 more stories, in order of consequence",
         f(9), fill=(120, 116, 104))
    ME, EU, AM, AF, SA, EA, SEA, OC = ((190, 50, 45), (50, 90, 160), (50, 130, 80),
                                       (210, 130, 40), (140, 80, 170), (40, 150, 160),
                                       (180, 140, 30), (40, 60, 120))
    briefs = [
        (14, "GAZA", "Aid-vehicle strike kills 3.", "REUTERS", ME),
        (15, "KYIV", "Missiles hit Kyiv; 2 hurt.", "AP", EU),
        (16, "UST-LUGA", "Drones hit port; jets up.", "REUTERS", EU),
        (17, "BRASÍLIA", "Bolsonaro to ICU, stable.", "REUTERS", AM),
        (18, "WELLINGTON", "India 486/4, Rahul 136.", "BBC", OC),
        (19, "NIGERIA", "Boat toll reaches 24.", "AP", AF),
        (20, "MANIPUR", "Toxic alcohol kills 11.", "REUTERS", SA),
        (21, "JAVA", "Factory fire, 3 dead, 36 missing.", "BBC", SEA),
        (22, "WASHINGTON", "Trump confirms FBI hack.", "AP", AM),
        (23, "WASHINGTON", "Trump backs 10% card cap.", "AP", AM),
        (24, "DUBLIN", "Ireland 20–17 South Africa.", "BBC", EU),
        (25, "TURIN", "Alcaraz beats Shelton.", "ATP", EU),
        (26, "MELBOURNE", "Australia beat England.", "BBC", OC),
        (27, "OSAKA", "BTS win 5 MAMA awards.", "REUTERS", EA),
        (28, "ABUJA", "CAF backs Infantino.", "AFP", AF),
        (29, "TAIWAN", "21 jets; 15 cross line.", "AP", EA),
        (30, "FLORIDA", "Falcon 9 launches USSF-317.", "AP", AM),
        (31, "RIYADH", "3 Houthi missiles downed.", "AJ", ME),
        (32, "KRYVYI RIH", "Strike kills 2.", "REUTERS", EU),
        (33, "DAVAO", "Jet lands safely, 146 aboard.", "AP", SEA),
        (34, "DHAKA", "Factories shut in protests.", "TBS", SA),
        (35, "ETHIOPIA", "~700,000 displaced.", "AP", AF),
    ]
    for i, (num, region, s, src, col) in enumerate(briefs):
        col_i = i // 11
        row = i % 11
        bx = 468 + col_i * 276
        by = 816 + row * 13
        d.rectangle([bx, by, bx + 14, by + 13], fill=col)
        text(d, bx + 7, by + 1, str(num), f(8, True), fill=LIGHT, anchor="ma")
        text(d, bx + 18, by, region + ": ", f(10, True))
        rw = d.textlength(region + ": ", font=f(10, True))
        text(d, bx + 18 + rw, by, s, f(10))
        text(d, bx + 268, by + 1, src, f(8), fill=(120, 116, 104), anchor="ra")

    # ---- bottom: date check + how sure + footer ----
    d.rectangle([12, 964, 640, 1010], fill=(255, 250, 235), outline=RED, width=1)
    text(d, 20, 967, "DATE CHECK — LEFT OUT ON PURPOSE", f(9, True), fill=RED)
    text(d, 20, 978,
         "Fri 20 Nov: Poland missiles · Denmark expels attaché · ICJ Myanmar ruling · UK–EU deal",
         f(9))
    text(d, 20, 988,
         "Wall Street sell-off · Akvan landfall · Kyiv bridges barrage · GTA VI record · Trump–Xi–Putin summit.",
         f(9))
    text(d, 20, 998,
         "Not yet: COP31 final vote · Las Vegas GP race · Alcaraz–Zverev final · India declare at 720-9.",
         f(9))
    d.rectangle([648, 964, 1012, 1010], fill=(255, 250, 235), outline=INK, width=1)
    text(d, 656, 967, "HOW SURE", f(9, True))
    text(d, 656, 978, "● CONFIRMED — 2+ major outlets", f(9))
    text(d, 656, 988, "● OFFICIAL — on the record", f(9))
    text(d, 656, 998, "● REPORTED — one major outlet", f(9))
    text(d, 512, 1013,
         "Every story here happened or was first reported on Saturday 21 November 2026 (UTC). Maps, charts and text drawn in code.",
         f(9), fill=(120, 116, 104), anchor="ma")
    return img


if __name__ == "__main__":
    im = build_v13()
    im.save("entry_v13.png")
    print("saved entry_v13.png", im.size)
