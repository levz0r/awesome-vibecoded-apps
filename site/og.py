"""Render the 1200x630 social preview images for vibecodedapps.dev.

Usage: python3 site/og.py [--out _site]

Needs Pillow and a Verdana-lineage font (DejaVu Sans on Linux, Verdana on macOS).
Card text comes from build.og_cards(), so images always match the pages that use them.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from build import ROOT, glyph_cells, og_cards, parse_readme

W, H = 1200, 630
MARGIN = 64
GROUND, INK, META, BAND, RULE, WHITE = "#f3f2ee", "#1b1b19", "#62625b", "#3a33d6", "#dcdad3", "#ffffff"

FONTS = {
    "regular": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/System/Library/Fonts/Supplemental/Verdana.ttf"],
    "bold": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"],
}


def font(weight, size):
    for path in FONTS[weight]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    raise SystemExit(f"No {weight} font found; install fonts-dejavu-core. Tried: {FONTS[weight]}")


def draw_glyph(draw, name, x, y, cell, fill):
    for gx, gy in glyph_cells(name):
        draw.rectangle([x + gx * cell, y + gy * cell, x + (gx + 1) * cell - 1, y + (gy + 1) * cell - 1], fill=fill)


def wrap(draw, text, face, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=face) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def fit(draw, text, face, width):
    """Trim text with an ellipsis until it fits the width."""
    if draw.textlength(text, font=face) <= width:
        return text
    while text and draw.textlength(text + "…", font=face) > width:
        text = text[:-1]
    return text.rstrip() + "…"


def render(card):
    img = Image.new("RGB", (W, H), GROUND)
    draw = ImageDraw.Draw(img)

    # Band: the site's one committed colour, with the site glyph and name.
    draw.rectangle([0, 0, W, 112], fill=BAND)
    draw_glyph(draw, "vibecodedapps.dev", MARGIN, 36, 8, WHITE)
    draw.text((MARGIN + 60, 56), "vibecodedapps.dev", font=font("bold", 38), fill=WHITE, anchor="lm")

    # Heading: largest size that fits in two lines.
    for size in (72, 66, 60, 54):
        face = font("bold", size)
        lines = wrap(draw, card["heading"], face, W - 2 * MARGIN)
        if len(lines) <= 2:
            break
    if len(lines) == 2:
        # Balance the break so the second line isn't a lone word.
        words = card["heading"].split()
        splits = [(" ".join(words[:i]), " ".join(words[i:])) for i in range(1, len(words))]
        lines = list(min(splits, key=lambda pair: max(draw.textlength(t, font=face) for t in pair)))
    y = 168
    for line in lines:
        draw.text((MARGIN, y), line, font=face, fill=INK)
        y += int(size * 1.22)
    draw.text((MARGIN, y + 14), card["subline"], font=font("regular", 32), fill=META)

    # Sample apps: two columns of glyph + name under a hairline, like the list itself.
    top = 452
    draw.rectangle([MARGIN, top, W - MARGIN, top + 1], fill=RULE)
    name_face, col_w = font("bold", 30), (W - 2 * MARGIN) // 2
    for i, name in enumerate(card["apps"]):
        x = MARGIN + (i % 2) * col_w
        row_y = top + 34 + (i // 2) * 64
        draw_glyph(draw, name, x, row_y, 6, BAND)
        draw.text((x + 48, row_y + 15), fit(draw, name, name_face, col_w - 72), font=name_face, fill=INK, anchor="lm")
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(parser.parse_args().out) / "og"
    out.mkdir(parents=True, exist_ok=True)
    _, _, entries = parse_readme((ROOT / "README.md").read_text(encoding="utf-8"))
    cards = og_cards(entries)
    for card in cards:
        render(card).save(out / f"{card['stem']}.png", optimize=True)
    print(f"Rendered {len(cards)} preview images -> {out}")


if __name__ == "__main__":
    main()
