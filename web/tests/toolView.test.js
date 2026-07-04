import { it, expect } from 'vitest'
import { installFlags, condaCommand, dockerCommand, singularityCommand } from '../src/lib/toolView.js'

const tool = {
  id: 's',
  name: 's',
  versions: [
    {
      version: '1.19',
      containers: [
        { type: 'docker', image: 'quay.io/biocontainers/s:1.19--0' },
        { type: 'singularity', url: 'https://depot.galaxyproject.org/singularity/s:1.19--0' },
        { type: 'conda', command: 'conda install -c bioconda s=1.19' },
      ],
    },
  ],
}

it('installFlags detects container types', () => {
  expect(installFlags(tool)).toEqual({ conda: true, docker: true, singularity: true })
})

it('condaCommand returns latest command', () => {
  expect(condaCommand(tool)).toBe('conda install -c bioconda s=1.19')
})

it('dockerCommand builds a docker pull', () => {
  expect(dockerCommand(tool)).toBe('docker pull quay.io/biocontainers/s:1.19--0')
})

it('singularityCommand builds a singularity pull', () => {
  expect(singularityCommand(tool)).toBe(
    'singularity pull https://depot.galaxyproject.org/singularity/s:1.19--0'
  )
})
