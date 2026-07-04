from biocontainers_pipeline.sources import containers

DOCKERFILE = '''FROM biocontainers/biocontainers:vdebian
LABEL    software="abyss" \\
    about.summary="de novo sequence assembler" \\
    about.home="http://www.bcgsc.ca/abyss" \\
    software.version="2.1.5-7-deb" \\
    version="1" \\
    extra.identifiers.biotools="abyss" \\
    about.license="GPL-3+"
USER root
'''


def test_parse_dockerfile_labels():
    m = containers.parse_dockerfile_labels(DOCKERFILE)
    assert m["software"] == "abyss"
    assert m["summary"] == "de novo sequence assembler"
    assert m["home"] == "http://www.bcgsc.ca/abyss"
    assert m["license"] == "GPL-3+"
    assert m["biotools"] == "abyss"
    assert m["cv"] == "1"


def test_container_tag():
    assert containers.container_tag("1.8.1", "2") == "1.8.1_cv2"
    assert containers.container_tag("1.9.0", "") == "1.9.0"


def test_load_containers_builds_tags_from_labels(tmp_path):
    tool = tmp_path / "abyss"
    for ver in ("1.9.0", "2.1.5-7-deb"):
        d = tool / ver
        d.mkdir(parents=True)
        (d / "Dockerfile").write_text(DOCKERFILE)
    (tmp_path / "README.md").write_text("not a tool")
    catalog = containers.load_containers(str(tmp_path))
    assert set(catalog.keys()) == {"abyss"}
    versions = {v["version"]: v["tag"] for v in catalog["abyss"]["versions"]}
    assert versions == {"1.9.0": "1.9.0_cv1", "2.1.5-7-deb": "2.1.5-7-deb_cv1"}
    assert catalog["abyss"]["metadata"]["summary"] == "de novo sequence assembler"
    assert catalog["abyss"]["metadata"]["biotools"] == "abyss"
