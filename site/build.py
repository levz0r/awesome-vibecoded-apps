"""Build vibecodedapps.dev from README.md.

Usage: python3 site/build.py [--out _site]

Standard library only. When GITHUB_TOKEN and GITHUB_REPOSITORY are set (in
GitHub Actions), it also reads the date of the last link check on main and any
open `broken-links` issue, so rows whose link is failing are marked honestly.
"""

import argparse
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import urllib.request
from pathlib import Path

SITE = "https://vibecodedapps.dev"
REPO = "levz0r/awesome-vibecoded-apps"
REPO_URL = f"https://github.com/{REPO}"
SUBMIT_URL = f"{REPO_URL}/blob/main/CONTRIBUTING.md"
ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

ENTRY = re.compile(r"^- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<desc>.+)$")
SKIP_SECTIONS = {"Contents", "Footnotes", "Contributing"}
SAFE_URL = re.compile(r"^https?://[^\s\"'<>`]+$")

# Category pages, in nav order. `plural` reads naturally after "Vibe-coded".
CATEGORIES = {
    "Web Apps": ("web-apps", "web apps", "web apps"),
    "Games": ("games", "games", "games"),
    "iOS": ("ios", "iOS", "iOS apps"),
    "Android": ("android", "Android", "Android apps"),
    "macOS": ("macos", "macOS", "macOS apps"),
    "Windows": ("windows", "Windows", "Windows apps"),
    "Linux": ("linux", "Linux", "Linux apps"),
    "Cross-Platform": ("cross-platform", "cross-platform", "cross-platform apps"),
    "CLI Tools": ("cli-tools", "CLI tools", "CLI tools"),
    "Browser Extensions": ("browser-extensions", "extensions", "browser extensions"),
}


def parse_readme(text):
    """Return (intro paragraphs, footnote, [entry dicts]) from the README."""
    entries, intro, footnote = [], [], ""
    section = None
    for line in text.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if line.startswith("# "):
                section = "__title__"
            elif line.startswith("## ") and heading == "Apps":
                section = None  # platform subsections follow
            else:
                section = heading
            continue
        if section == "__title__":
            if line.startswith("> "):
                intro.append(line[2:].strip())
            elif line.strip():
                intro.append(line.strip())
        elif section == "Footnotes" and line.strip():
            footnote = line.strip()
        elif section and section not in SKIP_SECTIONS and line.startswith("- ["):
            if not (m := ENTRY.match(line)):
                raise SystemExit(f"Can't parse README entry: {line!r}")
            if section not in CATEGORIES:
                raise SystemExit(f"README section '{section}' has no page mapping in site/build.py")
            if not SAFE_URL.match(m["url"]):
                raise SystemExit(f"README entry '{m['name']}' has a non-http(s) link: {m['url']!r}")
            entries.append({**m.groupdict(), "category": section})
    return intro, footnote, entries


def github_json(path):
    token, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        return None
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except OSError as err:
        print(f"warning: GitHub API {path}: {err}")
        return None


def link_status():
    """Return (date of last link check on main or None, set of failing URLs)."""
    runs = github_json("actions/workflows/links.yml/runs?branch=main&status=success&per_page=1")
    checked = None
    if runs and runs.get("workflow_runs"):
        checked = datetime.date.fromisoformat(runs["workflow_runs"][0]["updated_at"][:10])
    failing = set()
    for issue in github_json("issues?labels=broken-links&state=open") or []:
        failing |= {u.rstrip("/") for u in re.findall(r"<(https?://[^>]+)>", issue.get("body") or "")}
    return checked, failing


def glyph(name, size=15):
    """A 5x5 mirrored mark derived from the name, so rows stay recognizable without screenshots."""
    bits = int(hashlib.sha1(name.lower().encode()).hexdigest(), 16)
    cells = []
    for row in range(5):
        for col in range(3):
            if bits >> (row * 3 + col) & 1:
                for x in {col, 4 - col}:
                    cells.append(f'<rect x="{x}" y="{row}" width="1" height="1"/>')
    if not cells:
        cells.append('<rect x="2" y="2" width="1" height="1"/>')
    return (f'<svg class="glyph" viewBox="0 0 5 5" width="{size}" height="{size}" '
            f'aria-hidden="true" shape-rendering="crispEdges">{"".join(cells)}</svg>')


LIVE_MARK = ('<svg class="mark" viewBox="0 0 12 12" width="12" height="12" aria-hidden="true">'
             '<path d="M2 6.5 4.8 9.2 10 3"/></svg>')
FAILING_MARK = ('<svg class="mark mark--failing" viewBox="0 0 12 12" width="12" height="12" aria-hidden="true">'
                '<circle cx="6" cy="6" r="4"/></svg>')


def domain(url):
    host = re.sub(r"^https?://(www\.)?", "", url).rstrip("/")
    parts = host.split("/")
    # For code hosts and stores, the owner is the useful part.
    if parts[0] in {"github.com", "gitlab.com"} and len(parts) > 1:
        return f"{parts[0]}/{parts[1]}"
    return parts[0]


def e(text):
    return html.escape(text, quote=True)


def inline_md(text):
    """Render [text](url) links from the README prose; only http(s) and relative links become anchors."""
    out, last = [], 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", text):
        out.append(e(text[last:m.start()]))
        label, url = m.groups()
        if SAFE_URL.match(url) or re.match(r"^[A-Za-z0-9_./#-]+$", url) and not url.startswith("//"):
            out.append(f'<a href="{e(url)}">{e(label)}</a>')
        else:
            out.append(e(label))
        last = m.end()
    out.append(e(text[last:]))
    return "".join(out)


def json_ld(data):
    """JSON for a <script> block: escape characters that could close the tag or start markup."""
    return (json.dumps(data, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def row(n, entry, failing, show_category):
    slug, _, plural = CATEGORIES[entry["category"]]
    is_failing = entry["url"].rstrip("/") in failing
    status = (f'<span class="status status--failing">{FAILING_MARK}link failing, under review</span>'
              if is_failing else f'<span class="status">{LIVE_MARK}live</span>')
    meta = [status]
    if show_category:
        meta.insert(0, f'<a href="/{slug}/">{e(plural)}</a>')
    return f"""
      <li class="entry" id="{e(re.sub(r'[^a-z0-9]+', '-', entry['name'].lower()).strip('-'))}">
        <span class="n">{n}.</span>
        {glyph(entry["name"])}
        <div class="body">
          <p class="title"><a href="{e(entry["url"])}" rel="noopener">{e(entry["name"])}</a> <span class="domain">({e(domain(entry["url"]))})</span> <span class="desc">{e(entry["desc"])}</span></p>
          <p class="meta">{' <span class="sep" aria-hidden="true">·</span> '.join(meta)}</p>
        </div>
      </li>"""


def page(*, path, title, description, heading, lede, entries, failing, current, show_category, extra_ld=None):
    canonical = f"{SITE}{path}"
    nav = "\n".join(
        f'<a href="/{slug}/"{" aria-current=\"page\"" if slug == current else ""}>{short}</a>'
        for slug, short, _ in CATEGORIES.values()
    )
    items = "".join(row(i, entry, failing, show_category) for i, entry in enumerate(entries, 1))
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": canonical,
        "isPartOf": {"@type": "WebSite", "name": "vibecodedapps.dev", "url": SITE + "/"},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": len(entries),
            "itemListElement": [
                {"@type": "ListItem", "position": i, "name": x["name"], "url": x["url"], "description": x["desc"]}
                for i, x in enumerate(entries, 1)
            ],
        },
    }
    if extra_ld:
        ld.update(extra_ld)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="vibecodedapps.dev">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#3a33d6">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">{json_ld(ld)}</script>
</head>
<body>
<!--
THESIS: Every shipped vibe-coded app is one dense numbered line, read the way developers read the front page each morning; refuses the dark AI-directory card grid.
OWN-WORLD: Warm grey ground, near-black ink, one fully committed ultramarine nav band, one small Verdana-lineage text size, hairline rules, a 5x5 glyph per app, drawn live ticks.
STORY: The visitor sees real shipped apps immediately, trusts they are live (checked weekly), opens a few, and makers find Submit in the band.
FIRST VIEWPORT: Ultramarine band (site name left, category links, submit right); one-line lede with count and last check date; numbered rows begin above the fold.
FORM: The Show List, grounded candidate 5 of 7, seed key 925c97e8.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, and DESIGN.md
-->
<a class="skip" href="#list">Skip to the list</a>
<header class="band">
  <nav class="band__inner" aria-label="Categories">
    <a class="home" href="/"{' aria-current="page"' if current == "" else ""}>{glyph("vibecodedapps.dev", 13)}vibecodedapps.dev</a>
    <span class="cats">{nav}</span>
    <span class="actions"><a href="{REPO_URL}">GitHub</a> <a class="submit" href="{SUBMIT_URL}">submit</a></span>
  </nav>
</header>
<main class="sheet">
  <h1>{e(heading)}</h1>
  <p class="lede">{lede}</p>
  <ol class="list" id="list">{items}
  </ol>
</main>
<footer class="sheet foot">
  {FOOTER}
</footer>
</body>
</html>
"""


FOOTER = ""  # filled in main() from the README


def main():
    global FOOTER
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(ROOT / "_site"))
    out = Path(parser.parse_args().out)

    intro, footnote, entries = parse_readme((ROOT / "README.md").read_text(encoding="utf-8"))
    checked, failing = link_status()
    live = sum(1 for x in entries if x["url"].rstrip("/") not in failing)
    when = f'{checked:%b} {checked.day}, {checked.year}' if checked else None
    check_note = (f'<time datetime="{checked.isoformat()}">{when}</time>' if checked else "every week")

    FOOTER = f"""<p>{inline_md(intro[1] if len(intro) > 1 else intro[0])}</p>
  <p>{inline_md(footnote)}</p>
  <p>This site is generated from the <a href="{REPO_URL}">Awesome Vibecoded Apps</a> list on GitHub. Every link is checked automatically each week. Built something with AI? <a href="{SUBMIT_URL}">Submit it</a>, or <a href="{REPO_URL}">star the list</a>.</p>"""

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    everything = sorted(entries, key=lambda x: x["name"].lower())
    pages = [("/", 1.0)]
    (out / "index.html").write_text(page(
        path="/",
        title=f"Vibe-coded apps: {len(entries)} real examples built with AI",
        description=(f"{len(entries)} real, live apps, games and tools built with vibe coding "
                     "(Claude Code, Cursor, Lovable and more), from the Awesome Vibecoded Apps list. Links checked weekly."),
        heading="Real apps built with vibe coding",
        lede=(f"{len(entries)} apps built by describing them to an AI. "
              f"{f'All {live}' if live == len(entries) else f'{live} of {len(entries)}'} live at the last check ({check_note})."),
        entries=everything, failing=failing, current="", show_category=True,
    ), encoding="utf-8")

    for category, (slug, _, plural) in CATEGORIES.items():
        members = [x for x in entries if x["category"] == category]
        if not members:
            continue
        n = len(members)
        noun = plural if n != 1 else plural[:-1] if plural.endswith("s") else plural
        (out / slug).mkdir()
        (out / slug / "index.html").write_text(page(
            path=f"/{slug}/",
            title=f"Vibe-coded {plural}: {n} real example{'s' if n != 1 else ''}",
            description=(f"{n} {noun} built with vibe coding, each one live and checked weekly. "
                         f"From the Awesome Vibecoded Apps list: {', '.join(x['name'] for x in members[:4])}"
                         f"{' and more' if n > 4 else ''}."),
            heading=f"Vibe-coded {plural}",
            lede=f"{n} {noun} built with AI. Links checked {check_note}.",
            entries=members, failing=failing, current=slug, show_category=False,
        ), encoding="utf-8")
        pages.append((f"/{slug}/", 0.8))

    (out / "404.html").write_text(page(
        path="/404.html", title="Not found | vibecodedapps.dev", description="This page does not exist.",
        heading="That page doesn't exist", lede='It may have been removed with a dead entry. <a href="/">See every app</a>.',
        entries=[], failing=failing, current=None, show_category=True,
    ).replace('<link rel="canonical" href="https://vibecodedapps.dev/404.html">', '<meta name="robots" content="noindex">'),
        encoding="utf-8")

    today = datetime.date.today().isoformat()
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>" for p, pr in pages)
    (out / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (out / "CNAME").write_text("vibecodedapps.dev\n")
    (out / ".nojekyll").write_text("")
    for asset in ("style.css", "og.png"):
        shutil.copy(HERE / asset, out / asset)
    (out / "favicon.svg").write_text(
        glyph("vibecodedapps.dev", 32).replace('class="glyph"', 'xmlns="http://www.w3.org/2000/svg" fill="#3a33d6"'))

    print(f"Built {len(pages)} pages, {len(entries)} entries, {len(failing)} failing links, last check {checked} -> {out}")


if __name__ == "__main__":
    main()
