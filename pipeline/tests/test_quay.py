import requests
import responses

from biocontainers_pipeline.sources import quay


@responses.activate
def test_list_repos_follows_pagination():
    base = "https://quay.io/api/v1"
    responses.get(base + "/repository", json={"repositories": [{"name": "a"}], "next_page": "TOK"})
    responses.get(base + "/repository", json={"repositories": [{"name": "b"}]})
    names = quay.list_repos(requests.Session(), base=base)
    assert names == ["a", "b"]


@responses.activate
def test_repo_tags_returns_rows():
    base = "https://quay.io/api/v1"
    responses.get(
        base + "/repository/biocontainers/samtools",
        json={"tags": {"1.19--h50ea8bc_0": {"name": "1.19--h50ea8bc_0", "last_modified": "Tue, 16 Dec 2025 21:28:43 -0000"}}},
    )
    rows = quay.repo_tags(requests.Session(), "samtools", base=base)
    assert rows[0][0] == "1.19--h50ea8bc_0"
