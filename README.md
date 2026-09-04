# HeloCode Labs — website

Static site on GitHub Pages, serving the public legal pages Google Play requires
for each app.

**This repository must stay public.** GitHub Pages does not publish from private
repositories on the free plan. It holds no source code and no secrets.

## Live

| Page | URL |
| --- | --- |
| Home | https://chamod-ishankha.github.io/helocode-site/ |
| Nakshatra — Privacy | https://chamod-ishankha.github.io/helocode-site/nakshatra/privacy.html |
| Nakshatra — Terms | https://chamod-ishankha.github.io/helocode-site/nakshatra/terms.html |

## Editing

Do **not** edit the HTML in the repository root — it is generated and will be
overwritten. Edit the sources in `src/`, then rebuild:

```bash
python build.py
```

```
src/site.css            styles, shared by every page
src/index.body.html     landing page content
src/privacy.body.html   privacy policy content
src/terms.body.html     terms of service content
build.py                wraps each fragment in the shared shell
```

`build.py` inlines the stylesheet into every page rather than linking it. A
privacy policy has to render even if a relative path breaks, and the pages are
small enough that duplication is cheaper than that failure mode.

It also numbers the `<h2>` headings on legal pages and generates the table of
contents from them, so section numbers and sidebar links cannot drift apart when
the text is edited. The landing page opts out of that treatment.

Contact email and the "last updated" date are set once at the top of `build.py`.

## Adding another app

1. Copy `src/privacy.body.html` and `src/terms.body.html`, rename for the new app.
2. Add entries to `PAGES` in `build.py` with the output path `<app>/privacy.html`.
3. Link the app from `src/index.body.html`.
4. Run `python build.py` and commit both the sources and the generated HTML.
