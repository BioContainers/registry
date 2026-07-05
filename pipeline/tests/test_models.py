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


def test_latest_version_is_honest_newest_but_primary_is_bioconda():
    # A legacy Docker version may sort on top by number; latest_version stays honest
    # (newest overall), while primary_source reports Bioconda as the recommended source.
    t = Tool(id="x", name="x", versions=[
        Version(version="2.0", docker="biocontainers/x:v2.0_cv1"),  # legacy, highest number
        Version(version="1.9", build="h0"),                         # bioconda
    ])
    assert t.latest_version() == "2.0"
    assert t.primary_source() == "bioconda"


def test_primary_source_dockerhub_when_no_bioconda():
    t = Tool(id="x", name="x", versions=[Version(version="deb", docker="biocontainers/x:deb")])
    assert t.primary_source() == "dockerhub"
    assert t.latest_version() == "deb"
