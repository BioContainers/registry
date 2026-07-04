"""Bioconda channel repodata — the authoritative index of built packages.

Each package file (`<name>-<version>-<build>.tar.bz2`) becomes a biocontainers
container tagged `<version>--<build>` on quay.io/biocontainers and the Galaxy
Singularity depot. We keep the newest build per (name, version).
"""

import bz2
import itertools
import json
import logging
import os

REPODATA_URL = "https://conda.anaconda.org/bioconda/{subdir}/repodata.json.bz2"
DEFAULT_SUBDIRS = ("noarch", "linux-64")

logger = logging.getLogger(__name__)


def fetch(subdir, cache_dir, session):
    """Download a subdir's repodata.json.bz2 into cache_dir (once). Returns the path."""
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"{subdir}.repodata.json.bz2")
    if os.path.isfile(path) and os.path.getsize(path) > 0:
        logger.info("repodata: using cached %s", path)
        return path
    url = REPODATA_URL.format(subdir=subdir)
    logger.info("repodata: downloading %s", url)
    r = session.get(url, timeout=180)
    r.raise_for_status()
    with open(path, "wb") as fh:
        fh.write(r.content)
    return path


def iter_records(path):
    """Yield every package record from a repodata bz2 file (both formats)."""
    with bz2.open(path, "rb") as fh:
        data = json.load(fh)
    for rec in itertools.chain(
        data.get("packages", {}).values(), data.get("packages.conda", {}).values()
    ):
        yield rec


def merge_records(index, records):
    """Fold records into index = {name: {version: best_build_dict}} keeping the
    newest build per (name, version) by (build_number, timestamp)."""
    for rec in records:
        name = rec.get("name")
        version = rec.get("version")
        if not name or not version:
            continue
        build = rec.get("build", "")
        bn = rec.get("build_number", 0) or 0
        ts = rec.get("timestamp", 0) or 0
        slot = index.setdefault(name, {})
        cur = slot.get(version)
        if cur is None or (bn, ts) > (cur["build_number"], cur["timestamp"]):
            slot[version] = {
                "version": version,
                "build": build,
                "build_number": bn,
                "timestamp": ts,
                "license": rec.get("license", "") or "",
            }
    return index


def build_index(session, cache_dir, subdirs=DEFAULT_SUBDIRS):
    """Return {name: {version: {build, build_number, timestamp, license}}}."""
    index = {}
    for subdir in subdirs:
        path = fetch(subdir, cache_dir, session)
        merge_records(index, iter_records(path))
    logger.info("repodata: %d packages indexed", len(index))
    return index
