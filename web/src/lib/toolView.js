export function installFlags(tool) {
  const types = new Set()
  for (const v of tool.versions || []) {
    for (const c of v.containers || []) types.add(c.type)
  }
  return {
    conda: types.has('conda'),
    docker: types.has('docker'),
    singularity: types.has('singularity'),
  }
}

function latestContainer(tool, type) {
  const v = (tool.versions || [])[0]
  return v?.containers?.find((c) => c.type === type) || null
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
