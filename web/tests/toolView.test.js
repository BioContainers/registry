import { it, expect } from 'vitest'
import { installFlags, condaCommand } from '../src/lib/toolView.js'

const tool = {
  id: 's',
  name: 's',
  versions: [
    {
      version: '1.19',
      containers: [
        { type: 'docker', image: 'quay.io/biocontainers/s:1.19--0' },
        { type: 'conda', command: 'conda install -c bioconda s=1.19' },
      ],
    },
  ],
}

it('installFlags detects container types', () => {
  expect(installFlags(tool)).toEqual({ conda: true, docker: true, singularity: false })
})

it('condaCommand returns latest command', () => {
  expect(condaCommand(tool)).toBe('conda install -c bioconda s=1.19')
})
