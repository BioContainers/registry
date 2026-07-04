import os
import re

import yaml


def _strip_jinja(text: str) -> str:
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("{%")]
    return re.sub(r"{{.*?}}", "PLACEHOLDER", "\n".join(lines))


def parse_meta(text: str) -> dict:
    try:
        doc = yaml.safe_load(_strip_jinja(text)) or {}
    except yaml.YAMLError:
        return {"home": "", "license": "", "summary": ""}
    if not isinstance(doc, dict):
        return {"home": "", "license": "", "summary": ""}
    about = doc.get("about", {}) or {}
    if not isinstance(about, dict):
        about = {}
    return {
        "home": str(about.get("home", "") or ""),
        "license": str(about.get("license", "") or ""),
        "summary": str(about.get("summary", "") or "").strip(),
    }


def load_recipes(recipes_dir: str) -> dict:
    out = {}
    for name in os.listdir(recipes_dir):
        meta = os.path.join(recipes_dir, name, "meta.yaml")
        if os.path.isfile(meta):
            with open(meta, encoding="utf-8", errors="replace") as fh:
                out[name] = parse_meta(fh.read())
    return out
