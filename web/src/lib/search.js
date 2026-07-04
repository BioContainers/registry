import MiniSearch from 'minisearch'

const STORE = [
  'id', 'name', 'description', 'license',
  'registries', 'latest_version', 'versionCount',
  'biotools', 'doi',
]

export function buildIndex(records) {
  const mini = new MiniSearch({
    fields: ['name', 'description'],
    storeFields: STORE,
    searchOptions: { boost: { name: 3 }, prefix: true, fuzzy: 0.2 },
  })
  mini.addAll(records)
  return mini
}

export function runSearch(mini, query) {
  const q = (query || '').trim()
  if (!q) return null
  return mini.search(q).map((h) => {
    const doc = {}
    for (const k of STORE) doc[k] = h[k]
    return doc
  })
}
