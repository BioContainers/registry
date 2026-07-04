"""Read metadata from bioconda-recipes meta.yaml files (git clone).

meta.yaml uses Jinja templating, most commonly `{% set version = "1.2.3" %}` with
`version: {{ version }}`. We resolve simple `{% set %}` variables, then read the
`about:` block and package version.
"""

import os
import re

import yaml

_SET_RE = re.compile(r"""{%\s*set\s+(\w+)\s*=\s*["']([^"']*)["']\s*%}""")


def _resolve_jinja(text: str) -> str:
    """Resolve `{% set k = "v" %}` variables and substitute `{{ k }}`; blank out
    any remaining Jinja so the result is parseable YAML."""
    variables = dict(_SET_RE.findall(text))
    # drop set/control lines
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("{%")]
    out = "\n".join(lines)

    def sub(m):
        expr = m.group(1).strip()
        return variables.get(expr, "")

    out = re.sub(r"{{\s*([^}|]+?)\s*}}", sub, out)
    # any leftover complex jinja ({{ x|filter }}, {{ func() }}) -> blank
    out = re.sub(r"{{.*?}}", "", out)
    return out


def parse_meta(text: str) -> dict:
    result = {"home": "", "license": "", "summary": "", "version": ""}
    try:
        doc = yaml.safe_load(_resolve_jinja(text)) or {}
    except yaml.YAMLError:
        return result
    if not isinstance(doc, dict):
        return result
    about = doc.get("about", {}) or {}
    if not isinstance(about, dict):
        about = {}
    result["home"] = str(about.get("home", "") or "")
    result["license"] = str(about.get("license", "") or "")
    result["summary"] = str(about.get("summary", "") or "").strip()
    package = doc.get("package", {}) or {}
    if isinstance(package, dict):
        result["version"] = str(package.get("version", "") or "").strip()
    return result


def load_recipes(recipes_dir: str) -> dict:
    """Map package name -> parsed metadata for every recipes/<name>/meta.yaml."""
    out = {}
    for name in os.listdir(recipes_dir):
        meta = os.path.join(recipes_dir, name, "meta.yaml")
        if os.path.isfile(meta):
            with open(meta, encoding="utf-8", errors="replace") as fh:
                out[name] = parse_meta(fh.read())
    return out
