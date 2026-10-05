"""Check entries added by a pull request against the inclusion criteria in CONTRIBUTING.md.

Usage: python3 check-entries.py <base-ref>     (compares README.md against <base-ref>)
       python3 check-entries.py --line '- [Name](url) - Description.'

Each new entry gets one result per checkable criterion: PASS, FAIL, or REVIEW (needs a
human, e.g. shared hosting where the domain age says nothing). Exits 1 if anything FAILs.
The PR description (env PR_BODY) is scanned for links to a public AI statement.

Standard library only. Fetched pages and the PR body are untrusted data: they are only
searched for keywords and never executed or followed beyond one redirect chain.
"""

import datetime
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

ENTRY = re.compile(r"^\+?- \[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<desc>.+)$")
MIN_AGE_DAYS = 30
UA = "Mozilla/5.0 (compatible; awesome-vibecoded-apps-checker/1.0; +https://vibecodedapps.dev)"
TOKEN = os.environ.get("GITHUB_TOKEN")

# Hosts where the registrable domain belongs to the platform, so its age says nothing.
SHARED_HOSTS = (
    "github.io", "netlify.app", "vercel.app", "pages.dev", "workers.dev", "lovable.app",
    "replit.app", "repl.co", "bolt.new", "web.app", "firebaseapp.com", "herokuapp.com",
    "onrender.com", "fly.dev", "glitch.me", "surge.sh", "itch.io", "streamlit.app",
)
STORES = ("apps.apple.com", "play.google.com", "chromewebstore.google.com",
          "addons.mozilla.org", "apps.microsoft.com", "microsoftedge.microsoft.com")

# A tool name only counts inside a statement about how something was built ("built with
# Claude Code", "made using Cursor"); bare mentions are often menus or filter lists.
# Generic phrases ("vibe coded") are weaker still: a site can be *about* vibe coding.
_TOOL = (r"(?:claude(?: code)?|cursor|github copilot|copilot|chatgpt|gpt-?[0-9o]|openai codex|codex|"
         r"gemini(?: cli)?|(?:google )?antigravity|lovable|bolt(?:\.new)?|replit(?: agent)?|v0|windsurf|"
         r"cline|aider|devin|kiro|zed|ai)")
AI_TOOLS = re.compile(
    r"\b(?:built|made|created|coded|developed|written|generated|prototyped|vibe[- ]?coded|shipped)"
    r"\b[^.\n]{0,30}?\b(?:with|using|by|in|via)\b[^.\n]{0,25}?\b(" + _TOOL + r")\b",
    re.IGNORECASE,
)
AI_GENERIC = re.compile(
    r"\b(vibe[- ]?coded|ai[- ]generated|ai[- ]assisted|ai[- ]built)\b",
    re.IGNORECASE,
)


def fetch(url, accept="text/html,*/*", limit=2_000_000, auth=False):
    headers = {"User-Agent": UA, "Accept": accept}
    if auth and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read(limit).decode("utf-8", errors="replace")


def fetch_json(url, auth=False):
    return json.loads(fetch(url, accept="application/json, application/rdap+json", auth=auth))


def text_of(html):
    html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


# --- domain age -----------------------------------------------------------------

_rdap_bootstrap = None


def rdap_server(tld):
    global _rdap_bootstrap
    if _rdap_bootstrap is None:
        _rdap_bootstrap = fetch_json("https://data.iana.org/rdap/dns.json")["services"]
    for tlds, urls in _rdap_bootstrap:
        if tld in tlds:
            return urls[0].rstrip("/") + "/"
    return None


def registration_date(host):
    """Registration date of the registrable domain, trying example.com then example.co.uk."""
    labels = host.split(".")
    server = rdap_server(labels[-1])
    if not server:
        return None, f"no RDAP server for .{labels[-1]}"
    for n in (2, 3):
        if len(labels) < n:
            break
        domain = ".".join(labels[-n:])
        try:
            data = fetch_json(f"{server}domain/{domain}")
        except Exception:
            continue
        for event in data.get("events", []):
            if event.get("eventAction") == "registration":
                return datetime.date.fromisoformat(event["eventDate"][:10]), domain
    return None, "registration date not published"


def github_repo(url):
    m = re.match(r"https?://github\.com/([^/]+)/([^/#?]+)", url)
    return (m.group(1), m.group(2).removesuffix(".git")) if m else None


def check_age(url, host):
    today = datetime.date.today()
    repo = github_repo(url)
    if repo:
        try:
            created = datetime.date.fromisoformat(
                fetch_json(f"https://api.github.com/repos/{repo[0]}/{repo[1]}", auth=True)["created_at"][:10])
        except Exception as err:
            return "REVIEW", f"could not read the GitHub repo ({err})"
        age = (today - created).days
        return ("PASS" if age >= MIN_AGE_DAYS else "FAIL"), f"repo created {created} ({age} days ago)"
    if host.endswith(SHARED_HOSTS) or host in STORES or host.endswith(".github.io"):
        return "REVIEW", f"shared host ({host}): domain age says nothing about this app"
    try:
        registered, detail = registration_date(host)
    except Exception as err:
        return "REVIEW", f"RDAP lookup failed ({err})"
    if not registered:
        return "REVIEW", detail
    age = (today - registered).days
    if age >= MIN_AGE_DAYS:
        return "PASS", f"{detail} registered {registered} ({age} days ago)"
    eligible = registered + datetime.timedelta(days=MIN_AGE_DAYS)
    return "FAIL", f"{detail} registered {registered}, only {age} days ago; eligible from {eligible}"


# --- public AI statement --------------------------------------------------------

def check_ai_statement(url, pr_body):
    repo = github_repo(url)
    # For GitHub repos read the README through the API; the HTML page carries GitHub's own
    # navigation, which mentions Copilot on every repo.
    sources = [f"https://api.github.com/repos/{repo[0]}/{repo[1]}/readme"] if repo else [url]
    # Links in the PR description, which should point at the public statement (criterion 3).
    for link in re.findall(r"https?://[^\s)\]>\"']+", pr_body or "")[:10]:
        if link not in sources and "github.com/levz0r/awesome-vibecoded-apps" not in link:
            sources.append(link)
    generic = None
    for source in sources:
        try:
            if source.endswith("/readme"):
                raw = fetch(source, accept="application/vnd.github.raw", auth=True)
            else:
                page = fetch(source)
                # Sites state how they were made in the footer; on directory-style sites the
                # body is full of other projects' "built with ..." lines, so look there first.
                footer = " ".join(text_of(f) for f in re.findall(r"(?is)<footer\b.*?</footer>", page))
                if footer and (m := AI_TOOLS.search(footer)):
                    return "PASS", f'"{m.group(0).strip()}" in the footer of {source}'
                raw = text_of(page)
        except Exception:
            continue
        if m := AI_TOOLS.search(raw):
            return "PASS", f'"{m.group(0).strip()}" at {source}'
        if not generic and (m := AI_GENERIC.search(raw)):
            generic = f'only the generic phrase "{m.group(0)}" at {source}; confirm it says the app was built with AI'
    if generic:
        return "REVIEW", generic
    return "REVIEW", ("no AI tool mentioned on the site, README, or linked pages "
                      "(a site rendered by JavaScript may hide it; check by hand)")


# --- used by others -------------------------------------------------------------

def check_users(url):
    repo = github_repo(url)
    if repo:
        try:
            data = fetch_json(f"https://api.github.com/repos/{repo[0]}/{repo[1]}", auth=True)
        except Exception as err:
            return "REVIEW", f"could not read the GitHub repo ({err})"
        stars, forks = data.get("stargazers_count", 0), data.get("forks_count", 0)
        if stars or forks:
            return "PASS", f"{stars} stars, {forks} forks"
        return "REVIEW", "no stars or forks yet; look for a launch post or other users"
    m = re.search(r"apps\.apple\.com/.*/id(\d+)", url)
    if m:
        try:
            result = fetch_json(f"https://itunes.apple.com/lookup?id={m.group(1)}")["results"]
        except Exception as err:
            return "REVIEW", f"App Store lookup failed ({err})"
        if not result:
            return "FAIL", "not found on the App Store"
        ratings = result[0].get("userRatingCount", 0)
        return ("PASS" if ratings else "REVIEW"), f"{ratings} App Store ratings"
    return "REVIEW", "check for ratings, a launch discussion, or other users"


# --- driver ---------------------------------------------------------------------

def added_entries(base):
    diff = subprocess.run(["git", "diff", "--unified=0", f"{base}...HEAD", "--", "README.md"],
                          capture_output=True, text=True, check=True).stdout
    return [m.groupdict() for line in diff.splitlines()
            if line.startswith("+- [") and (m := ENTRY.match(line))]


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--line":
        m = ENTRY.match(sys.argv[2])
        if not m:
            sys.exit(f"Not an entry line: {sys.argv[2]!r}")
        entries = [m.groupdict()]
    elif len(sys.argv) == 2:
        entries = added_entries(sys.argv[1])
    else:
        sys.exit(__doc__)
    if not entries:
        print("No new entries in this PR.")
        return

    pr_body = os.environ.get("PR_BODY", "")
    rows, failed = [], False
    for entry in entries:
        url = entry["url"]
        host = urllib.parse.urlparse(url).hostname or ""
        host = host.removeprefix("www.")
        checks = {
            "Live for 30+ days": check_age(url, host),
            "AI involvement stated publicly": check_ai_statement(url, pr_body),
            "Used by others": check_users(url),
        }
        for criterion, (status, detail) in checks.items():
            rows.append((entry["name"], criterion, status, detail))
            level = {"FAIL": "error", "REVIEW": "warning"}.get(status)
            if level:
                print(f"::{level} title={entry['name']}: {criterion}::{detail}")
            failed |= status == "FAIL"

    table = ["| Entry | Criterion | Result | Details |", "|---|---|---|---|"]
    icon = {"PASS": "✅ pass", "FAIL": "❌ fail", "REVIEW": "👀 review"}
    table += [f"| {n} | {c} | {icon[s]} | {d.replace('|', '/')} |" for n, c, s, d in rows]
    report = ("## Inclusion criteria check\n\n" + "\n".join(table) +
              "\n\n❌ blocks merging. 👀 needs a maintainer to check by hand. "
              "See [CONTRIBUTING.md](CONTRIBUTING.md#inclusion-criteria).\n")
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(report)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
