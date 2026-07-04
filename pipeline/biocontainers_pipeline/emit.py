import json
import os
from collections import Counter
from math import floor, log10


def round_sig(n, sig=2):
    if not n:
        return 0
    d = sig - int(floor(log10(abs(n)))) - 1
    return int(round(n, d))


def _identifier(identifiers, prefix):
    for i in identifiers or []:
        if i.startswith(prefix + ":"):
            return i[len(prefix) + 1:]
    return ""


def search_record(t):
    """Lightweight record for the in-browser index (loaded once for all tools)."""
    rec = {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "license": t.license,
        "registries": t.registries(),
        "latest_version": t.latest_version(),
        "versionCount": len(t.versions),
    }
    # Compact badges for search cards, only when present.
    biotools = _identifier(t.identifiers, "biotools")
    doi = _identifier(t.identifiers, "doi")
    if biotools:
        rec["biotools"] = biotools
    if doi:
        rec["doi"] = doi
    return rec


def _version_out(v):
    d = {"version": v.version}
    if v.last_updated:
        d["last_updated"] = v.last_updated
    if v.build is not None:
        d["build"] = v.build       # bioconda: frontend builds quay/singularity/conda
    if v.docker:
        d["docker"] = v.docker     # Dockerfile image
    return d


def tool_detail(t):
    d = {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "home_url": t.home_url,
        "license": t.license,
        "versions": [_version_out(v) for v in t.versions],
    }
    # Optional enrichment — emitted only when present, to keep files small.
    for key, value in (
        ("long_description", t.long_description),
        ("doc_url", t.doc_url),
        ("dev_url", t.dev_url),
        ("license_family", t.license_family),
        ("identifiers", t.identifiers),
        ("maintainers", t.maintainers),
        ("dependencies", t.dependencies),
    ):
        if value:
            d[key] = value
    if t.total_pulls:
        d["total_pulls"] = round_sig(t.total_pulls)
    return d


def facets(tools):
    lic, reg = Counter(), Counter()
    for t in tools:
        lic[t.license or "Not available"] += 1
        for r in t.registries():
            reg[r] += 1

    def block(name, c):
        return {"facet": name, "values": [{"value": k, "count": v} for k, v in c.most_common()]}

    return [block("license", lic), block("registry", reg)]


def stats(tools, generated):
    reg = Counter()
    for t in tools:
        for r in t.registries():
            reg[r] += 1
    return {
        "tools": len(tools),
        "versions": sum(len(t.versions) for t in tools),
        "containers": sum(t.container_count() for t in tools),
        "registries": dict(reg),
        "generated": generated,
    }


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
