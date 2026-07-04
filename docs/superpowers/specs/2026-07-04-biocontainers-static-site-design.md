# BioContainers.pro — Static, Backend‑Free Site Design

**Date:** 2026-07-04
**Status:** Approved (brainstorming complete)
**Author:** ypriverol + Claude

## Goal

Replace the current backend-driven biocontainers.pro (Vue 2 SPA + Flask/GA4GH‑TRS API +
MongoDB) with a **fully static site** hosted on GitHub Pages. The content stays
equivalent, search still works — but there is **no server at runtime**. All data is
regenerated from upstream by a pipeline that runs in **GitHub Actions**, committed into the
repo as static JSON, and searched entirely in the browser.

## Key decisions

- **Data strategy:** Regenerate from upstream (not a one-off snapshot of the old API).
- **Sources — exactly two pipelines, nothing else pulled:**
  1. **bioconda → quay.io:** metadata from `bioconda-recipes` `meta.yaml`
     (home, license, summary, doc); container tags + pull stats from the
     `quay.io/biocontainers` API.
  2. **Dockerfile → DockerHub:** metadata from `BioContainers/containers` Dockerfile
     LABELs; tags + stats from the DockerHub `biocontainers` namespace API.
- **No other sources:** no bio.tools, no `tools-metadata` annotations, no
  `multi-package-containers` (mulled), no Singularity depot as a *data* source.
- **Container commands are constructed, not fetched** from `name` + `tag`:
  - Docker (bioconda): `quay.io/biocontainers/<name>:<tag>`
  - Docker (dockerfile): `biocontainers/<name>:<tag>`
  - Singularity (bioconda): `https://depot.galaxyproject.org/singularity/<name>:<tag>`
  - Conda (bioconda): `conda install -c bioconda <name>=<version>`
- **No dedup / normalization machinery:** drop `anchor_tool`, cross-tool grouping, and
  mulled `contains`. **1 package = 1 tool.** The only grouping left: a package's container
  tags (`1.19--h50ea8bc_0`, `1.19--py_0`, …) are grouped under their software version `1.19`.
- **No `source` family label:** provenance is implicit in each version's container list.
  Facets are **license / toolclass / registry**.
- **Frontend:** modernize Vue 2 → **Vue 3 + Vite + Vue Router 4 + Pinia**; port `iview` →
  **View UI Plus** (Vue 3 successor) to keep the look with a mechanical port.
- **Search:** client-side **MiniSearch** over a prebuilt index; no server.
- **Dropped features:** vulnerability scan modal, "similar tools".
- **Repo layout:** single repo (evolve the existing `registry/` repo); **data committed**
  to `main`.
- **Everything runs in GitHub Actions** (local run supported as fallback). Data-build
  commits **directly to `main`** (with `[skip ci]` on the data commit).

## Architecture

```
build time (GitHub Actions, weekly + manual):
  Pipeline 1: bioconda-recipes meta.yaml + quay.io/biocontainers tags ─┐
  Pipeline 2: BioContainers/containers Dockerfiles + dockerhub tags ───┤─▶ normalize
                                                                        └─▶ precompute
                                                                            facets, stats
                                                                        ─▶ committed data/

runtime (browser only, GitHub Pages @ biocontainers.pro):
  Vue 3 + Vite SPA
   • MiniSearch loads search-index.json once → search + browse + client-side facets
   • tool detail lazy-fetches tools/<id>.json (versions, container pull commands)
   • facets.json / stats.json read statically
   • 404.html SPA deep-link fallback · CNAME biocontainers.pro
```

## Data contract (`data/`) — the only interface between pipeline and frontend

### `data/search-index.json`
Array, one lightweight record per tool. Loaded once; fed to MiniSearch; also the browse +
client-side facet source.
```json
{ "id":"samtools", "name":"samtools",
  "description":"Tools for manipulating SAM/BAM/CRAM",
  "license":"MIT", "toolclass":"CommandLineTool",
  "registries":["quay.io","conda","singularity"],
  "latest_version":"1.19", "versionCount":42, "total_pulls":1234567 }
```

### `data/tools/<id>.json`
Full detail, lazy-fetched when a tool page opens. Container commands constructed from
name+tag.
```json
{ "id":"samtools", "name":"samtools", "home_url":"http://www.htslib.org/",
  "description":"...", "license":"MIT", "toolclass":"CommandLineTool",
  "total_pulls":1234567,
  "versions":[
    { "version":"1.19", "last_updated":"2024-01-10",
      "containers":[
        {"type":"docker","image":"quay.io/biocontainers/samtools:1.19--h50ea8bc_0","pulls":1000},
        {"type":"singularity","url":"https://depot.galaxyproject.org/singularity/samtools:1.19--h50ea8bc_0"},
        {"type":"conda","command":"conda install -c bioconda samtools=1.19"} ] } ] }
```
For a Dockerfile-derived tool, versions carry a single docker container
(`biocontainers/<name>:<tag>`) and no conda/singularity lines.

### `data/facets.json`
Precomputed counts for `license`, `toolclass`, `registry`.
```json
[ {"facet":"license","values":[{"value":"MIT","count":744}, ...]},
  {"facet":"toolclass","values":[...]},
  {"facet":"registry","values":[{"value":"quay.io","count":14000},{"value":"DockerHub","count":767}]} ]
```

### `data/stats.json`
```json
{ "tools":14767, "versions":152340, "total_pulls":987654321,
  "registries":{"quay.io":14000,"DockerHub":767}, "generated":"2026-07-04" }
```

**Notes:** ~15k files in `data/tools/` is fine for git + Pages (shard by first letter only
if it becomes heavy — not now). Pull counts are the most volatile field; round/bucket them
so weekly regen diffs stay small.

## Components

### Sub-project A — Data build pipeline (Python CLI)
- **Pipeline 1 (bioconda→quay):** list `quay.io/biocontainers` repos + tags + stats;
  join with `bioconda-recipes` `meta.yaml` metadata (home, license, summary, toolclass).
- **Pipeline 2 (dockerfile→dockerhub):** list DockerHub `biocontainers` repos + tags +
  stats; join with `BioContainers/containers` Dockerfile LABEL metadata.
- **Normalize:** 1 package = 1 tool; group tags under software version; construct container
  commands.
- **Precompute:** facets (license/toolclass/registry), stats.
- **Emit:** the four contract file kinds into `data/`.
- **Incremental crawl:** cache previous `data/`; only re-fetch tags for repos whose
  `last_modified` changed — keeps runs inside the Actions 6h limit and avoids rate limits.
- Runnable locally (same CLI) and in Actions.

### Sub-project B — Frontend (Vue 3 + Vite)
- Stack: Vue 3 + Vite + Vue Router 4 + Pinia; UI kit View UI Plus.
- `Index.vue` → `stats.json`. `Registry.vue` → MiniSearch over `search-index.json`,
  facets from `facets.json`, client-side pagination, `name`>`description` boost with
  prefix + light fuzzy. `Tool.vue` → lazy `tools/<id>.json`.
- Remove `VulnerabilitiesModal.vue`, similars, `Multipackage.vue`.
- `store.js`: drop `baseApiURL`; add static `dataBaseURL` (default `/data`).

## Build & deploy (GitHub Actions)
- **`data-build.yml`:** `workflow_dispatch` + weekly `schedule`. Runs the pipeline,
  regenerates `data/`, commits to `main` with `[skip ci]` on the data commit. Incremental
  crawl; rounded pull counts to limit churn.
- **`deploy.yml`:** on push to `main`, Vite build → GitHub Pages. `CNAME=biocontainers.pro`,
  `404.html` SPA fallback.

## Sequencing
- **Phase 0** — freeze this contract; run the pipeline once to produce a real seed `data/`.
- **Sub-project A** and **Sub-project B** then proceed in parallel, both targeting the
  frozen contract.

## Out of scope
Dedup/anchor/mulled logic; bio.tools, tools-metadata, singularity/conda as *data* sources;
vulnerability scanning; similar tools; the old Flask API and MongoDB (removed).
