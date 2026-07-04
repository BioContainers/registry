from collections import OrderedDict
from email.utils import parsedate_to_datetime

from biocontainers_pipeline.models import Container, Version


def sort_rows_desc(rows):
    """Sort (tag, pulls, last_modified) rows newest-first by last_modified.

    last_modified is an RFC 2822 date string (quay/dockerhub). Rows with an
    unparseable/empty date sort last, keeping a stable order among themselves.
    """
    def key(row):
        try:
            return parsedate_to_datetime(row[2]).timestamp()
        except (TypeError, ValueError):
            return float("-inf")

    return sorted(rows, key=key, reverse=True)


def version_of(tag: str) -> str:
    """Software version from a container tag: '1.23--h96c455f_0' -> '1.23'."""
    return tag.split("--", 1)[0]


def quay_containers(name, tag, pulls, last_modified):
    ver = version_of(tag)
    return [
        Container(type="docker", image=f"quay.io/biocontainers/{name}:{tag}", pulls=pulls),
        Container(type="singularity", url=f"https://depot.galaxyproject.org/singularity/{name}:{tag}"),
        Container(type="conda", command=f"conda install -c bioconda {name}={ver}"),
    ]


def dockerhub_container(name, tag, pulls, last_modified):
    return Container(type="docker", image=f"biocontainers/{name}:{tag}", pulls=pulls)


def group_versions(rows, builder):
    """Group (tag, pulls, last_modified) rows by software version.

    builder(tag, pulls, last_modified) -> list[Container]. Version order follows the
    caller's row order (callers sort newest-first). Containers that are identical within
    a version (e.g. the conda command, which is the same for every build tag) are
    collapsed to a single entry.
    """
    groups: "OrderedDict[str, Version]" = OrderedDict()
    seen: "dict[str, set]" = {}
    for tag, pulls, last_modified in rows:
        ver = version_of(tag)
        v = groups.get(ver)
        if v is None:
            v = Version(version=ver, last_updated=last_modified, containers=[])
            groups[ver] = v
            seen[ver] = set()
        for c in builder(tag, pulls, last_modified):
            key = (c.type, c.image, c.url, c.command)
            if key in seen[ver]:
                continue
            seen[ver].add(key)
            v.containers.append(c)
    return list(groups.values())
