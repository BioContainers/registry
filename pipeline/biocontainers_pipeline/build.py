import itertools
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timezone

import requests
from requests.adapters import HTTPAdapter

from biocontainers_pipeline import emit
from biocontainers_pipeline.models import Tool, Version
from biocontainers_pipeline.normalize import version_key
from biocontainers_pipeline.sources import bioconda
from biocontainers_pipeline.sources import containers as containers_src
from biocontainers_pipeline.sources import dockerhub
from biocontainers_pipeline.sources import repodata as repodata_src

try:
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover
    Retry = None

logger = logging.getLogger(__name__)


def make_session():
    s = requests.Session()
    if Retry is not None:
        retry = Retry(
            total=3, backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        s.mount("https://", adapter)
        s.mount("http://", adapter)
    return s


def _iso(ts_ms):
    if not ts_ms:
        return ""
    return datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def build_bioconda_tools(index, recipes=None):
    """index: {name: {version: {build, build_number, timestamp, license}}}.
    recipes: {name: {home, license, summary, version}}."""
    recipes = recipes or {}
    tools = []
    for name in sorted(index):
        version_map = index[name]
        ordered = sorted(
            version_map.values(),
            key=lambda d: version_key(d["version"]),
            reverse=True,
        )
        versions = [
            Version(
                version=d["version"],
                last_updated=_iso(d["timestamp"]),
                build=d["build"],
            )
            for d in ordered
        ]
        meta = recipes.get(name, {})
        license_ = meta.get("license") or (ordered[0]["license"] if ordered else "")
        tools.append(
            Tool(
                id=name,
                name=name,
                description=meta.get("summary", ""),
                long_description=meta.get("description", ""),
                home_url=meta.get("home", ""),
                doc_url=meta.get("doc_url", ""),
                dev_url=meta.get("dev_url", ""),
                license=license_,
                license_family=meta.get("license_family", ""),
                identifiers=meta.get("identifiers", []) or [],
                maintainers=meta.get("maintainers", []) or [],
                dependencies=_clean_deps(ordered[0]["depends"]) if ordered else [],
                total_pulls=0,
                versions=versions,
            )
        )
    return tools


def _clean_deps(depends):
    """Drop virtual/compiler internals (__glibc, libgcc, _openmp_mutex, …) that add
    noise rather than signal on a tool page."""
    out = []
    for dep in depends:
        pkg = dep.split()[0] if dep else ""
        if pkg.startswith("_") or pkg.startswith("lib") or pkg in {"python_abi"}:
            continue
        out.append(dep)
    return out


def _dockerfile_tool(tool, info, session, dh_base):
    """Build one Dockerfile tool, taking real image tags + pulls from DockerHub and
    falling back to the git version dirs if DockerHub has nothing."""
    md = info["metadata"]
    tags = dockerhub.repo_tags(session, tool, base=dh_base)
    if tags:
        best = {}  # software version -> (tag, last_updated), newest kept
        for tag, lu in tags:
            sv = dockerhub.software_version(tag)
            if sv not in best or lu > best[sv][1]:
                best[sv] = (tag, lu)
        versions = [
            Version(
                version=sv,
                last_updated=(best[sv][1][:10] if best[sv][1] else ""),
                docker=f"biocontainers/{tool}:{best[sv][0]}",
            )
            for sv in sorted(best, key=version_key, reverse=True)
        ]
        pulls = dockerhub.repo_pulls(session, tool, base=dh_base)
    else:
        versions = [
            Version(version=v, docker=f"biocontainers/{tool}:{v}")
            for v in sorted(info["versions"], key=version_key, reverse=True)
        ]
        pulls = 0
    identifiers = [f"biotools:{md['biotools']}"] if md.get("biotools") else []
    return Tool(
        id=tool,
        name=tool,
        description=md.get("summary", ""),
        home_url=md.get("home", ""),
        license=md.get("license", ""),
        identifiers=identifiers,
        total_pulls=pulls,
        versions=versions,
    )


def build_dockerfile_tools(catalog, session=None, dh_base="https://hub.docker.com/v2", max_workers=12):
    """catalog: {tool: {"metadata": {...}, "versions": [dir, ...]}}."""
    session = session or make_session()
    items = list(catalog.items())
    logger.info("dockerfile: querying DockerHub for %d tools", len(items))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(lambda kv: _dockerfile_tool(kv[0], kv[1], session, dh_base), items))


def _merge_dockerfile(existing, extra):
    """Append DockerHub versions to a bioconda tool, filling blank metadata."""
    existing.versions.extend(extra.versions)
    for field in ("description", "home_url", "license"):
        if not getattr(existing, field) and getattr(extra, field):
            setattr(existing, field, getattr(extra, field))
    if not existing.identifiers and extra.identifiers:
        existing.identifiers = extra.identifiers


def run_build(
    out="data",
    recipes_dir=None,
    containers_dir=None,
    repodata_cache="/tmp/bioconda-repodata",
    subdirs=repodata_src.DEFAULT_SUBDIRS,
    limit=None,
    session=None,
    generated=None,
    index=None,
    recipes=None,
):
    session = session or make_session()
    generated = generated or date.today().isoformat()

    if index is None:
        index = repodata_src.build_index(session, repodata_cache, subdirs=subdirs)
    if recipes is None:
        recipes = bioconda.load_recipes(recipes_dir) if recipes_dir else {}
        logger.info("recipes: %d metadata entries", len(recipes))

    if limit:
        index = dict(itertools.islice(sorted(index.items()), limit))

    by_id = {t.id: t for t in build_bioconda_tools(index, recipes)}
    logger.info("bioconda: %d tools", len(by_id))

    if containers_dir:
        catalog = containers_src.load_containers(containers_dir)
        for t in build_dockerfile_tools(catalog, session=session):
            if t.id in by_id:
                _merge_dockerfile(by_id[t.id], t)
            else:
                by_id[t.id] = t
        logger.info("dockerfile: %d tools merged (total %d)", len(catalog), len(by_id))

    emit.write_catalog(list(by_id.values()), out, generated)
    logger.info("wrote catalog: %d tools -> %s", len(by_id), out)
