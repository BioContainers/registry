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
    r = session.get(
        f"{base}/repositories/{NAMESPACE}/{name}/tags/",
        params={"page_size": 100},
        timeout=60,
    )
    r.raise_for_status()
    return [(t["name"], 0, t.get("last_updated", "")) for t in r.json().get("results", [])]
