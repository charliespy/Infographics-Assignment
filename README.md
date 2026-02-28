# Infographics Assignment

A Jekyll site for showcasing infographics, hosted on GitHub Pages.

## Local Development

### Option A: Static preview (no Ruby required)

Build the home page into `preview/index.html` and serve it locally. The preview **auto-updates** when you run the script in watch mode.

```bash
# Build once
python3 scripts/build_preview.py

# Serve (in one terminal)
python3 -m http.server 8000

# Auto-rebuild on changes (in another terminal)
python3 scripts/build_preview.py --watch
```

Then open [http://localhost:8000/preview/](http://localhost:8000/preview/). Edit `index.html`, `_layouts/default.html`, `_config.yml`, or `assets/css/style.css` — the watcher will rebuild the preview so a browser refresh shows your changes.

### Option B: Full Jekyll (Ruby + Bundler)

**Prerequisites:** Ruby and Bundler installed.

```bash
bundle install
bundle exec jekyll serve
```

Then open [http://localhost:4000/Infographics-Assignment/](http://localhost:4000/Infographics-Assignment/) in your browser.

## Adding the three reference graphics

The "Three Graphics" section on the site displays images from `assets/images/` with these filenames:

- `graphic-1-colonialism.png` — [Our World in Data: Colonialism](https://ourworldindata.org/data-insights/colonialism-meant-that-for-centuries-many-territories-and-people-were-ruled-from-elsewhere)
- `graphic-2-income-inequality.png` — [Our World in Data: Global income inequality](https://ourworldindata.org/grapher/global-and-between-country-income-inequality)
- `graphic-3-mapping-deportations.png` — [Mapping the "White Man's Republic"](https://mappingdeportations.com/2025/09/15/the-roots-of-immigration-control/)

To add or refresh them: open each link, use your browser’s screenshot tool or “Save as PDF” (then crop/export as PNG), and save into `assets/images/` with the names above. Keep the citations on the site in sync with the sources.

## Adding Content

1. **Infographic images** — Drop them into `assets/images/`.
2. **New pages** — Create a Markdown file (e.g. `my-infographic.md`) in the root with front matter:

```yaml
---
layout: page
title: My Infographic
---
```

3. **Navigation** — Add the page to the `navigation` list in `_config.yml`:

```yaml
navigation:
  - title: My Infographic
    url: /my-infographic/
```

## Deploying to GitHub Pages

1. Push to the `main` branch.
2. In your repo settings, go to **Pages** and set the source to **Deploy from a branch** → `main` / `/ (root)`.
3. The site will be live at `https://<username>.github.io/Infographics-Assignment/`.
