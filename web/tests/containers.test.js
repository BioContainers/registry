import { it, expect } from 'vitest'
import {
  versionContainers,
  installFlags,
  condaCommand,
  dockerCommand,
  singularityCommand,
  primaryVersion,
  packageGuide,
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

it('prioritizes bioconda: default install uses the bioconda version, not the legacy docker one', () => {
  // dual-source tool: legacy Docker version sorts on top, bioconda version below
  const dual = {
    id: 'abyss', name: 'abyss', primary: 'bioconda',
    versions: [
      { version: '2.1.5-7-deb', docker: 'biocontainers/abyss:v2.1.5-7-deb_cv1' }, // legacy, top
      { version: '2.3.7', build: 'h5b5514e_2' }, // bioconda
    ],
  }
  expect(primaryVersion(dual).version).toBe('2.3.7')
  // default docker command is the quay.io bioconda image, NOT the legacy DockerHub one
  expect(dockerCommand(dual)).toBe('docker pull quay.io/biocontainers/abyss:2.3.7--h5b5514e_2')
  expect(condaCommand(dual)).toBe('conda install -c bioconda abyss=2.3.7')
  // docker-only tool still uses its docker image
  expect(primaryVersion(dockerfile).version).toBe('2.1.5')
})

it('packageGuide: templates + browse links per source, no version enumeration', () => {
  const bioconda = { id: 's', name: 'samtools', versions: [{ version: '1.19', build: 'h0' }, { version: '1.18', build: 'h1' }] }
  const g = packageGuide(bioconda)
  expect(g.docker).toBeNull()
  expect(g.bioconda.versionCount).toBe(2)
  expect(g.bioconda.browse[0].url).toBe('https://quay.io/repository/biocontainers/samtools?tab=tags')
  expect(g.bioconda.commands.map((c) => c.kind)).toEqual(['conda', 'docker', 'singularity'])
  expect(g.bioconda.commands[0].text).toBe('conda install -c bioconda samtools=<version>')
  expect(g.bioconda.commands[1].text).toBe('docker pull quay.io/biocontainers/samtools:<tag>')

  const dockerfile = { id: 'diann', name: 'diann', versions: [{ version: '1.8.1', docker: 'biocontainers/diann:v1.8.1_cv2' }] }
  const gd = packageGuide(dockerfile)
  expect(gd.bioconda).toBeNull()
  expect(gd.docker.browse[0].url).toBe('https://hub.docker.com/r/biocontainers/diann/tags')
  expect(gd.docker.commands[0].text).toBe('docker pull biocontainers/diann:<tag>')
  expect(gd.docker.sif).toBe('https://containers.biocontainers.pro/s3/SingImgsRepo/diann/<tag>/diann_<tag>.sif')
})
