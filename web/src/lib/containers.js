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
    return [{ type: 'docker', image: v.docker }]
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

function latestContainer(tool, type) {
  const v = (tool.versions || [])[0]
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
  return c?.url ? `singularity pull ${c.url}` : null
}
