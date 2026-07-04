from biocontainers_pipeline.normalize import (
    dockerhub_container,
    quay_containers,
    sort_rows_desc,
    version_of,
)


def test_group_versions_dedupes_identical_conda():
    from biocontainers_pipeline.normalize import group_versions, quay_containers

    # Two build tags of the same version 1.19.
    rows = [
        ("1.19--h50ea8bc_0", 0, ""),
        ("1.19--py_0", 0, ""),
    ]
    versions = group_versions(rows, lambda tag, p, lm: quay_containers("samtools", tag, p, lm))
    assert len(versions) == 1
    types = [c.type for c in versions[0].containers]
    # 2 distinct docker + 2 distinct singularity, but conda collapses to 1.
    assert types.count("conda") == 1
    assert types.count("docker") == 2
    assert types.count("singularity") == 2


def test_sort_rows_desc_newest_first():
    rows = [
        ("1.0--0", 0, "Tue, 16 Dec 2025 21:28:43 -0000"),
        ("2.0--0", 0, "Wed, 18 Mar 2026 19:56:37 -0000"),
        ("bad", 0, ""),
    ]
    ordered = [r[0] for r in sort_rows_desc(rows)]
    assert ordered == ["2.0--0", "1.0--0", "bad"]


def test_version_of_strips_build_suffix():
    assert version_of("1.23--h96c455f_0") == "1.23"
    assert version_of("0.1.19--h9dcdb79_15") == "0.1.19"
    assert version_of("latest") == "latest"


def test_quay_containers_constructs_three():
    cs = quay_containers("samtools", "1.19--h50ea8bc_0", pulls=10, last_modified="")
    kinds = {c.type: c for c in cs}
    assert kinds["docker"].image == "quay.io/biocontainers/samtools:1.19--h50ea8bc_0"
    assert kinds["singularity"].url == "https://depot.galaxyproject.org/singularity/samtools:1.19--h50ea8bc_0"
    assert kinds["conda"].command == "conda install -c bioconda samtools=1.19"


def test_dockerhub_container_uses_biocontainers_namespace():
    c = dockerhub_container("blast", "2.2.31", pulls=3, last_modified="")
    assert c.image == "biocontainers/blast:2.2.31"
    assert c.type == "docker"
