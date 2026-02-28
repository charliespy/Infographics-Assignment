# Infographics Assignment

A Jekyll site for showcasing infographics, hosted on GitHub Pages.

## Local Development

**Prerequisites:** Ruby and Bundler installed.

```bash
bundle install
bundle exec jekyll serve
```

Then open [http://localhost:4000/Infographics-Assignment/](http://localhost:4000/Infographics-Assignment/) in your browser.

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
