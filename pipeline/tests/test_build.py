import json

from biocontainers_pipeline import build


def _index():
    return {
        "samtools": {
            "1.19": {"version": "1.19", "build": "h50ea8bc_0", "build_number": 0, "timestamp": 200, "license": "MIT", "depends": ["htslib >=1.9", "libgcc", "_openmp_mutex"]},
            "1.18": {"version": "1.18", "build": "h50ea8bc_1", "build_number": 1, "timestamp": 100, "license": "MIT", "depends": []},
        }
    }


def test_build_bioconda_tools_orders_versions_newest_first():
    recipes = {"samtools": {
        "home": "http://htslib.org", "license": "MIT", "summary": "SAM tools", "version": "1.19",
        "doc_url": "http://docs", "dev_url": "http://src", "license_family": "MIT",
        "identifiers": ["biotools:samtools"], "maintainers": ["alice"], "description": "long",
    }}
    tools = build.build_bioconda_tools(_index(), recipes)
    t = tools[0]
    assert t.id == "samtools"
    assert t.home_url == "http://htslib.org"
    assert [v.version for v in t.versions] == ["1.19", "1.18"]  # semantic version desc
    assert t.registries() == ["conda", "quay.io", "singularity"]
    assert t.versions[0].build == "h50ea8bc_0"
    assert t.doc_url == "http://docs" and t.dev_url == "http://src"
    assert t.identifiers == ["biotools:samtools"] and t.maintainers == ["alice"]
    assert t.long_description == "long" and t.license_family == "MIT"
    # latest-version deps, with lib*/compiler internals filtered out
    assert t.dependencies == ["htslib >=1.9"]


def test_build_bioconda_license_falls_back_to_repodata():
    tools = build.build_bioconda_tools(_index(), recipes={})
    assert tools[0].license == "MIT"  # from repodata record


def test_build_dockerfile_tools_uses_git_derived_tags():
    catalog = {"diann": {
        "metadata": {"summary": "DIA-NN", "home": "h", "license": "CC", "biotools": "diann"},
        "versions": [
            {"version": "1.8.0", "tag": "1.8.0_cv1"},
            {"version": "1.8.1", "tag": "1.8.1_cv2"},
        ],
    }}
    tools = build.build_dockerfile_tools(catalog)
    t = tools[0]
    assert t.id == "diann"
    assert t.identifiers == ["biotools:diann"]
    # semantic version desc
    assert [v.version for v in t.versions] == ["1.8.1", "1.8.0"]
    assert t.versions[0].docker == "biocontainers/diann:1.8.1_cv2"


def test_run_build_merges_and_writes(tmp_path):
    index = _index()
    recipes = {"samtools": {"summary": "SAM tools", "home": "h", "license": "MIT", "version": "1.19"}}
    build.run_build(out=str(tmp_path), index=index, recipes=recipes, generated="2026-07-04")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert idx[0]["id"] == "samtools"
    detail = json.loads((tmp_path / "tools" / "samtools.json").read_text())
    assert len(detail["versions"]) == 2
