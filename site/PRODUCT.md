# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Plain Python + static HTML/CSS (user's choice). A dependency-free Python script turns `README.md` into the site in GitHub Actions and deploys it to GitHub Pages at `vibecodedapps.dev` (registered at Cloudflare, DNS on Cloudflare). No framework, no Node build step.

## Users

- **Primary: browsers.** People looking for real examples of apps built with vibe coding: curious developers, founders sizing up what AI-built software can do, writers and journalists collecting examples. They usually arrive from a search engine or an AI assistant (Google, Reddit, ChatGPT, Perplexity are today's top referrers to the repo) with a question like "what has anyone actually shipped with vibe coding?".
- **Secondary: makers.** People who built something with AI and want it listed. They need a clear, low-friction path to submit (a GitHub PR per `CONTRIBUTING.md`).

## Product Purpose

A browsable, search-friendly companion to the Awesome Vibecoded Apps list on GitHub (`levz0r/awesome-vibecoded-apps`). It answers "show me real things people built with vibe coding" and sends visitors to each app and back to the repo to star or contribute. Success: the site ranks for generic "vibe coded apps / vibe coding examples" searches the README alone can't win, and grows stars and submissions.

## Positioning

A curated, maintained list of shipped vibe-coded software, not a list of AI coding tools or tutorials. Every link is checked automatically each week and dead entries are removed; entries are in alphabetical order within categories; inclusion follows `CONTRIBUTING.md`.

## Operating Context

- Content source of truth is `README.md`; the site is regenerated on every push to `main`. Contributors never edit the site.
- Categories today: Apps (macOS, iOS, Android, Windows, Linux, Cross-Platform), Web Apps, CLI Tools, Games, Browser Extensions. About 49 entries, each a name, a URL and a one-sentence description.
- CI already runs awesome-lint, an alphabetical-order check, and a weekly lychee link check.

## Capabilities and Constraints

- One page per category plus an index; each page has its own title, description, canonical URL, sitemap entry and structured data.
- Entries have no images, tool labels, dates or metrics yet. AI-tool labels ("Built with Claude Code") are planned separately, later, and would add `/built-with/` pages.
- Undecided: whether to show entry thumbnails or screenshots later.

## Evidence on Hand

- Real entries and descriptions in `README.md`. Some well-known entries: Bitchat (Jack Dorsey), MenuGen (Andrej Karpathy), Fly (pieter levels).
- Repo stats (40 stars, 10 forks) exist but are small; do not present them as proof of scale.
- No testimonials, press, user counts or rankings exist. Do not invent any.
- Some entries are by the list maintainer; the README footnote discloses this and the site must keep that disclosure.

## Product Principles

1. The README is the only source; the site never drifts from it.
2. Every entry is real and live; say so because it's verified weekly, not as marketing.
3. Get visitors to the apps fast; the list is the product, not the chrome around it.
4. Make submitting obvious for makers without crowding browsers.
5. Search and AI-assistant discoverability is a first-class requirement: semantic HTML, fast static pages, no client-side rendering of content.

## Accessibility & Inclusion

WCAG 2.2 AA: semantic landmarks, visible focus, sufficient contrast in light and dark, content readable without JavaScript.
