import click


@click.group()
def cli():
    """BioContainers static data pipeline."""


@cli.command()
@click.option("--out", default="data", help="Output directory for the data/ catalog.")
@click.option("--limit", type=int, default=None, help="Max repos per source (for testing).")
@click.option("--only", type=click.Choice(["quay", "dockerhub"]), default=None)
@click.option("--recipes-dir", default=None, help="Path to a bioconda-recipes recipes/ dir.")
def build(out, limit, only, recipes_dir):
    """Regenerate the static data catalog."""
    from biocontainers_pipeline.build import run_build

    run_build(out=out, limit=limit, only=only, recipes_dir=recipes_dir)


if __name__ == "__main__":
    cli()
