# Prioritize Bioconda over legacy Docker in the registry — Design

**Goal:** In the BioContainers registry (static site), when a tool has a Bioconda source, present
that as the recommended install and demote the tool's legacy Dockerfile/DockerHub image to a
secondary "Legacy image" section. No container rebuilds — a registry data + UI change only.

## Why (context)

Most of the hand-written `BioContainers/containers` Dockerfiles no longer build (EOL Debian
buster/stretch bases); their images survive on DockerHub but are frozen at 2018–2019 and unpatchable.
For any tool that also exists in Bioconda, the quay.io/biocontainers image is the maintained,
patched, multi-arch path. So rather than rebuild the legacy images, we simply steer users to Bioconda
wherever one exists.

From the generated catalog (13,058 tools):
- **344 tools have BOTH** a Bioconda source and a legacy Dockerfile → the target of this change.
- **562 tools are DockerHub-only** (no Bioconda) → **left as-is** (their image is all they have).
- ~12,496 are Bioconda-only → unaffected.

## Current behavior (the bug)

`Tool.versions` merges bioconda + Dockerfile versions into one list sorted purely by version number.
`Tool.latest_version()` returns `versions[0]`, and the frontend's `latestContainer()` also uses
`versions[0]`. So when a legacy Docker version has the highest version string, the tool page's Usage
block promotes the (dead) DockerHub image and `condaCommand()` returns null — Conda is hidden even
though the tool has Bioconda versions.

## Design

### Data / pipeline

`models.py`:
- `latest_version()` → return the newest **Bioconda** version (first version with `build` set) when
  any exist; otherwise `versions[0]` (Docker-only tools unchanged).
- New `primary_source()` → `"bioconda"` if any version has `build` set, else `"dockerhub"`.

`emit.py`:
- `search_record()` and `tool_detail()` emit `"primary"` (`t.primary_source()`).
- `search_record()` emits `registries` ordered conda-family first
  (`conda, quay.io, singularity, DockerHub`) so cards lead with Bioconda.

Per-version records already distinguish source (`build` vs `docker`), so no per-version schema change
is needed for grouping.

### Frontend

`containers.js`:
- New `primaryVersion(tool)` = first version with `build` set, else `versions[0]`.
- `latestContainer(tool, type)` uses `primaryVersion(tool)` instead of `versions[0]`, so
  `condaCommand`/`dockerCommand`/`singularityCommand` (the Usage block) reflect Bioconda for
  dual-source tools; `docker` becomes the quay.io image, not the legacy DockerHub one.

`Tool.vue`:
- Sidebar "latest" uses the primary (Bioconda-preferred) version.
- Packages tab splits versions into **Bioconda** and **legacy Docker** groups
  (`v.build != null` vs `v.docker && v.build == null`):
  - Bioconda group rendered first; labeled "Bioconda packages — recommended" **only when** a legacy
    group also exists (dual-source).
  - Legacy Docker group rendered in a de-emphasized "Legacy Docker image" section with a short note,
    **only when** a Bioconda group also exists. For DockerHub-only tools the Docker versions render
    normally with no "legacy" framing (the 562 are left as-is).

`Registry.vue`:
- Cards use the (now Bioconda-preferred) `latest_version` and the reordered `registries`; add a small
  "bioconda" badge when `item.primary === 'bioconda'`.

## Out of scope

- The 562 DockerHub-only tools (no relabelling this round).
- Any container rebuild / triage / modernization pipeline (explicitly dropped).

## Testing

- Pipeline: `latest_version()` prefers Bioconda; `primary_source()` correct for bioconda-only,
  docker-only, and dual-source tools.
- Web: `latestContainer`/`condaCommand` pick the Bioconda version for a dual-source tool.
- Regenerate data and spot-check a real dual-source tool (e.g. `abyss`, `aragorn`): latest is the
  Bioconda version, Usage shows conda + quay docker + singularity, Packages tab shows the legacy
  DockerHub image under "Legacy Docker image".
