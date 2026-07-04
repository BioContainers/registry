import { it, expect } from 'vitest'
import { applyFacet, sortRecords, paginate } from '../src/lib/registryState.js'

const recs = [
  { id: 'a', name: 'a', license: 'MIT', toolclass: 'CommandLineTool', registries: ['quay.io'], total_pulls: 10, versionCount: 3 },
  { id: 'b', name: 'b', license: 'GPL', toolclass: 'CommandLineTool', registries: ['DockerHub'], total_pulls: 50, versionCount: 1 },
]

it('applyFacet filters by registry membership', () => {
  expect(applyFacet(recs, 'registry', 'DockerHub').map((r) => r.id)).toEqual(['b'])
})

it('applyFacet filters by license exact', () => {
  expect(applyFacet(recs, 'license', 'MIT').map((r) => r.id)).toEqual(['a'])
})

it('sortRecords by total_pulls desc', () => {
  expect(sortRecords(recs, 'total_pulls', 'desc').map((r) => r.id)).toEqual(['b', 'a'])
})

it('paginate slices', () => {
  expect(paginate(recs, 2, 1).map((r) => r.id)).toEqual(['b'])
})
