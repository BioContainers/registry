import requests

from biocontainers_pipeline import emit
from biocontainers_pipeline.models import Tool
from biocontainers_pipeline.normalize import (
    dockerhub_container,
    group_versions,
    quay_containers,
    sort_rows_desc,
)
from biocontainers_pipeline.sources import dockerhub, quay


def _quay_builder(name):
    return lambda tag, pulls, lm: quay_containers(name, tag, pulls, lm)


def _dockerhub_builder(name):
    return lambda tag, pulls, lm: [dockerhub_container(name, tag, pulls, lm)]


def build_quay_tools(session, recipes, limit=None, quay_base="https://quay.io/api/v1"):
    recipes = recipes or {}
    tools = []
    for name in quay.list_repos(session, base=quay_base, limit=limit):
        rows = quay.repo_tags(session, name, base=quay_base)
        if not rows:
            continue
        versions = group_versions(sort_rows_desc(rows), _quay_builder(name))
        meta = recipes.get(name, {})
        tools.append(
            Tool(
                id=name,
                name=name,
                description=meta.get("summary", ""),
                home_url=meta.get("home", ""),
                license=meta.get("license", ""),
                toolclass="CommandLineTool",
                total_pulls=0,
                versions=versions,
            )
        )
    return tools


def build_dockerhub_tools(session, limit=None, dh_base="https://hub.docker.com/v2"):
    tools = []
    for name, pull_count in dockerhub.list_repos(session, base=dh_base, limit=limit):
        rows = dockerhub.repo_tags(session, name, base=dh_base)
        if not rows:
            continue
        versions = group_versions(sort_rows_desc(rows), _dockerhub_builder(name))
        tools.append(
            Tool(
                id=name,
                name=name,
                toolclass="CommandLineTool",
                total_pulls=pull_count,
                versions=versions,
            )
        )
    return tools


def run_build(
    out="data",
    limit=None,
    only=None,
    recipes=None,
    recipes_dir=None,
    session=None,
    quay_base="https://quay.io/api/v1",
    dh_base="https://hub.docker.com/v2",
    generated=None,
):
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
