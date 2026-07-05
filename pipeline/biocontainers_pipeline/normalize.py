"""Version ordering. Container references are reconstructed in the frontend, so the
pipeline only needs to order versions sensibly."""

import re

_CHUNK_RE = re.compile(r"\d+|\D+")


def _datestamp_parts(s):
    """If `s` is an 8-digit YYYYMMDD date stamp, return (year, month, day); else None.

    Lets date-versioned tools (e.g. rsat: 20240828) sort by real date and interleave
    correctly with dashed dates like 2025-03-26, without affecting normal semver."""
    if len(s) != 8:
        return None
    y, mo, d = int(s[:4]), int(s[4:6]), int(s[6:8])
    if 1990 <= y <= 2099 and 1 <= mo <= 12 and 1 <= d <= 31:
        return (y, mo, d)
    return None


def version_key(version):
    """A sort key for mixed version strings so 1.23.1 > 1.18 > 0.1.19.

    Splits on separators, then into digit/non-digit runs; digits compare
    numerically and rank above alpha runs. Robust to odd tags like '2.1.5-7-deb'.
    An 8-digit YYYYMMDD run is expanded into year/month/day so date-based versions
    (e.g. 20240828 vs 2025-03-26) order by actual date.
    """
    key = []
    for part in re.split(r"[._\-+]", str(version)):
        for m in _CHUNK_RE.finditer(part):
            s = m.group()
            if s.isdigit():
                date = _datestamp_parts(s)
                if date:
                    key.extend((1, n) for n in date)
                else:
                    key.append((1, int(s)))
            else:
                key.append((0, s))
    return key
