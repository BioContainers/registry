"""Read the BioContainers/containers git repo (Dockerfile-based images).

Layout: <tool>/<version>/Dockerfile. The published DockerHub tag is derived from the
Dockerfile LABELs as `<version>_cv<LABEL version>` (the `version` LABEL is the container
revision). The tool image is `biocontainers/<tool>:<tag>`. Metadata (summary/home/
license/bio.tools) also comes from the LABELs.
"""

import os
import re

# LABEL key="value" pairs, tolerating multiline "\ " continuations.
_LABEL_RE = re.compile(r'([a-zA-Z0-9_.]+)\s*=\s*"([^"]*)"')


def parse_dockerfile_labels(text: str) -> dict:
    labels = {}
    for m in _LABEL_RE.finditer(text):
        labels.setdefault(m.group(1), m.group(2))
    return {
        "summary": labels.get("about.summary", "").strip(),
        "home": labels.get("about.home", "").strip(),
        "license": labels.get("about.license", "").strip(),
        "software": labels.get("software", "").strip(),
        "biotools": labels.get("extra.identifiers.biotools", "").strip(),
        "cv": labels.get("version", "").strip(),  # container revision -> _cv<n>
    }


def container_tag(version_dir: str, cv: str) -> str:
    return f"{version_dir}_cv{cv}" if cv else version_dir


def load_containers(containers_dir: str) -> dict:
    """Map tool -> {"metadata": {...}, "versions": [{"version", "tag"}, ...]}."""
    out = {}
    for tool in sorted(os.listdir(containers_dir)):
        tool_path = os.path.join(containers_dir, tool)
        if not os.path.isdir(tool_path) or tool.startswith("."):
            continue
        versions = []
        metadata = {"summary": "", "home": "", "license": "", "biotools": ""}
        for version in sorted(os.listdir(tool_path)):
            dockerfile = os.path.join(tool_path, version, "Dockerfile")
            if not os.path.isfile(dockerfile):
                continue
            with open(dockerfile, encoding="utf-8", errors="replace") as fh:
                labels = parse_dockerfile_labels(fh.read())
            versions.append({"version": version, "tag": container_tag(version, labels["cv"])})
            for key in metadata:
                if labels.get(key) and not metadata[key]:
                    metadata[key] = labels[key]
        if versions:
            out[tool] = {"metadata": metadata, "versions": versions}
    return out
