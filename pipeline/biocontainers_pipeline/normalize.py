"""Version ordering. Container references are reconstructed in the frontend, so the
pipeline only needs to order versions sensibly."""

import re

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
