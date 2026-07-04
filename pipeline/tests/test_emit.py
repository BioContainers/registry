import json

from biocontainers_pipeline import emit
from biocontainers_pipeline.models import Tool, Version


def _tool():
    return Tool(
        id="samtools", name="samtools", description="d", home_url="h", license="MIT",
        total_pulls=0,
        versions=[Version(version="1.19", last_updated="x", build="h50ea8bc_0")],
    )


def test_round_sig():
    assert emit.round_sig(1234567) == 1200000


def test_search_record_is_lean():
    r = emit.search_record(_tool())
    assert r["registries"] == ["conda", "quay.io", "singularity"]
    assert r["latest_version"] == "1.19"
    assert r["versionCount"] == 1
    assert "toolclass" not in r and "total_pulls" not in r


def test_version_output_is_minimal():
    d = emit.tool_detail(_tool())
    v = d["versions"][0]
    assert v == {"version": "1.19", "last_updated": "x", "build": "h50ea8bc_0"}
    assert "total_pulls" not in d  # omitted when zero


def test_write_catalog(tmp_path):
    emit.write_catalog([_tool()], str(tmp_path), generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
    stats = json.loads((tmp_path / "stats.json").read_text())
    assert stats["tools"] == 1 and stats["versions"] == 1 and stats["containers"] == 3
    facets = json.loads((tmp_path / "facets.json").read_text())
    names = {f["facet"] for f in facets}
    assert names == {"license", "registry"}  # no all-constant toolclass facet
