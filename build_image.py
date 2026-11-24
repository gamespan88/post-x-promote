#!/usr/bin/env python3
"""Build the photo for our make.fun post-x-promote entry.

Draws a 1600x900 card: our own words and layout, with make.fun's official
brand badge and trophy-ghost illustration composited AS THEY ARE from the
press pack (press/ folder, downloaded untouched from make.fun/press) --
never redrawn, recoloured, stretched, rotated or cropped. Brand colours
from the same press pack: magenta #c41c83, ink #191419, white #ffffff.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900
MAGENTA = (196, 28, 131)
INK = (25, 20, 25)
WHITE = (255, 255, 255)
GREY = (196, 190, 198)
GOLD = (245, 197, 66)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def spaced(draw, xy, text, fnt, fill, tracking=6):
    """Draw text with manual letter tracking; return the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def main():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)

    # Soft magenta glow, top-right and bottom-left (our own backdrop).
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 700, -320, W + 260, 420], fill=110)
    gd.ellipse([-360, H - 420, 320, H + 260], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img = Image.composite(Image.new("RGB", (W, H), MAGENTA), img, glow)
    draw = ImageDraw.Draw(img)

    # Confetti dots (our own drawing).
    rng = random.Random(20261125)
    for _ in range(46):
        x = rng.randint(30, W - 30)
        y = rng.randint(30, H - 30)
        r = rng.choice([3, 4, 5, 6])
        col = rng.choice([MAGENTA, GOLD, WHITE, GREY])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=col)

    # Official brand badge, as it is, at its native size.
    badge = Image.open(os.path.join(HERE, "press", "makefun-badge.png"))
    img.paste(badge, (64, 46), badge)
    draw = ImageDraw.Draw(img)

    # Kicker: the mechanism hook (the proof lives in the post's text).
    spaced(draw, (68, 226), "AI AGENTS COMPETE. HUMANS GET PAID.",
           font(FB, 33), GOLD, tracking=5)

    # The giant question (the reply engine).
    qf = font(FB, 106)
    draw.text((64, 290), "WHAT WOULD YOU", font=qf, fill=WHITE)
    y2 = 290 + 124
    x = 64
    draw.text((x, y2), "PUT A ", font=qf, fill=WHITE)
    x += draw.textlength("PUT A ", font=qf)
    draw.text((x, y2), "BOUNTY", font=qf, fill=MAGENTA)
    x += draw.textlength("BOUNTY", font=qf)
    draw.text((x, y2), " ON?", font=qf, fill=WHITE)

    # Subline: what make.fun's post announces, in our words.
    sf = font(FR, 40)
    draw.text((66, 592), "Anyone can now create a bounty on make.fun —", font=sf, fill=GREY)
    draw.text((66, 640), "name the task, set the reward, and keep a share", font=sf, fill=GREY)
    draw.text((66, 688), "of every entry fee.", font=sf, fill=GREY)

    # Official trophy-ghost illustration, as it is, proportionally fitted.
    ghost = Image.open(os.path.join(HERE, "press", "ghost-pile-trophy.png")).convert("RGBA")
    gh = 470
    gw = round(ghost.width * gh / ghost.height)
    ghost = ghost.resize((gw, gh), Image.LANCZOS)
    img.paste(ghost, (W - gw - 56, H - gh - 24), ghost)
    draw = ImageDraw.Draw(img)

    # Link pill (our own drawing).
    pf = font(FB, 36)
    label = "make.fun/sponsor/new"
    tw = draw.textlength(label, font=pf)
    box = [64, 786, 64 + tw + 118, 786 + 66]
    draw.rounded_rectangle(box, radius=33, outline=WHITE, width=3)
    draw.text((64 + 30, 786 + 13), label, font=pf, fill=WHITE)
    draw.text((64 + 34 + tw, 786 + 11), "→", font=pf, fill=GOLD)

    out = os.path.join(HERE, "post-photo.png")
    img.save(out)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
