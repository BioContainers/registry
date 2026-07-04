// Turn identifiers and tool names into external links (no data fetched).

export function parseIdentifier(id) {
  const idx = id.indexOf(':')
  const prefix = idx === -1 ? id : id.slice(0, idx)
  const value = idx === -1 ? '' : id.slice(idx + 1)
  switch (prefix) {
    case 'biotools':
      return { label: `bio.tools: ${value}`, url: `https://bio.tools/${value}` }
    case 'doi':
      return { label: `DOI: ${value}`, url: `https://doi.org/${value}` }
    case 'usegalaxy-eu':
      return { label: `Galaxy: ${value}`, url: `https://usegalaxy.eu/tools/list?q=${encodeURIComponent(value)}` }
    default:
      return { label: id, url: null }
  }
}

export function isBioconda(tool) {
  return (tool.versions || []).some((v) => v.build !== undefined && v.build !== null)
}

// Always-available registry/recipe links for bioconda tools (constructed from the name).
export function registryLinks(tool) {
  if (!isBioconda(tool)) return []
  const n = tool.name
  return [
    { label: 'Bioconda recipe', url: `https://bioconda.github.io/recipes/${n}/README.html` },
    { label: 'Browse quay.io tags', url: `https://quay.io/repository/biocontainers/${n}?tab=tags` },
    { label: 'anaconda.org', url: `https://anaconda.org/bioconda/${n}` },
    { label: 'Recipe source', url: `https://github.com/bioconda/bioconda-recipes/tree/master/recipes/${n}` },
  ]
}

export function maintainerUrl(handle) {
  return `https://github.com/${handle}`
}
