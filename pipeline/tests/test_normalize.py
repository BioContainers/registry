from biocontainers_pipeline.normalize import version_key, _datestamp_parts


def test_version_key_orders_semantically():
    versions = ["0.1.19", "1.23.1", "1.18", "1.9", "2.1.5-7-deb"]
    ordered = sorted(versions, key=version_key, reverse=True)
    assert ordered[0] == "2.1.5-7-deb"
    assert ordered[1] == "1.23.1"
    # crucially, an often-rebuilt old version does NOT sort to the top
    assert ordered.index("1.23.1") < ordered.index("0.1.19")


def test_version_key_orders_datestamped_versions_by_date():
    # rsat-style: YYYYMMDD stamps must interleave with dashed dates, newest first (issue #83).
    versions = ["20240828", "20240507", "20230828", "2025-03-26"]
    ordered = sorted(versions, key=version_key, reverse=True)
    assert ordered == ["2025-03-26", "20240828", "20240507", "20230828"]


def test_datestamp_only_matches_plausible_dates():
    assert _datestamp_parts("20240828") == (2024, 8, 28)
    assert _datestamp_parts("99999999") is None   # not a real date -> left as a plain number
    assert _datestamp_parts("1234") is None        # wrong length
