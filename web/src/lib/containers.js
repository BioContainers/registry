// Reconstruct container references from a tool's minimal version record.
// bioconda version: { version, build }  -> docker(quay) + singularity + conda
// Dockerfile version: { version, docker } -> that DockerHub image

export function versionContainers(toolName, v) {
  if (v.build !== undefined && v.build !== null) {
    const tag = v.build ? `${v.version}--${v.build}` : v.version
    return [
      { type: 'docker', image: `quay.io/biocontainers/${toolName}:${tag}` },
      { type: 'singularity', url: `https://depot.galaxyproject.org/singularity/${toolName}:${tag}` },
      { type: 'conda', command: `conda install -c bioconda ${toolName}=${v.version}` },
    ]
  }
  if (v.docker) {
    // Any Docker image is also runnable with Singularity via docker://.
    return [
      { type: 'docker', image: v.docker },
      { type: 'singularity', command: `singularity pull docker://${v.docker}` },
    ]
  }
  return []
}

export function installFlags(tool) {
  const types = new Set()
  for (const v of tool.versions || []) {
    for (const c of versionContainers(tool.name, v)) types.add(c.type)
  }
  return { conda: types.has('conda'), docker: types.has('docker'), singularity: types.has('singularity') }
}

// A tool's recommended version: the newest Bioconda version if any exists,
// otherwise the newest version overall (Docker-only tools). This is what the
// Usage block and default install commands are built from, so tools that also
// exist in Bioconda steer users there rather than to the legacy Docker image.
export function primaryVersion(tool) {
  const versions = tool.versions || []
  return versions.find((v) => v.build !== undefined && v.build !== null) || versions[0] || null
}

function latestContainer(tool, type) {
  const v = primaryVersion(tool)
  if (!v) return null
  return versionContainers(tool.name, v).find((c) => c.type === type) || null
}

// "How to pull + where to browse" guide for the Packages tab. We deliberately do
// NOT enumerate versions here — the authoritative, browsable tag lists live on
// quay.io / DockerHub, and Singularity images on the Galaxy depot / BioContainers
// S3. We just give command templates (with <version>/<tag> placeholders) and links.
export function packageGuide(tool) {
  const n = tool.name
  const versions = tool.versions || []
  const isBioconda = (v) => v.build !== undefined && v.build !== null
  const bc = versions.filter(isBioconda)
  const dk = versions.filter((v) => v.docker && !isBioconda(v))
  const guide = { bioconda: null, docker: null }

  if (bc.length) {
    guide.bioconda = {
      versionCount: bc.length,
      browse: [
        { label: 'quay.io tags', url: `https://quay.io/repository/biocontainers/${n}?tab=tags` },
        { label: 'Bioconda recipe', url: `https://bioconda.github.io/recipes/${n}/README.html` },
      ],
      commands: [
        { kind: 'conda', text: `conda install -c bioconda ${n}=<version>` },
        { kind: 'docker', text: `docker pull quay.io/biocontainers/${n}:<tag>` },
        { kind: 'singularity', text: `singularity pull https://depot.galaxyproject.org/singularity/${n}:<tag>` },
      ],
      singularity: {
        text: 'Browse the Galaxy depot (one flat list of all tools)',
        url: 'https://depot.galaxyproject.org/singularity/',
      },
    }
  }
  if (dk.length) {
    guide.docker = {
      versionCount: dk.length,
      browse: [{ label: 'DockerHub tags', url: `https://hub.docker.com/r/biocontainers/${n}/tags` }],
      commands: [
        { kind: 'docker', text: `docker pull biocontainers/${n}:<tag>` },
        { kind: 'singularity', text: `singularity pull docker://biocontainers/${n}:<tag>` },
      ],
      sif: `https://containers.biocontainers.pro/s3/SingImgsRepo/${n}/<tag>/${n}_<tag>.sif`,
    }
  }
  return guide
}

export function condaCommand(tool) {
  return latestContainer(tool, 'conda')?.command || null
}

export function dockerCommand(tool) {
  const c = latestContainer(tool, 'docker')
  return c?.image ? `docker pull ${c.image}` : null
}

export function singularityCommand(tool) {
  const c = latestContainer(tool, 'singularity')
  if (!c) return null
  return c.command || (c.url ? `singularity pull ${c.url}` : null)
}
