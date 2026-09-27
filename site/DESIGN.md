---
name: vibecodedapps.dev
description: Every shipped vibe-coded app as one dense numbered line under a single ultramarine band.
colors:
  band-ultramarine: "#3a33d6"
  band-ink: "#ffffff"
  band-lilac: "#d9d7ff"
  warm-grey-ground: "#f3f2ee"
  near-black-ink: "#1b1b19"
  meta-grey: "#62625b"
  visited-grey: "#66665f"
  hairline: "#dcdad3"
  live-green: "#2c7a4b"
  failing-rust: "#b0391f"
  select-lilac: "#d8d6ff"
  night-ground: "#141416"
  night-ink: "#e9e8e3"
  night-meta: "#a2a29a"
  night-visited: "#8c8c85"
  night-hairline: "#2c2c30"
  night-glyph: "#a19dff"
  night-live: "#6cc995"
  night-failing: "#ff8a6b"
typography:
  headline:
    fontFamily: "Verdana, Geneva, \"DejaVu Sans\", sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1.5
  title:
    fontFamily: "Verdana, Geneva, \"DejaVu Sans\", sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1.5
  body:
    fontFamily: "Verdana, Geneva, \"DejaVu Sans\", sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Verdana, Geneva, \"DejaVu Sans\", sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\""
rounded:
  none: "0px"
  focus: "2px"
spacing:
  gutter: "16px"
  gutter-narrow: "12px"
  band-y: "8px"
  row-top: "7px"
  row-bottom: "6px"
  column-gap: "10px"
  lede-after: "14px"
  heading-before: "22px"
components:
  band:
    backgroundColor: "{colors.band-ultramarine}"
    textColor: "{colors.band-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "8px 16px"
  band-link:
    textColor: "{colors.band-lilac}"
    typography: "{typography.body}"
  band-link-current:
    textColor: "{colors.band-ink}"
    typography: "{typography.body}"
  band-submit:
    textColor: "{colors.band-ink}"
    typography: "{typography.title}"
  entry-row:
    backgroundColor: "{colors.warm-grey-ground}"
    textColor: "{colors.near-black-ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "7px 0 6px"
  entry-row-target:
    backgroundColor: "{colors.select-lilac}"
  entry-title:
    textColor: "{colors.near-black-ink}"
    typography: "{typography.title}"
  entry-meta:
    textColor: "{colors.meta-grey}"
    typography: "{typography.label}"
  status-failing:
    textColor: "{colors.failing-rust}"
    typography: "{typography.label}"
---

# Design System: vibecodedapps.dev

## Overview

**Creative North Star: "The Show List"**

The site reads like a developer's morning front page: a single ultramarine band across the top, then a numbered column of one-line entries on warm grey paper, each separated by a hairline. Every shipped app gets exactly the same weight: name, domain, one sentence, and a meta line with its category and a drawn live tick. Rank is position in the list, never size, colour, or a card.

Density is the aesthetic. There is one text size (15px Verdana-lineage sans at 1.5 leading) for everything from the page heading to the footer; hierarchy comes from bold, from the meta grey, and from order. The only colour with volume is the band. Everything below it is ink, grey, hairlines, and a tiny 5x5 mirrored pixel glyph per app, derived from its name, so rows stay recognizable without screenshots.

The build explicitly refuses the dark AI-directory card grid: no cards, no thumbnails, no gradients, no shadows, no rounded tiles, no hero.

**Key Characteristics:**
- One committed ultramarine band; flat, full strength, full width.
- One type size across the whole page; weight and grey carry hierarchy.
- Numbered hairline-ruled rows; the list starts above the fold.
- A 5x5 mirrored name-derived glyph per row, in the band colour.
- Drawn SVG status marks (tick for live, open ring for failing), never emoji.
- Light and dark schemes from the same tokens; the band does not change.

## Colors

One saturated voice (ultramarine) on a warm, low-chroma neutral ground; all other colour is either status or text grey.

### Primary
- **Band Ultramarine** (`band-ultramarine`): the nav band background in both schemes, the pixel glyph fill in light mode, the favicon, `theme-color`, and the focus ring in light mode. In dark mode `select` also uses it as the `:target` row highlight.

### Neutral
- **Warm Grey Ground** (`warm-grey-ground`): page background, light mode. Also the scrollbar track.
- **Near-Black Ink** (`near-black-ink`): all primary text, app names, footer links.
- **Meta Grey** (`meta-grey`): row numbers, domains, the lede, meta lines, footer prose.
- **Hairline** (`hairline`): the 1px rules above the list and under every row; scrollbar thumb.
- **Band Ink** (`band-ink`) and **Band Lilac** (`band-lilac`): text inside the band. Lilac is the resting link colour; white is hover, current page, the home name, and submit.
- **Select Lilac** (`select-lilac`): `::selection` and the `:target` row highlight in light mode.
- **Night set** (`night-*`): the dark-scheme replacements for ground, ink, meta, visited, hairline, glyph, live and failing. The band colour and band text are identical in both schemes.

### Status
- **Live Green** (`live-green` / `night-live`): stroke of the drawn tick only. The word "live" stays in meta grey.
- **Failing Rust** (`failing-rust` / `night-failing`): the ring and the "link failing, under review" label, used only when an open broken-links issue names the URL.

### Named Rules
**The One Band Rule.** Ultramarine appears at volume in exactly one place, the band. Below it, it only appears as the 15px glyph, a focus ring, or a selection. No ultramarine buttons, headings, or panels.

**The Status Is Earned Rule.** Green and rust are only ever driven by the weekly link check. They never decorate.

## Typography

**Body Font:** Verdana (with Geneva, "DejaVu Sans", sans-serif)

**Character:** A wide, screen-native humanist sans chosen for legibility at small size; it reads as a working list, not a brochure. No web fonts are loaded.

### Hierarchy
- **Headline** (700, 15px, 1.5): the page `h1` ("Real apps built with vibe coding"). Same size as body.
- **Title** (700, 15px, 1.5): the app name inside each row, the band home name, and submit.
- **Body** (400, 15px, 1.5): row descriptions, band links, footer. Row title line is capped at 110ch; footer paragraphs at 72ch.
- **Label** (400, 15px, 1.5, tabular numerals): row numbers, domains, meta lines, the lede, all in meta grey.

### Named Rules
**The One Size Rule.** Every piece of text is 15px. Hierarchy is bold, grey, and position. Never introduce a second size, including for headings or the footer.

**The Rank Is Position Rule.** A row's importance is its number. No entry gets a larger name, a badge, or a highlight.

## Layout

A single centred column, max 1120px, with a 16px side gutter; the band's inner row uses the same max width so band and list share left and right edges. The band is a wrapping flex row: home name, category links, then GitHub and submit pushed right with `margin-left: auto`.

Each entry is a three-column grid: a right-aligned number column (2.6em), a 15px glyph column, and the body, with a 10px column gap and 7px/6px vertical padding between hairlines. The body holds two lines: title line (name, domain in parens, description), then meta line (category link on the index, a mid-dot separator, status).

Vertical rhythm is tight and fixed: 22px above the heading, 2px under it, 14px under the lede, 18px above and 40px below the footer.

At 560px and below: the number column narrows to 2em and the gap to 8px; the band padding drops to 6px 12px, and the band reorders so the home name and GitHub/submit share the first line and category links wrap underneath. Nothing else changes; there is no hamburger and no hidden navigation.

## Elevation & Depth

Completely flat. There are no shadows, no layered surfaces, and no transparency. Separation comes from 1px hairline rules and from the band's solid colour. The only state that changes a surface is `:target`, which fills a row with the select colour.

### Named Rules
**The Hairline Rule.** Rows are separated by a single 1px rule in the hairline colour, never by gaps, cards, or shadows.

## Shapes

Square everything. No component has a radius; the only curve is the 2px radius on the focus outline. The recurring geometry is the 5x5 pixel glyph: a horizontally mirrored grid of 1-unit squares derived from a SHA-1 of the app name, rendered with `shape-rendering: crispEdges` at 15px in rows and 13px in the band (32px as the favicon). The two status marks are the only drawn strokes: a round-capped tick and an open ring, both 12px.

## Components

### Navigation (the band)
Flat ultramarine, full width, wrapping. Links are lilac with no underline at rest; hover and the current page go white and underlined (1px, 0.2em offset). The home link is bold white with its glyph. GitHub sits at rest colour; **submit** is always bold, white, and underlined so makers find it without it becoming a button. Focus outline switches to white inside the band.

### Entry row (signature component)
Number, glyph, then a two-line body between hairlines. The app name is a bold link with no underline at rest (underline on hover), followed by the domain in meta grey parens and the one-sentence description in normal weight. Visited names dim to `visited-grey` (5.2:1 on the ground). The meta line carries the category link (underlined, meta grey, ink on hover) on the index only, a mid-dot separator, and the status: a green drawn tick with "live", or a rust ring with "link failing, under review". Rows are anchor-addressable by slugged name; the targeted row fills with select colour.

### Lede
One line in meta grey under the heading carrying the count and the date of the last link check (a `<time>` element), falling back to "every week" when the date is unknown.

### Footer
Meta-grey prose at the same size, max 72ch, with ink-coloured links: the README intro, the maintainer disclosure footnote, and a closing submit/star line.

### Skip link
Off-screen at rest, drops to 8px from the top on focus, ground-coloured background.

## Do's and Don'ts

### Do:
- **Do** keep every piece of text at 15px Verdana-lineage sans, 1.5 leading.
- **Do** separate rows with a single 1px hairline and keep row padding at 7px top, 6px bottom.
- **Do** give every entry a number, a 5x5 name-derived glyph, name, domain, description, and a status mark.
- **Do** keep ultramarine confined to the band, the glyphs, focus, and selection.
- **Do** draw status marks as inline SVG strokes and drive them only from the link check.
- **Do** keep submit bold, white, and underlined in the band's right edge.
- **Do** swap to the night set under `prefers-color-scheme: dark` while keeping the band identical.

### Don't:
- **Don't** introduce cards, thumbnails, tiles, or a grid of boxes; the list is one column of lines.
- **Don't** add a second type size, a display face, or web fonts.
- **Don't** add shadows, gradients, rounded corners, or translucent layers.
- **Don't** rank entries by size, colour, or badges; position is the only rank.
- **Don't** use emoji or icon-font glyphs for status or navigation.
- **Don't** turn submit into a filled button or add a second accent colour.
