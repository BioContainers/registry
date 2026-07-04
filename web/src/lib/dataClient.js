const base = () => (import.meta.env?.BASE_URL || '/')

export const dataUrl = (path) => `${base()}data/${path}`

let _index, _facets, _stats
const _tools = new Map()

async function getJson(url) {
  const r = await fetch(url)
  if (!r.ok) throw new Error(`fetch ${url} -> ${r.status}`)
  return r.json()
}

export async function loadIndex() {
  return (_index ??= await getJson(dataUrl('search-index.json')))
}

export async function loadFacets() {
  return (_facets ??= await getJson(dataUrl('facets.json')))
}

export async function loadStats() {
  return (_stats ??= await getJson(dataUrl('stats.json')))
}

export async function loadTool(id) {
  if (!_tools.has(id)) _tools.set(id, await getJson(dataUrl(`tools/${id}.json`)))
  return _tools.get(id)
}

export function __reset() {
  _index = _facets = _stats = undefined
  _tools.clear()
}
