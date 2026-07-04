from biocontainers_pipeline.normalize import version_key


def test_version_key_orders_semantically():
    versions = ["0.1.19", "1.23.1", "1.18", "1.9", "2.1.5-7-deb"]
    ordered = sorted(versions, key=version_key, reverse=True)
    assert ordered[0] == "2.1.5-7-deb"
    assert ordered[1] == "1.23.1"
    # crucially, an often-rebuilt old version does NOT sort to the top
    assert ordered.index("1.23.1") < ordered.index("0.1.19")
