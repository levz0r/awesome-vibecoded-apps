"""Fail if entries in any README section are not in case-insensitive alphabetical order."""

import re
import sys

ENTRY = re.compile(r"^- \[([^\]]+)\]\(")

path = sys.argv[1] if len(sys.argv) > 1 else "README.md"
section, entries, errors = None, [], []


def check(section, entries):
    for (prev, _), (name, line) in zip(entries, entries[1:]):
        if name.lower() < prev.lower():
            errors.append(f"{path}:{line}: '{name}' should come before '{prev}' in section '{section}'")


with open(path, encoding="utf-8") as f:
    for number, text in enumerate(f, 1):
        if text.startswith("#"):
            check(section, entries)
            section, entries = text.strip("# \n"), []
        elif section != "Contents" and (match := ENTRY.match(text)):
            entries.append((match.group(1), number))
check(section, entries)

print("\n".join(errors) or "All sections are in alphabetical order.")
sys.exit(1 if errors else 0)
