# Contribution Guidelines

Thank you for your interest in contributing to Awesome Vibecoded Apps!

## What Belongs Here

This list is for **apps and projects that were built using vibe coding** - AI-assisted development where you collaborated with tools like Claude, ChatGPT, Cursor, GitHub Copilot, or similar AI coding assistants.

### Inclusion Criteria

Every entry must meet **all** of these. Pull requests that don't are closed, and existing entries that stop meeting them are removed.

1. **Live for at least 30 days.** The project has been publicly available for at least 30 days when you submit (first public release, store listing, or first deploy).
2. **Works without special access.** The link loads and the main feature can be tried: no "coming soon" pages, waitlist-only access, or sign-up walls with nothing to try first. Paid apps are fine if the store listing or site shows what they do.
3. **AI involvement is stated publicly.** A README, blog post, video, launch post, or store description says the project was built with AI tools and names them. Link it in your pull request; a claim made only in the pull request isn't enough.
4. **Substantially built with AI.** Most of the code was produced through AI-assisted development, not just fixes, tests, or documentation.
5. **Used by someone besides the author.** At least one of: a public repo with stars or forks from others, a store listing with ratings or reviews, a launch post with discussion (Hacker News, Reddit, Product Hunt, and so on), or coverage by someone else.
6. **You built it or have permission to submit it.**

Links are checked automatically every week. An entry whose link is broken is removed, and can be re-added once it works again.

### What We're NOT Looking For

- AI coding tools themselves (those belong in [awesome-vibe-coding](https://github.com/filipecalegario/awesome-vibe-coding))
- Templates, boilerplates, starter kits, and tutorial or course projects
- Projects that only used AI for minor fixes or documentation
- Abandoned or broken projects
- Duplicate entries

## How to Submit

### Adding Your Project

1. Fork this repository
2. Add your project to the appropriate category in `README.md`
3. Use this format:
   ```markdown
   - [Project Name](link) - A short description ending with a period.
   ```
4. Keep descriptions concise (under 100 characters if possible)
5. Keep entries in alphabetical order (case-insensitive) within the relevant category. In **Apps**, entries are grouped by platform (macOS, iOS, Android, Windows, Linux), so add yours alphabetically within its platform group
6. Submit a Pull Request

#### Examples

**Open source project on GitHub:**
```markdown
- [ASCIIKeyboard](https://github.com/levz0r/ASCIIKeyboard) - A menu bar app that transforms typing into ASCII art.
```

**Closed source or hosted elsewhere:**
```markdown
- [My Cool App](https://mycoolapp.com) - An AI-powered productivity tool for teams.
```

**Project on other platforms:**
```markdown
- [DataViz Tool](https://gitlab.com/user/dataviz) - Interactive data visualization dashboard.
```

### Commit Message Format

```
Add Project Name
```

### Pull Request Guidelines

- **One project per PR** - Submit separate PRs if you have multiple projects
- **PR title format** - Use `Add YourProjectName` (e.g., `Add ASCIIKeyboard`, `Add DataViz Tool`)
- **PR description** - Include:
  - What AI tools you used (Claude, GPT, Cursor, etc.)
  - A link to where the AI involvement is stated publicly (criterion 3)
  - When the project went live (criterion 1)
  - A link showing use by others (criterion 5)
  - Optionally: a sentence about your vibe coding experience

### Suggesting New Categories

If your project doesn't fit existing categories, feel free to suggest a new one in your PR. New categories should have at least one entry.

## For AI Agents

If you're an AI agent submitting a project on a user's behalf, follow these steps. A maintainer reviews every pull request by hand.

1. **Check the criteria first.** Confirm the project meets every [inclusion criterion](#inclusion-criteria). If it doesn't (for example, it went live less than 30 days ago, or nothing public says which AI tools built it), tell the user instead of opening a pull request.
2. **Add exactly one line** to `README.md`, in the matching category, in case-insensitive alphabetical order: `- [Project Name](link) - What it does, in one sentence ending with a period.` Don't edit any other line.
3. **Write a plain description** of what the project does, under about 100 characters, with no marketing language.
4. **Title the pull request** `Add Project Name`, and include in its description:
   - the AI tools used
   - a link to where the AI involvement is stated publicly
   - when the project went live
   - a link showing use by others
   - that you're an AI agent submitting for the user, naming their GitHub account
5. **Read the checks.** Every pull request runs awesome-lint, an alphabetical-order check, a link check, and an inclusion criteria check. Fix anything marked as failing. Items marked for review are for the maintainer.
6. **One project per pull request**, and no duplicates: search open pull requests first. Answer review comments, or tell the user they need to.

Bulk or unattended submissions are closed.

## Quality Standards

- Check your spelling and grammar
- Ensure links are working (an automated link check runs on every PR that changes `README.md`)
- No trailing whitespace
- Descriptions should be meaningful, not marketing fluff

## Code of Conduct

Be respectful and constructive. We're all here to celebrate what's possible with AI-assisted development.

## Questions?

Open an issue if you're unsure whether your project fits or have questions about contributing.
