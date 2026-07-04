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
    r = session.get(
        f"{base}/repository/{NAMESPACE}/{name}",
        params={"includeTags": "true", "includeStats": "false"},
        timeout=60,
    )
    r.raise_for_status()
    tags = r.json().get("tags", {})
    return [(t.get("name", tag), 0, t.get("last_modified", "")) for tag, t in tags.items()]
