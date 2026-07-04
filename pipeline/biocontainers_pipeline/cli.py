import click


@click.group()
def cli():
    """BioContainers static data pipeline."""


@cli.command()
@click.option("--out", default="data", help="Output directory for the data/ catalog.")
@click.option("--recipes-dir", default=None, help="Path to a bioconda-recipes recipes/ dir (metadata).")
@click.option("--containers-dir", default=None, help="Path to a BioContainers/containers checkout (Dockerfile tools).")
@click.option("--repodata-cache", default="/tmp/bioconda-repodata", help="Where to cache downloaded repodata.")
@click.option("--limit", type=int, default=None, help="Max bioconda tools (for testing).")
def build(out, recipes_dir, containers_dir, repodata_cache, limit):
    """Regenerate the static data catalog from bioconda repodata + recipes + Dockerfiles."""
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    from biocontainers_pipeline.build import run_build

    run_build(
        out=out,
        recipes_dir=recipes_dir,
        containers_dir=containers_dir,
        repodata_cache=repodata_cache,
        limit=limit,
    )


if __name__ == "__main__":
    cli()
