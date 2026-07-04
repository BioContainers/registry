from biocontainers_pipeline.models import Container, Tool, Version


def test_registries_derived_from_containers():
    t = Tool(
        id="x", name="x", description="", home_url="", license="MIT",
        toolclass="CommandLineTool", total_pulls=0,
        versions=[
            Version(version="1.0", last_updated="", containers=[
                Container(type="docker", image="quay.io/biocontainers/x:1.0--0", url=None, command=None, pulls=5),
                Container(type="conda", image=None, url=None, command="conda install -c bioconda x=1.0", pulls=0),
            ])
        ],
    )
    assert t.registries() == ["conda", "quay.io"]
