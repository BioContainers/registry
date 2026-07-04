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

// When a registry search finds nothing, offer to search the upstream registries directly.
export function externalSearchLinks(keyword) {
  const q = encodeURIComponent((keyword || '').trim())
  return [
    { label: 'quay.io / biocontainers', url: `https://quay.io/search?q=${q}` },
    { label: 'DockerHub / biocontainers', url: `https://hub.docker.com/search?q=${q}` },
  ]
}

// Framework papers to cite when using a container.
const BIOCONTAINERS_PAPER = {
  key: 'biocontainers',
  text: 'da Veiga Leprevost F, Grüning BA, et al. (2017) BioContainers: an open-source and community-driven framework for software standardization. Bioinformatics 33(16):2580-2582.',
  url: 'https://doi.org/10.1093/bioinformatics/btx192',
}
const BIOCONDA_PAPER = {
  key: 'bioconda',
  text: 'Grüning B, Dale R, Sjödin A, et al. (2018) Bioconda: sustainable and comprehensive software distribution for the life sciences. Nature Methods 15:475-476.',
  url: 'https://doi.org/10.1038/s41592-018-0046-7',
}

// bioconda-based tools -> cite both Bioconda and BioContainers.
// Docker(file)-based only -> cite BioContainers only.
export function citations(tool) {
  return isBioconda(tool) ? [BIOCONDA_PAPER, BIOCONTAINERS_PAPER] : [BIOCONTAINERS_PAPER]
}
