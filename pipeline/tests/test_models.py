from biocontainers_pipeline.models import Tool, Version


def test_registries_and_counts():
    t = Tool(
        id="x", name="x", license="MIT",
        versions=[
            Version(version="1.0", build="h0"),        # bioconda -> 3 containers
            Version(version="deb", docker="biocontainers/x:deb"),  # dockerfile -> 1
        ],
    )
    assert t.registries() == ["DockerHub", "conda", "quay.io", "singularity"]
    assert t.latest_version() == "1.0"
    assert t.container_count() == 4


def test_bioconda_empty_build_still_counts_as_bioconda():
    t = Tool(id="x", name="x", versions=[Version(version="1.0", build="")])
    assert t.registries() == ["conda", "quay.io", "singularity"]
    assert t.container_count() == 3
