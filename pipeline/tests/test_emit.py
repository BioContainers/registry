import json

from biocontainers_pipeline import emit
from biocontainers_pipeline.models import Container, Tool, Version


def _tool():
    return Tool(
        id="samtools", name="samtools", description="d", home_url="h", license="MIT",
        toolclass="CommandLineTool", total_pulls=1234567,
        versions=[
            Version(version="1.19", last_updated="x", containers=[
                Container(type="docker", image="quay.io/biocontainers/samtools:1.19--0", pulls=1010)
            ])
        ],
    )


def test_round_sig():
    assert emit.round_sig(1234567) == 1200000


def test_search_record_shape():
    r = emit.search_record(_tool())
    assert r["registries"] == ["quay.io"]
    assert r["latest_version"] == "1.19"
    assert r["versionCount"] == 1
    assert r["total_pulls"] == 1200000


def test_write_catalog(tmp_path):
    emit.write_catalog([_tool()], str(tmp_path), generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
    detail = json.loads((tmp_path / "tools" / "samtools.json").read_text())
    assert detail["versions"][0]["containers"][0]["image"].startswith("quay.io/")
    stats = json.loads((tmp_path / "stats.json").read_text())
    assert stats["tools"] == 1 and stats["versions"] == 1
    assert stats["containers"] == 1
    facets = json.loads((tmp_path / "facets.json").read_text())
    assert any(f["facet"] == "license" for f in facets)
