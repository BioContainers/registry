import requests
import responses

from biocontainers_pipeline.sources import dockerhub


@responses.activate
def test_list_repos_paginates_and_keeps_pull_count():
    base = "https://hub.docker.com/v2"
    responses.get(
        base + "/repositories/biocontainers/",
        json={"results": [{"name": "blast", "pull_count": 42}], "next": base + "/repositories/biocontainers/?page=2"},
    )
    responses.get(
        base + "/repositories/biocontainers/",
        json={"results": [{"name": "fastqc", "pull_count": 7}], "next": None},
    )
    repos = dockerhub.list_repos(requests.Session(), base=base)
    assert repos == [("blast", 42), ("fastqc", 7)]
