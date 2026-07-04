"""DockerHub tags for the BioContainers/containers (Dockerfile) family.

The git repo tells us which Dockerfile tools exist and their metadata; DockerHub
is authoritative for the actual image tags (which vary: `1.8.1_cv2`, `v1.9.0_cv4`,
plain `1.9.0`, …) and the pull count.
"""

import logging
import re

NAMESPACE = "biocontainers"
_CV_RE = re.compile(r"_cv\d+$", re.I)

logger = logging.getLogger(__name__)


def software_version(tag):
    """Software version from a DockerHub tag: strip a leading 'v' and a `_cv<n>` suffix.
    'v1.9.0_cv4' -> '1.9.0'; '1.8.1_cv2' -> '1.8.1'; '1.9.0' -> '1.9.0'."""
    t = _CV_RE.sub("", tag)
    if re.match(r"v\d", t):
        t = t[1:]
    return t


def repo_tags(session, tool, base="https://hub.docker.com/v2"):
    """Return [(tag, last_updated), ...] for biocontainers/<tool>, or [] if absent."""
    url = f"{base}/repositories/{NAMESPACE}/{tool}/tags/"
    params = {"page_size": 100}
    out = []
    while url:
        r = session.get(url, params=params, timeout=60)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        data = r.json()
        out.extend((t["name"], t.get("last_updated", "")) for t in data.get("results", []))
        url, params = data.get("next"), None
    return out


def pull_counts(session, base="https://hub.docker.com/v2"):
    """All biocontainers pull counts in one paginated sweep: {name: pull_count}.
    Much cheaper than a per-tool call (~a dozen requests vs ~900)."""
    url = f"{base}/repositories/{NAMESPACE}/"
    params = {"page_size": 100}
    out = {}
    while url:
        r = session.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        for x in data.get("results", []):
            out[x["name"]] = x.get("pull_count", 0) or 0
        url, params = data.get("next"), None
    return out
