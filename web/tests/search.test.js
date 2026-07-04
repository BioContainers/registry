import { it, expect } from 'vitest'
import { buildIndex, runSearch } from '../src/lib/search.js'

const recs = [
  { id: 'samtools', name: 'samtools', description: 'SAM/BAM tools', license: 'MIT', toolclass: 'CommandLineTool', registries: ['quay.io'], latest_version: '1.19', versionCount: 2, total_pulls: 10 },
  { id: 'bwa', name: 'bwa', description: 'Burrows-Wheeler aligner', license: 'GPL', toolclass: 'CommandLineTool', registries: ['quay.io'], latest_version: '0.7', versionCount: 1, total_pulls: 5 },
]

it('finds by name prefix', () => {
  const mini = buildIndex(recs)
  const hits = runSearch(mini, 'samto')
  expect(hits[0].id).toBe('samtools')
})

it('empty query returns null', () => {
  const mini = buildIndex(recs)
  expect(runSearch(mini, '   ')).toBeNull()
})
