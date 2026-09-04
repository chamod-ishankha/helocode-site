#!/usr/bin/env python3
"""Assemble the static site.

Pages are written as body fragments in src/ and wrapped in a shared shell here.
The stylesheet is inlined into every page rather than linked: a privacy policy
has to render even if a relative path breaks, and these pages are small enough
that duplication is cheaper than that failure mode.

Run:  python build.py
"""

import io
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

EMAIL = "helocodeio@gmail.com"
UPDATED = "4 September 2026"

STAR = (
    '<svg viewBox="0 0 100 100" aria-hidden="true">'
    '<path fill="currentColor" d="M50 3 57.5 35.5 81.5 18.5 65 42.5 97 50 '
    '65 57.5 81.5 81.5 57.5 64.5 50 97 42.5 64.5 18.5 81.5 35 57.5 3 50 '
    '35 42.5 18.5 18.5 42.5 35Z"/></svg>'
)

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;600&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<div class="sky"></div>

<nav class="nav">
  <div class="nav-in">
    <a class="brand" href="{root}index.html">
      <span style="color:var(--gold);display:flex">{star}</span>
      <span>HeloCode Labs</span>
    </a>
    <div class="nav-links">
      <a href="{root}nakshatra/privacy.html">Privacy</a>
      <a href="{root}nakshatra/terms.html">Terms</a>
    </div>
  </div>
</nav>

{body}

<footer class="foot">
  <div class="shell foot-in">
    <span>&copy; 2026 HeloCode Labs &middot; Sri Lanka</span>
    <span>
      <a href="{root}nakshatra/privacy.html">Privacy</a> &nbsp;
      <a href="{root}nakshatra/terms.html">Terms</a> &nbsp;
      <a href="mailto:{email}">{email}</a>
    </span>
  </div>
</footer>

</body>
</html>
"""

PAGES = [
    # (body fragment, output path, depth, numbered, title, description)
    #
    # `numbered` drives the legal-document treatment: numbered <h2>s plus a
    # generated table of contents. The landing page is prose, not clauses, so
    # it opts out.
    ("index.body.html", "index.html", 0, False,
     "HeloCode Labs",
     "HeloCode Labs builds mobile apps in Sri Lanka."),
    ("privacy.body.html", "nakshatra/privacy.html", 1, True,
     "Privacy Policy — Nakshatra | HeloCode Labs",
     "How Nakshatra handles your data. Birth details never leave your device."),
    ("terms.body.html", "nakshatra/terms.html", 1, True,
     "Terms of Service — Nakshatra | HeloCode Labs",
     "Terms of service for the Nakshatra astrology and almanac app."),
]


def number_sections(body: str):
    """Number the <h2>s and build a matching table of contents.

    Keeping this generated means section numbers and TOC links can never drift
    apart when the text is edited.
    """
    entries = []

    def repl(m):
        text = m.group(1).strip()
        n = len(entries) + 1
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        entries.append((n, text, slug))
        return f'<h2 id="{slug}"><span class="num">{n:02d}</span>{text}</h2>'

    body = re.sub(r"<h2>(.*?)</h2>", repl, body, flags=re.S)

    if not entries:
        return body, ""

    links = "\n".join(
        f'      <a href="#{slug}">{text}</a>' for _, text, slug in entries
    )
    toc = f'  <aside class="toc">\n    <div class="toc-title">Contents</div>\n{links}\n  </aside>'
    return body, toc


def main():
    css = io.open(os.path.join(SRC, "site.css"), encoding="utf-8").read().strip()

    for frag, out, depth, numbered, title, desc in PAGES:
        body = io.open(os.path.join(SRC, frag), encoding="utf-8").read()
        toc = ""
        if numbered:
            body, toc = number_sections(body)
        body = body.replace("{{TOC}}", toc)
        body = body.replace("{{EMAIL}}", EMAIL)
        body = body.replace("{{UPDATED}}", UPDATED)
        body = body.replace("{{STAR}}", STAR)

        html = SHELL.format(
            title=title, desc=desc, css=css, body=body, star=STAR,
            root="../" if depth else "", email=EMAIL,
        )

        path = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
        io.open(path, "w", encoding="utf-8", newline="\n").write(html)
        print(f"built {out:28} {len(html):>6} bytes")


if __name__ == "__main__":
    main()
