from dataclasses import dataclass, field


@dataclass
class Container:
    type: str            # docker | singularity | conda
    image: str | None = None
    url: str | None = None
    command: str | None = None
    pulls: int = 0

    def registry(self) -> str:
        if self.type == "conda":
            return "conda"
        if self.type == "singularity":
            return "singularity"
        if self.image and self.image.startswith("quay.io/"):
            return "quay.io"
        return "DockerHub"


@dataclass
class Version:
    version: str
    last_updated: str = ""
    containers: list[Container] = field(default_factory=list)


@dataclass
class Tool:
    id: str
    name: str
    description: str = ""
    home_url: str = ""
    license: str = ""
    toolclass: str = "CommandLineTool"
    total_pulls: int = 0
    versions: list[Version] = field(default_factory=list)

    def registries(self) -> list[str]:
        regs = {c.registry() for v in self.versions for c in v.containers}
        return sorted(regs)

    def latest_version(self) -> str:
        return self.versions[0].version if self.versions else ""
