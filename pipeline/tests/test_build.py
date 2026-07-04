import json

import requests
import responses

from biocontainers_pipeline import build


@responses.activate
def test_build_quay_tools_joins_metadata():
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories": [{"name": "samtools"}]})
    responses.get(
        base + "/repository/biocontainers/samtools",
        json={"tags": {"1.19--h50ea8bc_0": {"name": "1.19--h50ea8bc_0", "last_modified": "d"}}},
    )
    recipes = {"samtools": {"home": "http://htslib.org", "license": "MIT", "summary": "SAM tools"}}
    tools = build.build_quay_tools(requests.Session(), recipes, quay_base=base)
    assert tools[0].id == "samtools"
    assert tools[0].license == "MIT"
    assert tools[0].versions[0].version == "1.19"
    assert tools[0].registries() == ["conda", "quay.io", "singularity"]


@responses.activate
def test_run_build_writes_catalog(tmp_path):
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories": [{"name": "samtools"}]})
    responses.get(
        base + "/repository/biocontainers/samtools",
        json={"tags": {"1.19--0": {"name": "1.19--0", "last_modified": "d"}}},
    )
    build.run_build(
        out=str(tmp_path), only="quay", recipes=None,
        session=requests.Session(), quay_base=base, generated="2026-07-04",
    )
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
