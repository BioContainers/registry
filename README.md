BioContainers Web
==============================

The [main page of BioContainers](https://biocontainers.pro) and the
[registry](https://biocontainers.pro/registry), served as a **fully static site on
GitHub Pages** — no backend, no database. The tool catalog is regenerated from upstream by a
pipeline that runs in GitHub Actions and is committed into the repo as static JSON; search runs
entirely in the browser.

Repository layout
---------------------------------

- **`pipeline/`** — Python CLI that regenerates the static catalog from two upstream families:
  - bioconda recipes + `quay.io/biocontainers` container tags
  - `BioContainers/containers` Dockerfiles + DockerHub `biocontainers` tags

  It writes the data contract into **`data/`**: `search-index.json`, `tools/<id>.json`,
  `facets.json`, `stats.json`. See `docs/` for the design spec and plans.

- **`web/`** — the Vue 3 + Vite single-page app. It reads only the static `data/` files and
  searches client-side with [MiniSearch](https://github.com/lucaong/minisearch). Three screens:
  Home (stats), Registry (search + facets), Tool detail (versions + container pull commands).

- **`data/`** — the generated catalog, committed to the repo and served alongside the app.

Workflows
---------------------------------

- **`.github/workflows/data-build.yml`** — weekly (and manual) run of the pipeline; commits an
  updated `data/` to the default branch.
- **`.github/workflows/deploy.yml`** — on push, builds `web/` and publishes it (with `data/`) to
  GitHub Pages at `biocontainers.pro`.

Local development
---------------------------------

Build a small sample catalog and run the app against it:

```bash
# 1. Generate a sample data/ catalog (needs Python 3.11+)
cd pipeline
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -m biocontainers_pipeline.cli build --out ../data --only quay --limit 60

# 2. Run the web app (needs Node 20+); web/public/data symlinks to ../../data
cd ../web
npm install
npm run dev
```

Tests: `cd pipeline && .venv/bin/python -m pytest` and `cd web && npm test`.

Contributing
--------------------

Open a PR against the default branch; merges deploy automatically to https://biocontainers.pro
