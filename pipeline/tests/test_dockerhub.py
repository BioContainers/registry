import requests
import responses

from biocontainers_pipeline.sources import dockerhub


def test_software_version_strips_prefix_and_cv():
    assert dockerhub.software_version("v1.9.0_cv4") == "1.9.0"
    assert dockerhub.software_version("1.8.1_cv2") == "1.8.1"
    assert dockerhub.software_version("1.9.0") == "1.9.0"
    assert dockerhub.software_version("2.1.5-7-deb_cv1") == "2.1.5-7-deb"


@responses.activate
def test_repo_tags_paginates():
    base = "https://hub.docker.com/v2"
    responses.get(
        base + "/repositories/biocontainers/diann/tags/",
        json={"results": [{"name": "1.8.1_cv2", "last_updated": "2022-01-02"}], "next": None},
    )
    rows = dockerhub.repo_tags(requests.Session(), "diann", base=base)
    assert rows == [("1.8.1_cv2", "2022-01-02")]


@responses.activate
def test_repo_tags_absent_is_empty():
    base = "https://hub.docker.com/v2"
    responses.get(base + "/repositories/biocontainers/nope/tags/", status=404)
    assert dockerhub.repo_tags(requests.Session(), "nope", base=base) == []
