import { it, expect } from 'vitest'
import {
  versionContainers,
  installFlags,
  condaCommand,
  dockerCommand,
  singularityCommand,
} from '../src/lib/containers.js'

const bioconda = { id: 's', name: 's', versions: [{ version: '1.19', build: 'h50ea8bc_0' }] }
const dockerfile = { id: 'abyss', name: 'abyss', versions: [{ version: '2.1.5', docker: 'biocontainers/abyss:2.1.5' }] }

it('reconstructs bioconda containers from name+build', () => {
  const cs = versionContainers('s', { version: '1.19', build: 'h50ea8bc_0' })
  const by = Object.fromEntries(cs.map((c) => [c.type, c]))
  expect(by.docker.image).toBe('quay.io/biocontainers/s:1.19--h50ea8bc_0')
  expect(by.singularity.url).toBe('https://depot.galaxyproject.org/singularity/s:1.19--h50ea8bc_0')
  expect(by.conda.command).toBe('conda install -c bioconda s=1.19')
})

it('reconstructs a dockerfile container', () => {
  const cs = versionContainers('abyss', { version: '2.1.5', docker: 'biocontainers/abyss:2.1.5' })
  expect(cs).toEqual([{ type: 'docker', image: 'biocontainers/abyss:2.1.5' }])
})

it('installFlags and command helpers', () => {
  expect(installFlags(bioconda)).toEqual({ conda: true, docker: true, singularity: true })
  expect(installFlags(dockerfile)).toEqual({ conda: false, docker: true, singularity: false })
  expect(condaCommand(bioconda)).toBe('conda install -c bioconda s=1.19')
  expect(dockerCommand(bioconda)).toBe('docker pull quay.io/biocontainers/s:1.19--h50ea8bc_0')
  expect(singularityCommand(bioconda)).toBe(
    'singularity pull https://depot.galaxyproject.org/singularity/s:1.19--h50ea8bc_0'
  )
  expect(singularityCommand(dockerfile)).toBeNull()
})
