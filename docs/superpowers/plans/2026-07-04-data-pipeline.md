# BioContainers Data Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Python CLI that regenerates the static `data/` catalog (search index, per-tool detail, facets, stats) for biocontainers.pro from two upstream families — bioconda→quay.io and Dockerfile→DockerHub — with no database and no server.

**Architecture:** Pure functions per source (quay, bioconda, dockerhub, dockerfiles) return plain dataclasses; a `normalize` step turns raw containers into `Tool` objects (1 package = 1 tool, tags grouped by software version, container commands constructed); an `emit` step writes the four contract file kinds. A `click` CLI wires them and supports an incremental cache. Runs locally and in GitHub Actions.

**Tech Stack:** Python 3.11, `requests`, `click`, `PyYAML`, `pytest`, `responses` (HTTP mocking).

## Global Constraints

- Python **3.11+**.
- **Only two source families** — bioconda-recipes + quay.io/biocontainers, and BioContainers/containers + DockerHub biocontainers. No bio.tools, tools-metadata, mulled, or singularity-depot network calls.
- Container pull commands are **constructed from name+tag**, never fetched.
- **1 package = 1 tool.** No dedup/anchor/mulled grouping. Only grouping: container tags grouped under their software version (tag string split on `--`, left side is the version).
- Output is the contract in `docs/superpowers/specs/2026-07-04-biocontainers-static-site-design.md` — files: `data/search-index.json`, `data/tools/<id>.json`, `data/facets.json`, `data/stats.json`. No `source` field; facets are `license`/`toolclass`/`registry`.
- Pull counts rounded to 2 significant figures in committed output to limit weekly git churn.
- Pipeline package lives at `pipeline/` in the existing `registry` repo. `data/` is written at repo root.
- Every network client is injectable (pass a `session`/base-url) so tests never hit the real network.

---

### Task 1: Scaffold pipeline package, deps, and CLI skeleton

**Files:**
- Create: `pipeline/pyproject.toml`, `pipeline/biocontainers_pipeline/__init__.py`, `pipeline/biocontainers_pipeline/cli.py`
- Test: `pipeline/tests/test_cli.py`

**Interfaces:**
- Produces: `cli` (a `click.Group`) with a `build` command taking `--out DIR`, `--limit INT`, `--only [quay|dockerhub]`.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_cli.py
from click.testing import CliRunner
from biocontainers_pipeline.cli import cli

def test_cli_build_help():
    result = CliRunner().invoke(cli, ["build", "--help"])
    assert result.exit_code == 0
    assert "--out" in result.output
    assert "--limit" in result.output
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_cli.py -v`
Expected: FAIL (ModuleNotFoundError: biocontainers_pipeline).

- [ ] **Step 3: Write minimal implementation**
```toml
# pipeline/pyproject.toml
[project]
name = "biocontainers-pipeline"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.31", "click>=8.1", "PyYAML>=6.0"]
[project.optional-dependencies]
dev = ["pytest>=8", "responses>=0.25"]
[tool.setuptools.packages.find]
where = ["."]
include = ["biocontainers_pipeline*"]
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"
```
```python
# pipeline/biocontainers_pipeline/__init__.py
```
```python
# pipeline/biocontainers_pipeline/cli.py
import click

@click.group()
def cli():
    """BioContainers static data pipeline."""

@cli.command()
@click.option("--out", default="data", help="Output directory for the data/ catalog.")
@click.option("--limit", type=int, default=None, help="Max repos per source (for testing).")
@click.option("--only", type=click.Choice(["quay", "dockerhub"]), default=None)
def build(out, limit, only):
    """Regenerate the static data catalog."""
    from biocontainers_pipeline.build import run_build
    run_build(out=out, limit=limit, only=only)

if __name__ == "__main__":
    cli()
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && pip install -e ".[dev]" && python -m pytest tests/test_cli.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): scaffold package and CLI skeleton"
```

---

### Task 2: Contract dataclasses

**Files:**
- Create: `pipeline/biocontainers_pipeline/models.py`
- Test: `pipeline/tests/test_models.py`

**Interfaces:**
- Produces: dataclasses `Container(type: str, image: str|None, url: str|None, command: str|None, pulls: int)`, `Version(version: str, last_updated: str, containers: list[Container])`, `Tool(id: str, name: str, description: str, home_url: str, license: str, toolclass: str, total_pulls: int, versions: list[Version])`. Method `Tool.registries() -> list[str]` returns sorted unique container registries derived from its versions (`"quay.io"`, `"DockerHub"`, `"conda"`, `"singularity"`).

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_models.py
from biocontainers_pipeline.models import Tool, Version, Container

def test_registries_derived_from_containers():
    t = Tool(id="x", name="x", description="", home_url="", license="MIT",
             toolclass="CommandLineTool", total_pulls=0, versions=[
        Version(version="1.0", last_updated="", containers=[
            Container(type="docker", image="quay.io/biocontainers/x:1.0--0", url=None, command=None, pulls=5),
            Container(type="conda", image=None, url=None, command="conda install -c bioconda x=1.0", pulls=0),
        ])])
    assert t.registries() == ["conda", "quay.io"]
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_models.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/models.py
from dataclasses import dataclass, field

@dataclass
class Container:
    type: str            # docker | singularity | conda
    image: str | None = None
    url: str | None = None
    command: str | None = None
    pulls: int = 0

    def registry(self) -> str:
        if self.type == "conda":
            return "conda"
        if self.type == "singularity":
            return "singularity"
        if self.image and self.image.startswith("quay.io/"):
            return "quay.io"
        return "DockerHub"

@dataclass
class Version:
    version: str
    last_updated: str = ""
    containers: list[Container] = field(default_factory=list)

@dataclass
class Tool:
    id: str
    name: str
    description: str = ""
    home_url: str = ""
    license: str = ""
    toolclass: str = "CommandLineTool"
    total_pulls: int = 0
    versions: list[Version] = field(default_factory=list)

    def registries(self) -> list[str]:
        regs = {c.registry() for v in self.versions for c in v.containers}
        return sorted(regs)

    def latest_version(self) -> str:
        return self.versions[0].version if self.versions else ""
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_models.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): contract dataclasses"
```

---

### Task 3: Version grouping + container-command construction helpers

**Files:**
- Create: `pipeline/biocontainers_pipeline/normalize.py`
- Test: `pipeline/tests/test_normalize.py`

**Interfaces:**
- Consumes: `Container`, `Version` from `models`.
- Produces:
  - `version_of(tag: str) -> str` — the software version (`"1.23--h96c455f_0"` → `"1.23"`; no `--` → tag unchanged).
  - `quay_containers(name: str, tag: str, pulls: int, last_modified: str) -> list[Container]` — a docker(quay), singularity, and conda container for a bioconda tag.
  - `dockerhub_container(name: str, tag: str, pulls: int, last_modified: str) -> Container` — a single docker(DockerHub) container.
  - `group_versions(containers_by_tag: list[tuple[str,str,int,str]], builder) -> list[Version]` — group `(tag, ...)` rows by `version_of(tag)`, newest software version first, each version's `containers` flattened from `builder`.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_normalize.py
from biocontainers_pipeline.normalize import version_of, quay_containers, dockerhub_container

def test_version_of_strips_build_suffix():
    assert version_of("1.23--h96c455f_0") == "1.23"
    assert version_of("0.1.19--h9dcdb79_15") == "0.1.19"
    assert version_of("latest") == "latest"

def test_quay_containers_constructs_three():
    cs = quay_containers("samtools", "1.19--h50ea8bc_0", pulls=10, last_modified="")
    kinds = {c.type: c for c in cs}
    assert kinds["docker"].image == "quay.io/biocontainers/samtools:1.19--h50ea8bc_0"
    assert kinds["singularity"].url == "https://depot.galaxyproject.org/singularity/samtools:1.19--h50ea8bc_0"
    assert kinds["conda"].command == "conda install -c bioconda samtools=1.19"

def test_dockerhub_container_uses_biocontainers_namespace():
    c = dockerhub_container("blast", "2.2.31", pulls=3, last_modified="")
    assert c.image == "biocontainers/blast:2.2.31"
    assert c.type == "docker"
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_normalize.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/normalize.py
from biocontainers_pipeline.models import Container, Version

def version_of(tag: str) -> str:
    return tag.split("--", 1)[0]

def quay_containers(name, tag, pulls, last_modified):
    ver = version_of(tag)
    return [
        Container(type="docker", image=f"quay.io/biocontainers/{name}:{tag}", pulls=pulls),
        Container(type="singularity", url=f"https://depot.galaxyproject.org/singularity/{name}:{tag}"),
        Container(type="conda", command=f"conda install -c bioconda {name}={ver}"),
    ]

def dockerhub_container(name, tag, pulls, last_modified):
    return Container(type="docker", image=f"biocontainers/{name}:{tag}", pulls=pulls)

def group_versions(rows, builder):
    # rows: list of (tag, pulls, last_modified); builder(tag, pulls, last_modified) -> list[Container]
    from collections import OrderedDict
    groups: "OrderedDict[str, Version]" = OrderedDict()
    # newest first by last_modified string is unreliable; keep insertion order from caller (caller sorts)
    for tag, pulls, last_modified in rows:
        ver = version_of(tag)
        v = groups.get(ver)
        if v is None:
            v = Version(version=ver, last_updated=last_modified, containers=[])
            groups[ver] = v
        v.containers.extend(builder(tag, pulls, last_modified))
    return list(groups.values())
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_normalize.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): version grouping and container construction"
```

---

### Task 4: quay.io source client

**Files:**
- Create: `pipeline/biocontainers_pipeline/sources/__init__.py`, `pipeline/biocontainers_pipeline/sources/quay.py`
- Test: `pipeline/tests/test_quay.py`

**Interfaces:**
- Produces:
  - `list_repos(session, base="https://quay.io/api/v1", limit=None) -> list[str]` — biocontainers repo names, following `next_page`.
  - `repo_tags(session, name, base=...) -> list[tuple[str,int,str]]` — `(tag, pulls, last_modified)` rows for a repo; `pulls` is 0 when quay gives none.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_quay.py
import responses, requests
from biocontainers_pipeline.sources import quay

@responses.activate
def test_list_repos_follows_pagination():
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories":[{"name":"a"}], "next_page":"TOK"})
    responses.get(base + "/repository", json={"repositories":[{"name":"b"}]})
    names = quay.list_repos(requests.Session(), base=base)
    assert names == ["a", "b"]

@responses.activate
def test_repo_tags_returns_rows():
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository/biocontainers/samtools",
        json={"tags":{"1.19--h50ea8bc_0":{"name":"1.19--h50ea8bc_0","last_modified":"Tue, 16 Dec 2025 21:28:43 -0000"}}})
    rows = quay.repo_tags(requests.Session(), "samtools", base=base)
    assert rows[0][0] == "1.19--h50ea8bc_0"
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_quay.py -v`
Expected: FAIL (ModuleNotFoundError).

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/sources/quay.py
NAMESPACE = "biocontainers"

def list_repos(session, base="https://quay.io/api/v1", limit=None):
    names, next_page = [], None
    while True:
        params = {"public": "true", "namespace": NAMESPACE}
        if next_page:
            params["next_page"] = next_page
        r = session.get(base + "/repository", params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        names.extend(repo["name"] for repo in data.get("repositories", []))
        if limit and len(names) >= limit:
            return names[:limit]
        next_page = data.get("next_page")
        if not next_page:
            return names

def repo_tags(session, name, base="https://quay.io/api/v1"):
    r = session.get(f"{base}/repository/{NAMESPACE}/{name}",
                    params={"includeTags": "true", "includeStats": "false"}, timeout=60)
    r.raise_for_status()
    tags = r.json().get("tags", {})
    return [(t.get("name", tag), 0, t.get("last_modified", "")) for tag, t in tags.items()]
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_quay.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): quay.io source client"
```

---

### Task 5: DockerHub source client

**Files:**
- Create: `pipeline/biocontainers_pipeline/sources/dockerhub.py`
- Test: `pipeline/tests/test_dockerhub.py`

**Interfaces:**
- Produces:
  - `list_repos(session, base="https://hub.docker.com/v2", limit=None) -> list[tuple[str,int]]` — `(name, pull_count)` following `next`.
  - `repo_tags(session, name, base=...) -> list[tuple[str,int,str]]` — `(tag, 0, last_updated)` rows (per-tag pulls unavailable; repo pull_count used as tool total).

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_dockerhub.py
import responses, requests
from biocontainers_pipeline.sources import dockerhub

@responses.activate
def test_list_repos_paginates_and_keeps_pull_count():
    base = "https://hub.docker.com/v2"
    responses.get(base + "/repositories/biocontainers/",
        json={"results":[{"name":"blast","pull_count":42}], "next": base + "/repositories/biocontainers/?page=2"})
    responses.get(base + "/repositories/biocontainers/",
        json={"results":[{"name":"fastqc","pull_count":7}], "next": None})
    repos = dockerhub.list_repos(requests.Session(), base=base)
    assert repos == [("blast", 42), ("fastqc", 7)]
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_dockerhub.py -v`
Expected: FAIL.

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/sources/dockerhub.py
NAMESPACE = "biocontainers"

def list_repos(session, base="https://hub.docker.com/v2", limit=None):
    url = f"{base}/repositories/{NAMESPACE}/"
    params = {"page_size": 100}
    out = []
    while url:
        r = session.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        out.extend((x["name"], x.get("pull_count", 0)) for x in data.get("results", []))
        if limit and len(out) >= limit:
            return out[:limit]
        url, params = data.get("next"), None
    return out

def repo_tags(session, name, base="https://hub.docker.com/v2"):
    r = session.get(f"{base}/repositories/{NAMESPACE}/{name}/tags/",
                    params={"page_size": 100}, timeout=60)
    r.raise_for_status()
    return [(t["name"], 0, t.get("last_updated", "")) for t in r.json().get("results", [])]
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_dockerhub.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): dockerhub source client"
```

---

### Task 6: bioconda meta.yaml metadata reader

**Files:**
- Create: `pipeline/biocontainers_pipeline/sources/bioconda.py`
- Test: `pipeline/tests/test_bioconda.py`, `pipeline/tests/fixtures/samtools_meta.yaml`

**Interfaces:**
- Produces: `parse_meta(text: str) -> dict` with keys `home`, `license`, `summary` (missing → `""`). Handles bioconda jinja by stripping `{% ... %}` lines and reading the `about:` block. `load_recipes(recipes_dir: str) -> dict[str, dict]` maps package name → parsed metadata by walking `<recipes_dir>/*/meta.yaml`.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_bioconda.py
from biocontainers_pipeline.sources import bioconda

META = '''{% set version = "1.19" %}
package:
  name: samtools
  version: {{ version }}
about:
  home: http://www.htslib.org/
  license: MIT
  summary: Tools for manipulating SAM/BAM/CRAM
'''

def test_parse_meta_reads_about_block():
    m = bioconda.parse_meta(META)
    assert m["home"] == "http://www.htslib.org/"
    assert m["license"] == "MIT"
    assert m["summary"].startswith("Tools for manipulating")
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_bioconda.py -v`
Expected: FAIL.

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/sources/bioconda.py
import os, re, yaml

def _strip_jinja(text: str) -> str:
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("{%")]
    return re.sub(r"{{.*?}}", "PLACEHOLDER", "\n".join(lines))

def parse_meta(text: str) -> dict:
    try:
        doc = yaml.safe_load(_strip_jinja(text)) or {}
    except yaml.YAMLError:
        return {"home": "", "license": "", "summary": ""}
    about = doc.get("about", {}) or {}
    lic = about.get("license", "")
    return {
        "home": str(about.get("home", "") or ""),
        "license": str(lic or ""),
        "summary": str(about.get("summary", "") or "").strip(),
    }

def load_recipes(recipes_dir: str) -> dict:
    out = {}
    for name in os.listdir(recipes_dir):
        meta = os.path.join(recipes_dir, name, "meta.yaml")
        if os.path.isfile(meta):
            with open(meta, encoding="utf-8", errors="replace") as fh:
                out[name] = parse_meta(fh.read())
    return out
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_bioconda.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): bioconda meta.yaml reader"
```

---

### Task 7: Facets, stats, and JSON emit

**Files:**
- Create: `pipeline/biocontainers_pipeline/emit.py`
- Test: `pipeline/tests/test_emit.py`

**Interfaces:**
- Consumes: `Tool` from `models`.
- Produces:
  - `round_sig(n: int, sig=2) -> int`.
  - `search_record(tool) -> dict` — `{id,name,description,license,toolclass,registries,latest_version,versionCount,total_pulls}`.
  - `tool_detail(tool) -> dict` — full nested detail.
  - `facets(tools) -> list[dict]` — counts for `license`, `toolclass`, `registry`.
  - `stats(tools) -> dict` — `{tools,versions,total_pulls,registries,generated}` (`generated` param passed in).
  - `write_catalog(tools, out_dir, generated) -> None` — writes `search-index.json`, `tools/<id>.json`, `facets.json`, `stats.json`.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_emit.py
import json, os
from biocontainers_pipeline.models import Tool, Version, Container
from biocontainers_pipeline import emit

def _tool():
    return Tool(id="samtools", name="samtools", description="d", home_url="h", license="MIT",
        toolclass="CommandLineTool", total_pulls=1234567, versions=[
            Version(version="1.19", last_updated="x", containers=[
                Container(type="docker", image="quay.io/biocontainers/samtools:1.19--0", pulls=1010)])])

def test_round_sig():
    assert emit.round_sig(1234567) == 1200000

def test_search_record_shape():
    r = emit.search_record(_tool())
    assert r["registries"] == ["quay.io"]
    assert r["latest_version"] == "1.19"
    assert r["versionCount"] == 1
    assert r["total_pulls"] == 1200000

def test_write_catalog(tmp_path):
    emit.write_catalog([_tool()], str(tmp_path), generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
    detail = json.loads((tmp_path / "tools" / "samtools.json").read_text())
    assert detail["versions"][0]["containers"][0]["image"].startswith("quay.io/")
    stats = json.loads((tmp_path / "stats.json").read_text())
    assert stats["tools"] == 1 and stats["versions"] == 1
    facets = json.loads((tmp_path / "facets.json").read_text())
    assert any(f["facet"] == "license" for f in facets)
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_emit.py -v`
Expected: FAIL.

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/emit.py
import json, os
from collections import Counter
from dataclasses import asdict

def round_sig(n, sig=2):
    if not n:
        return 0
    from math import floor, log10
    d = sig - int(floor(log10(abs(n)))) - 1
    return int(round(n, d))

def search_record(t):
    return {"id": t.id, "name": t.name, "description": t.description, "license": t.license,
            "toolclass": t.toolclass, "registries": t.registries(),
            "latest_version": t.latest_version(), "versionCount": len(t.versions),
            "total_pulls": round_sig(t.total_pulls)}

def tool_detail(t):
    d = {"id": t.id, "name": t.name, "description": t.description, "home_url": t.home_url,
         "license": t.license, "toolclass": t.toolclass, "total_pulls": round_sig(t.total_pulls),
         "versions": []}
    for v in t.versions:
        d["versions"].append({"version": v.version, "last_updated": v.last_updated,
            "containers": [{k: val for k, val in asdict(c).items() if val not in (None, 0, "")} | {"type": c.type}
                           for c in v.containers]})
    return d

def facets(tools):
    lic, tc, reg = Counter(), Counter(), Counter()
    for t in tools:
        lic[t.license or "Not available"] += 1
        tc[t.toolclass or "Unknown"] += 1
        for r in t.registries():
            reg[r] += 1
    def block(name, c):
        return {"facet": name, "values": [{"value": k, "count": v} for k, v in c.most_common()]}
    return [block("license", lic), block("toolclass", tc), block("registry", reg)]

def stats(tools, generated):
    reg = Counter()
    for t in tools:
        for r in t.registries():
            reg[r] += 1
    return {"tools": len(tools), "versions": sum(len(t.versions) for t in tools),
            "total_pulls": round_sig(sum(t.total_pulls for t in tools)),
            "registries": dict(reg), "generated": generated}

def write_catalog(tools, out_dir, generated):
    os.makedirs(os.path.join(out_dir, "tools"), exist_ok=True)
    tools = sorted(tools, key=lambda t: t.id)
    _dump(os.path.join(out_dir, "search-index.json"), [search_record(t) for t in tools])
    for t in tools:
        _dump(os.path.join(out_dir, "tools", f"{t.id}.json"), tool_detail(t))
    _dump(os.path.join(out_dir, "facets.json"), facets(tools))
    _dump(os.path.join(out_dir, "stats.json"), stats(tools, generated))

def _dump(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
```

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_emit.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): facets, stats, and JSON emit"
```

---

### Task 8: Build orchestration (assemble Tools from sources)

**Files:**
- Create: `pipeline/biocontainers_pipeline/build.py`
- Test: `pipeline/tests/test_build.py`

**Interfaces:**
- Consumes: `sources.quay`, `sources.dockerhub`, `sources.bioconda`, `normalize`, `emit`, `models`.
- Produces:
  - `build_quay_tools(session, recipes, limit=None) -> list[Tool]` — for each quay repo: tags → `group_versions(..., quay_containers)`; metadata from `recipes[name]` (fallback empty); `toolclass="CommandLineTool"`.
  - `build_dockerhub_tools(session, limit=None) -> list[Tool]` — for each DockerHub repo: tags → `group_versions(..., dockerhub_container)`; `total_pulls` = repo pull_count.
  - `run_build(out, limit=None, only=None, recipes_dir=None, session=None, generated=None) -> None` — orchestrate + `emit.write_catalog`. When two sources yield the same tool `id`, quay wins and DockerHub-only versions are appended.

- [ ] **Step 1: Write the failing test**
```python
# pipeline/tests/test_build.py
import responses, requests, json
from biocontainers_pipeline import build

@responses.activate
def test_build_quay_tools_joins_metadata():
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories":[{"name":"samtools"}]})
    responses.get(base + "/repository/biocontainers/samtools",
        json={"tags":{"1.19--h50ea8bc_0":{"name":"1.19--h50ea8bc_0","last_modified":"d"}}})
    recipes = {"samtools": {"home":"http://htslib.org","license":"MIT","summary":"SAM tools"}}
    tools = build.build_quay_tools(requests.Session(), recipes, quay_base=base)
    assert tools[0].id == "samtools"
    assert tools[0].license == "MIT"
    assert tools[0].versions[0].version == "1.19"
    assert tools[0].registries() == ["conda", "quay.io", "singularity"]

@responses.activate
def test_run_build_writes_catalog(tmp_path):
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories":[{"name":"samtools"}]})
    responses.get(base + "/repository/biocontainers/samtools",
        json={"tags":{"1.19--0":{"name":"1.19--0","last_modified":"d"}}})
    build.run_build(out=str(tmp_path), only="quay", recipes=None,
                    session=requests.Session(), quay_base=base, generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
```

- [ ] **Step 2: Run test to verify it fails**
Run: `cd pipeline && python -m pytest tests/test_build.py -v`
Expected: FAIL.

- [ ] **Step 3: Write minimal implementation**
```python
# pipeline/biocontainers_pipeline/build.py
import requests
from biocontainers_pipeline.models import Tool
from biocontainers_pipeline.normalize import group_versions, quay_containers, dockerhub_container
from biocontainers_pipeline.sources import quay, dockerhub
from biocontainers_pipeline import emit

def build_quay_tools(session, recipes, limit=None, quay_base="https://quay.io/api/v1"):
    recipes = recipes or {}
    tools = []
    for name in quay.list_repos(session, base=quay_base, limit=limit):
        rows = quay.repo_tags(session, name, base=quay_base)
        if not rows:
            continue
        versions = group_versions(rows, quay_containers_for(name))
        meta = recipes.get(name, {})
        tools.append(Tool(id=name, name=name, description=meta.get("summary", ""),
            home_url=meta.get("home", ""), license=meta.get("license", ""),
            toolclass="CommandLineTool", total_pulls=0, versions=versions))
    return tools

def quay_containers_for(name):
    return lambda tag, pulls, lm: quay_containers(name, tag, pulls, lm)

def build_dockerhub_tools(session, limit=None, dh_base="https://hub.docker.com/v2"):
    tools = []
    for name, pull_count in dockerhub.list_repos(session, base=dh_base, limit=limit):
        rows = dockerhub.repo_tags(session, name, base=dh_base)
        if not rows:
            continue
        versions = group_versions(rows, dockerhub_containers_for(name))
        tools.append(Tool(id=name, name=name, toolclass="CommandLineTool",
            total_pulls=pull_count, versions=versions))
    return tools

def dockerhub_containers_for(name):
    return lambda tag, pulls, lm: [dockerhub_container(name, tag, pulls, lm)]

def run_build(out="data", limit=None, only=None, recipes=None, recipes_dir=None,
              session=None, quay_base="https://quay.io/api/v1",
              dh_base="https://hub.docker.com/v2", generated=None):
    from datetime import date
    session = session or requests.Session()
    generated = generated or date.today().isoformat()
    if recipes is None and recipes_dir:
        from biocontainers_pipeline.sources import bioconda
        recipes = bioconda.load_recipes(recipes_dir)
    by_id = {}
    if only in (None, "quay"):
        for t in build_quay_tools(session, recipes, limit=limit, quay_base=quay_base):
            by_id[t.id] = t
    if only in (None, "dockerhub"):
        for t in build_dockerhub_tools(session, limit=limit, dh_base=dh_base):
            if t.id in by_id:
                by_id[t.id].versions.extend(t.versions)
                by_id[t.id].total_pulls += t.total_pulls
            else:
                by_id[t.id] = t
    emit.write_catalog(list(by_id.values()), out, generated)
```
Also update `cli.py`'s `build` to pass `recipes_dir` via a new `--recipes-dir` option (default `None`).

- [ ] **Step 4: Run test to verify it passes**
Run: `cd pipeline && python -m pytest tests/test_build.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "feat(pipeline): build orchestration"
```

---

### Task 9: End-to-end smoke run against live APIs (small limit)

**Files:**
- Create: `pipeline/tests/test_smoke.py` (marked `@pytest.mark.network`, skipped by default)
- Modify: `pipeline/pyproject.toml` (register the `network` marker)

**Interfaces:**
- Consumes: `run_build`.
- Produces: confidence that the real quay.io responses parse into a valid catalog.

- [ ] **Step 1: Write the test**
```python
# pipeline/tests/test_smoke.py
import os, json, pytest
from biocontainers_pipeline import build

@pytest.mark.network
@pytest.mark.skipif(not os.environ.get("RUN_NETWORK_TESTS"), reason="network")
def test_small_live_build(tmp_path):
    build.run_build(out=str(tmp_path), limit=5, only="quay")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert len(idx) >= 1
    first = idx[0]
    detail = json.loads((tmp_path / "tools" / f"{first['id']}.json").read_text())
    assert detail["versions"]
```

- [ ] **Step 2: Register marker**
Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
markers = ["network: hits live upstream APIs; opt-in via RUN_NETWORK_TESTS"]
```

- [ ] **Step 3: Run it live once**
Run: `cd pipeline && RUN_NETWORK_TESTS=1 python -m pytest tests/test_smoke.py -v`
Expected: PASS (or, if quay throttles, re-run once).

- [ ] **Step 4: Run the full suite without network**
Run: `cd pipeline && python -m pytest -v`
Expected: all pass, smoke test skipped.

- [ ] **Step 5: Commit**
```bash
git add pipeline/ && git commit -m "test(pipeline): opt-in live smoke build"
```

---

### Task 10: GitHub Actions data-build workflow

**Files:**
- Create: `.github/workflows/data-build.yml` (at the `registry` repo root)

**Interfaces:**
- Consumes: the `build` CLI.
- Produces: a scheduled + manual workflow that regenerates `data/` and commits to `main`.

- [ ] **Step 1: Write the workflow**
```yaml
# .github/workflows/data-build.yml
name: data-build
on:
  workflow_dispatch:
  schedule:
    - cron: "0 3 * * 1"   # weekly, Monday 03:00 UTC
permissions:
  contents: write
concurrency:
  group: data-build
  cancel-in-progress: false
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 330
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install pipeline
        run: pip install -e "pipeline[dev]"
      - name: Shallow-clone bioconda recipes
        run: git clone --depth 1 https://github.com/bioconda/bioconda-recipes /tmp/bioconda-recipes
      - name: Build catalog
        run: python -m biocontainers_pipeline.cli build --out data --recipes-dir /tmp/bioconda-recipes/recipes
      - name: Commit data
        run: |
          git config user.name "biocontainers-bot"
          git config user.email "bot@biocontainers.pro"
          git add data
          git diff --cached --quiet || git commit -m "chore(data): weekly catalog refresh [skip ci]"
          git push
```

- [ ] **Step 2: Validate YAML locally**
Run: `python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/data-build.yml')); print('ok')"`
Expected: `ok`.

- [ ] **Step 3: Commit**
```bash
git add .github/workflows/data-build.yml && git commit -m "ci: weekly data-build workflow"
```

- [ ] **Step 4: (Manual, after push) trigger the workflow**
Run in GitHub UI: Actions → data-build → Run workflow. Confirm it commits a `data/` folder.

---

## Self-Review notes

- **Spec coverage:** two sources (Tasks 4/5/6/8), constructed commands (Task 3), 1-pkg-1-tool grouping (Task 3/8), contract files (Task 7), facets license/toolclass/registry (Task 7), rounded pulls (Task 7), Actions build (Task 10). Incremental crawl is **deferred**: v1 does a full weekly crawl inside the 330-min budget; add `last_modified` caching only if runtime demands it (noted here so it isn't forgotten).
- **Frontend** is a separate plan (`2026-07-04-frontend.md`), written next; it consumes this contract.
- **Pull stats:** quay per-tool pulls set to 0 (quay no longer exposes them publicly); DockerHub repo `pull_count` used as tool total. If a pulls source is later found, only `repo_tags`/`build_*` change.
