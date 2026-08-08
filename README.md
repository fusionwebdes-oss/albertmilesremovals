# Albert Miles Removals — Website

Static website for Albert Miles Removals, a house & office removal company in the West Midlands.

## Tech

- Plain static HTML/CSS/JS with a tiny Python build script (`build.py`).
- `_fragments/*.txt` — page content (one file per generated page).
- `_partials/header.html`, `_partials/footer.html` — shared site chrome.
- Handwritten pages (not generated): `index.html`, `about.html`, `404.html`.

## Build locally

```
python build.py
```

Regenerates the fragment-based pages, `sitemap.xml` and `robots.txt` in the repo root.

## Update the site

1. Edit content in `_fragments/` (or `_partials/`, `index.html`, `about.html`, `404.html`).
2. Run `python build.py` to regenerate pages.
3. Commit and push to `main` — Cloudflare Pages auto-deploys.

## Deploy

Hosted on Cloudflare Pages, connected to this GitHub repo (branch `main`).

- Build command: `python build.py`
- Build output directory: `/`
