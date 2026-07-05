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
