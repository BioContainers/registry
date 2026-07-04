export function applyFacet(records, facetName, facetValue) {
  if (!facetName || !facetValue) return records
  if (facetName === 'registry') {
    return records.filter((r) => (r.registries || []).includes(facetValue))
  }
  return records.filter((r) => r[facetName] === facetValue)
}

export function sortRecords(records, key, order) {
  const dir = order === 'asc' ? 1 : -1
  return [...records].sort((a, b) => {
    const av = a[key]
    const bv = b[key]
    if (typeof av === 'string') return av.localeCompare(bv) * dir
    return (av - bv) * dir
  })
}

export function paginate(records, page, pageSize) {
  const start = (page - 1) * pageSize
  return records.slice(start, start + pageSize)
}
