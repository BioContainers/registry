from click.testing import CliRunner

from biocontainers_pipeline.cli import cli


def test_cli_build_help():
    result = CliRunner().invoke(cli, ["build", "--help"])
    assert result.exit_code == 0
    assert "--out" in result.output
    assert "--limit" in result.output
