import { it, expect, vi, beforeEach } from 'vitest'
import * as client from '../src/lib/dataClient.js'

beforeEach(() => {
  client.__reset()
})

it('loadStats fetches and caches', async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ tools: 5 }) })
  vi.stubGlobal('fetch', fetchMock)
  expect(await client.loadStats()).toEqual({ tools: 5 })
  await client.loadStats()
  expect(fetchMock).toHaveBeenCalledTimes(1)
})

it('loadTool fetches by id', async () => {
  const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ id: 'samtools' }) })
  vi.stubGlobal('fetch', fetchMock)
  const t = await client.loadTool('samtools')
  expect(t.id).toBe('samtools')
  expect(fetchMock.mock.calls[0][0]).toContain('data/tools/samtools.json')
})
