import json
import os
from collections import Counter
from dataclasses import asdict
from math import floor, log10


def round_sig(n, sig=2):
    if not n:
        return 0
    d = sig - int(floor(log10(abs(n)))) - 1
    return int(round(n, d))


def search_record(t):
    return {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "license": t.license,
        "toolclass": t.toolclass,
        "registries": t.registries(),
        "latest_version": t.latest_version(),
        "versionCount": len(t.versions),
        "total_pulls": round_sig(t.total_pulls),
    }


def tool_detail(t):
    d = {
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "home_url": t.home_url,
        "license": t.license,
        "toolclass": t.toolclass,
        "total_pulls": round_sig(t.total_pulls),
        "versions": [],
    }
    for v in t.versions:
        containers = []
        for c in v.containers:
            entry = {k: val for k, val in asdict(c).items() if val not in (None, 0, "")}
            entry["type"] = c.type
            containers.append(entry)
        d["versions"].append(
            {"version": v.version, "last_updated": v.last_updated, "containers": containers}
        )
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
    return {
        "tools": len(tools),
        "versions": sum(len(t.versions) for t in tools),
        "containers": sum(len(v.containers) for t in tools for v in t.versions),
        "total_pulls": round_sig(sum(t.total_pulls for t in tools)),
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
