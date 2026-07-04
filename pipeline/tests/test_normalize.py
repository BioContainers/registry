from biocontainers_pipeline.normalize import (
    bioconda_containers,
    container_tag,
    dockerfile_container,
    version_key,
)


def test_version_key_orders_semantically():
    versions = ["0.1.19", "1.23.1", "1.18", "1.9", "2.1.5-7-deb"]
    ordered = sorted(versions, key=version_key, reverse=True)
    assert ordered[0] == "2.1.5-7-deb"
    assert ordered[1] == "1.23.1"
    # crucially, an often-rebuilt old version does NOT sort to the top
    assert ordered.index("1.23.1") < ordered.index("0.1.19")


def test_container_tag():
    assert container_tag("1.19", "h50ea8bc_0") == "1.19--h50ea8bc_0"
    assert container_tag("1.19", "") == "1.19"


def test_bioconda_containers_three_kinds():
    cs = bioconda_containers("samtools", "1.19", "h50ea8bc_0")
    by = {c.type: c for c in cs}
    assert by["docker"].image == "quay.io/biocontainers/samtools:1.19--h50ea8bc_0"
    assert by["singularity"].url == "https://depot.galaxyproject.org/singularity/samtools:1.19--h50ea8bc_0"
    assert by["conda"].command == "conda install -c bioconda samtools=1.19"


def test_dockerfile_container_dockerhub_namespace():
    c = dockerfile_container("abyss", "2.1.5-7-deb")
    assert c.type == "docker"
    assert c.image == "biocontainers/abyss:2.1.5-7-deb"
