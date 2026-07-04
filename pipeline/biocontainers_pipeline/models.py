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
    home_url: str = ""
    license: str = ""
    total_pulls: int = 0
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
        return self.versions[0].version if self.versions else ""

    def container_count(self) -> int:
        # a bioconda version = docker+singularity+conda (3); a Dockerfile version = 1
        return sum(3 if v.build is not None else (1 if v.docker else 0) for v in self.versions)
