import bz2
import json

from biocontainers_pipeline.sources import repodata


def test_merge_records_keeps_newest_build():
    index = {}
    records = [
        {"name": "s", "version": "1.0", "build": "h0", "build_number": 0, "timestamp": 100},
        {"name": "s", "version": "1.0", "build": "h1", "build_number": 1, "timestamp": 200},
        {"name": "s", "version": "0.9", "build": "hx", "build_number": 5, "timestamp": 50},
    ]
    repodata.merge_records(index, records)
    assert set(index["s"].keys()) == {"1.0", "0.9"}
    assert index["s"]["1.0"]["build"] == "h1"  # newest build_number/timestamp wins


def test_merge_records_skips_incomplete():
    index = {}
    repodata.merge_records(index, [{"name": "", "version": "1"}, {"version": "1"}])
    assert index == {}


def test_iter_records_reads_both_sections(tmp_path):
    path = tmp_path / "linux-64.repodata.json.bz2"
    payload = {
        "packages": {"a-1.0-h0.tar.bz2": {"name": "a", "version": "1.0", "build": "h0"}},
        "packages.conda": {"b-2.0-h1.conda": {"name": "b", "version": "2.0", "build": "h1"}},
    }
    with bz2.open(path, "wt") as fh:
        json.dump(payload, fh)
    names = sorted(r["name"] for r in repodata.iter_records(str(path)))
    assert names == ["a", "b"]
