from biocontainers_pipeline.sources import containers

DOCKERFILE = '''FROM biocontainers/biocontainers:vdebian
LABEL    software="abyss" \\
    about.summary="de novo sequence assembler" \\
    about.home="http://www.bcgsc.ca/abyss" \\
    software.version="2.1.5-7-deb" \\
    about.license="GPL-3+"
USER root
'''


def test_parse_dockerfile_labels():
    m = containers.parse_dockerfile_labels(DOCKERFILE)
    assert m["software"] == "abyss"
    assert m["summary"] == "de novo sequence assembler"
    assert m["home"] == "http://www.bcgsc.ca/abyss"
    assert m["license"] == "GPL-3+"


def test_load_containers_walks_tool_version_dirs(tmp_path):
    tool = tmp_path / "abyss"
    for ver in ("1.9.0", "2.1.5-7-deb"):
        d = tool / ver
        d.mkdir(parents=True)
        (d / "Dockerfile").write_text(DOCKERFILE)
    (tmp_path / "README.md").write_text("not a tool")
    catalog = containers.load_containers(str(tmp_path))
    assert set(catalog.keys()) == {"abyss"}
    assert catalog["abyss"]["versions"] == ["1.9.0", "2.1.5-7-deb"]
    assert catalog["abyss"]["metadata"]["summary"] == "de novo sequence assembler"
