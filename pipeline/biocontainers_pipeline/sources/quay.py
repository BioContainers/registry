import re

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


def repo_detail(session, name, base="https://quay.io/api/v1"):
    """Fetch a repo's description and tag rows in a single call."""
    r = session.get(
        f"{base}/repository/{NAMESPACE}/{name}",
        params={"includeTags": "true", "includeStats": "false"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    tags = data.get("tags", {})
    rows = [(t.get("name", tag), 0, t.get("last_modified", "")) for tag, t in tags.items()]
    return {"description": data.get("description", "") or "", "tags": rows}


def repo_tags(session, name, base="https://quay.io/api/v1"):
    return repo_detail(session, name, base=base)["tags"]


def parse_repo_description(desc):
    """Extract summary/license/home from a quay biocontainers repo description.

    These descriptions embed recipe metadata, e.g.::

        # Coreutils
        > The gnu core utilities are the basic file ... utilities.
        > Licence: Gpl
        Home: https://depot.galaxyproject.org/software/coreutils/...
    """
    out = {"summary": "", "license": "", "home": ""}
    if not desc:
        return out
    summaries = []
    for raw in desc.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        body = line.lstrip("> ").strip()
        m = re.match(r"Licen[cs]e:\s*(.+)", body, re.I)
        if m:
            out["license"] = m.group(1).strip()
            continue
        m = re.match(r"Home:\s*(.+)", body, re.I)
        if m:
            out["home"] = m.group(1).strip()
            continue
        summaries.append(body)
    out["summary"] = " ".join(summaries).strip()
    return out
