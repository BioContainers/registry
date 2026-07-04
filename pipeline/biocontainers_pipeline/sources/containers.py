"""Read the BioContainers/containers git repo (Dockerfile-based images).

Layout: <tool>/<version>/Dockerfile. Each Dockerfile carries LABELs such as
about.summary, about.home, about.license, software.version. The DockerHub image
for a version dir is `biocontainers/<tool>:<version-dir>`.
"""

import os
import re

# LABEL key="value" pairs, tolerating multiline "\ " continuations.
_LABEL_RE = re.compile(r'([a-zA-Z0-9_.]+)\s*=\s*"([^"]*)"')


def parse_dockerfile_labels(text: str) -> dict:
    labels = {}
    for m in _LABEL_RE.finditer(text):
        labels[m.group(1)] = m.group(2)
    return {
        "summary": labels.get("about.summary", "").strip(),
        "home": labels.get("about.home", "").strip(),
        "license": labels.get("about.license", "").strip(),
        "software": labels.get("software", "").strip(),
    }


def load_containers(containers_dir: str) -> dict:
    """Map tool -> {"metadata": {...}, "versions": [version_dir, ...]}.

    Metadata is taken from the newest version's Dockerfile (last dir alphabetically
    as a cheap heuristic; refined by callers if needed).
    """
    out = {}
    for tool in sorted(os.listdir(containers_dir)):
        tool_path = os.path.join(containers_dir, tool)
        if not os.path.isdir(tool_path) or tool.startswith("."):
            continue
        versions = []
        metadata = {"summary": "", "home": "", "license": "", "software": ""}
        for version in sorted(os.listdir(tool_path)):
            dockerfile = os.path.join(tool_path, version, "Dockerfile")
            if not os.path.isfile(dockerfile):
                continue
            versions.append(version)
            with open(dockerfile, encoding="utf-8", errors="replace") as fh:
                labels = parse_dockerfile_labels(fh.read())
            # keep the richest metadata seen
            for key in metadata:
                if labels.get(key) and not metadata[key]:
                    metadata[key] = labels[key]
        if versions:
            out[tool] = {"metadata": metadata, "versions": versions}
    return out
