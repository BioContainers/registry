from dataclasses import dataclass, field


@dataclass
class Version:
    """A software version. Container commands are reconstructed by the frontend from
    the tool name + these coordinates, so we store only what can't be derived:

    - bioconda package: `build` set (the quay/singularity tag is `version--build`);
      docker/singularity/conda commands all derive from name+version+build.
    - Dockerfile image: `docker` set to the full DockerHub image reference.
    """
    version: str
    last_updated: str = ""
    build: str | None = None   # bioconda build string; None => not a bioconda version
    docker: str | None = None  # Dockerfile-based DockerHub image reference


@dataclass
class Tool:
    id: str
    name: str
    description: str = ""
    long_description: str = ""
    home_url: str = ""
    doc_url: str = ""
    dev_url: str = ""
    license: str = ""
    license_family: str = ""
    total_pulls: int = 0
    identifiers: list[str] = field(default_factory=list)   # e.g. "biotools:samtools", "doi:10.x"
    maintainers: list[str] = field(default_factory=list)   # GitHub handles
    dependencies: list[str] = field(default_factory=list)  # run deps of the latest version
    versions: list[Version] = field(default_factory=list)

    def registries(self) -> list[str]:
        regs = set()
        for v in self.versions:
            if v.build is not None:
                regs.update({"conda", "quay.io", "singularity"})
            if v.docker:
                regs.add("DockerHub")
        return sorted(regs)

    def latest_version(self) -> str:
        # Prefer the newest Bioconda version (maintained/patched) over a legacy
        # Dockerfile version, even if the Docker version sorts higher by number.
        for v in self.versions:
            if v.build is not None:
                return v.version
        return self.versions[0].version if self.versions else ""

    def primary_source(self) -> str:
        """'bioconda' when the tool has any Bioconda version, else 'dockerhub'."""
        return "bioconda" if any(v.build is not None for v in self.versions) else "dockerhub"

    def container_count(self) -> int:
        # a bioconda version = docker+singularity+conda (3); a Dockerfile version = 1
        return sum(3 if v.build is not None else (1 if v.docker else 0) for v in self.versions)
