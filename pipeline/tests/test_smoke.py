import json
import os

import pytest

from biocontainers_pipeline import build


@pytest.mark.network
@pytest.mark.skipif(not os.environ.get("RUN_NETWORK_TESTS"), reason="network")
def test_small_live_build(tmp_path):
    build.run_build(out=str(tmp_path), limit=5, only="quay")
    idx = json.loads((tmp_path / "search-index.json").read_text())
    assert len(idx) >= 1
    first = idx[0]
    detail = json.loads((tmp_path / "tools" / f"{first['id']}.json").read_text())
    assert detail["versions"]
