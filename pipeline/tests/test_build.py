import json

from biocontainers_pipeline import build


def _index():
    return {
        "samtools": {
            "1.19": {"version": "1.19", "build": "h50ea8bc_0", "build_number": 0, "timestamp": 200, "license": "MIT"},
            "1.18": {"version": "1.18", "build": "h50ea8bc_1", "build_number": 1, "timestamp": 100, "license": "MIT"},
        }
    }


def test_build_bioconda_tools_orders_versions_newest_first():
    recipes = {"samtools": {"home": "http://htslib.org", "license": "MIT", "summary": "SAM tools", "version": "1.19"}}
    tools = build.build_bioconda_tools(_index(), recipes)
    t = tools[0]
    assert t.id == "samtools"
    assert t.home_url == "http://htslib.org"
    assert [v.version for v in t.versions] == ["1.19", "1.18"]  # timestamp desc
    assert t.registries() == ["conda", "quay.io", "singularity"]
    assert t.versions[0].containers[0].image == "quay.io/biocontainers/samtools:1.19--h50ea8bc_0"


def test_build_bioconda_license_falls_back_to_repodata():
    tools = build.build_bioconda_tools(_index(), recipes={})
    assert tools[0].license == "MIT"  # from repodata record


def test_build_dockerfile_tools():
    catalog = {"abyss": {"metadata": {"summary": "assembler", "home": "h", "license": "GPL"}, "versions": ["1.9.0", "2.1.5"]}}
    tools = build.build_dockerfile_tools(catalog)
    t = tools[0]
    assert t.id == "abyss"
    assert t.description == "assembler"
    assert t.versions[0].containers[0].image == "biocontainers/abyss:2.1.5"  # reversed -> newest first


def test_run_build_merges_and_writes(tmp_path):
    index = _index()
    recipes = {"samtools": {"summary": "SAM tools", "home": "h", "license": "MIT", "version": "1.19"}}
    build.run_build(out=str(tmp_path), index=index, recipes=recipes, generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
    detail = json.loads((tmp_path / "tools" / "samtools.json").read_text())
    assert len(detail["versions"]) == 2
