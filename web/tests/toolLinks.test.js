import { it, expect } from 'vitest'
import { parseIdentifier, isBioconda, registryLinks, maintainerUrl } from '../src/lib/toolLinks.js'

it('parses identifiers into links', () => {
  expect(parseIdentifier('biotools:samtools')).toEqual({
    label: 'bio.tools: samtools', url: 'https://bio.tools/samtools',
  })
  expect(parseIdentifier('doi:10.1093/x')).toEqual({ label: 'DOI: 10.1093/x', url: 'https://doi.org/10.1093/x' })
  expect(parseIdentifier('unknown:z').url).toBeNull()
})

it('registryLinks only for bioconda tools', () => {
  const bioconda = { name: 's', versions: [{ version: '1', build: 'h0' }] }
  const dockerfile = { name: 'a', versions: [{ version: '1', docker: 'biocontainers/a:1' }] }
  expect(isBioconda(bioconda)).toBe(true)
  expect(isBioconda(dockerfile)).toBe(false)
  const links = registryLinks(bioconda)
  expect(links.map((l) => l.label)).toContain('Browse quay.io tags')
  expect(links[0].url).toContain('bioconda.github.io/recipes/s/')
  expect(registryLinks(dockerfile)).toEqual([])
})

it('maintainerUrl', () => {
  expect(maintainerUrl('alice')).toBe('https://github.com/alice')
})
