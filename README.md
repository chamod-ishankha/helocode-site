# HeloCode Labs — website

Static site hosted on GitHub Pages. Serves the public legal pages that Google
Play requires for each app.

**This repository must stay public** — GitHub Pages only publishes from public
repositories on the free plan. It contains no source code and no secrets.

## Pages

| Path | Purpose |
| --- | --- |
| `index.html` | Landing page |
| `nakshatra/privacy.html` | Privacy policy (required by Play) |
| `nakshatra/terms.html` | Terms of service |

CSS is inlined in each page on purpose: a privacy policy has to render even if
a relative path breaks, and the pages are small enough that duplication costs
nothing.

## Adding a new app

Copy the `nakshatra/` folder, rename it, update the content, and link it from
`index.html`.
