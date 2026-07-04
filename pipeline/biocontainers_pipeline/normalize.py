"""Construct container references from package coordinates (no network calls)."""

import re

from biocontainers_pipeline.models import Container

_CHUNK_RE = re.compile(r"\d+|\D+")


def version_key(version):
    """A sort key for mixed version strings so 1.23.1 > 1.18 > 0.1.19.

    Splits on separators, then into digit/non-digit runs; digits compare
    numerically and rank above alpha runs. Robust to odd tags like '2.1.5-7-deb'.
    """
    key = []
    for part in re.split(r"[._\-+]", str(version)):
        for m in _CHUNK_RE.finditer(part):
            s = m.group()
            key.append((1, int(s)) if s.isdigit() else (0, s))
    return key


def container_tag(version, build):
    """Biocontainers image tag: `<version>--<build>` (or just version if no build)."""
    return f"{version}--{build}" if build else version


def bioconda_containers(name, version, build):
    """The three ways to get a bioconda package: quay docker, Galaxy singularity, conda."""
    tag = container_tag(version, build)
    return [
        Container(type="docker", image=f"quay.io/biocontainers/{name}:{tag}"),
        Container(
            type="singularity",
            url=f"https://depot.galaxyproject.org/singularity/{name}:{tag}",
        ),
        Container(type="conda", command=f"conda install -c bioconda {name}={version}"),
    ]


def dockerfile_container(tool, version_dir):
    """A BioContainers/containers Dockerfile image on DockerHub."""
    return Container(type="docker", image=f"biocontainers/{tool}:{version_dir}")
