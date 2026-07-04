import { it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Home from '../src/views/Home.vue'
import * as client from '../src/lib/dataClient.js'

it('renders tool count from stats', async () => {
  vi.spyOn(client, 'loadStats').mockResolvedValue({ tools: 14767, versions: 152340 })
  const wrapper = mount(Home, {
    global: { stubs: ['Spin', 'Icon', 'router-link'] },
  })
  await new Promise((r) => setTimeout(r))
  expect(wrapper.text()).toContain('14,767 tools')
})
