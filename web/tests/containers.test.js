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

it('reconstructs a dockerfile container with docker:// singularity', () => {
  const cs = versionContainers('diann', { version: '1.8.1', docker: 'biocontainers/diann:1.8.1_cv2' })
  expect(cs).toEqual([
    { type: 'docker', image: 'biocontainers/diann:1.8.1_cv2' },
    { type: 'singularity', command: 'singularity pull docker://biocontainers/diann:1.8.1_cv2' },
  ])
})

it('installFlags and command helpers', () => {
  expect(installFlags(bioconda)).toEqual({ conda: true, docker: true, singularity: true })
  expect(installFlags(dockerfile)).toEqual({ conda: false, docker: true, singularity: true })
  expect(condaCommand(bioconda)).toBe('conda install -c bioconda s=1.19')
  expect(dockerCommand(bioconda)).toBe('docker pull quay.io/biocontainers/s:1.19--h50ea8bc_0')
  expect(singularityCommand(bioconda)).toBe(
    'singularity pull https://depot.galaxyproject.org/singularity/s:1.19--h50ea8bc_0'
  )
  expect(singularityCommand(dockerfile)).toBe('singularity pull docker://biocontainers/abyss:2.1.5')
})
