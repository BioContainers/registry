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

export function condaCommand(tool) {
  const v = (tool.versions || [])[0]
  return v?.containers?.find((c) => c.type === 'conda')?.command || null
}
