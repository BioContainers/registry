<template>
  <div class="content" v-if="tool">
    <Tabs v-model="tab">
      <TabPane label="Readme" name="readme">
        <Row :gutter="40">
          <Col span="16">
            <h1>{{ tool.name }}</h1>
            <p class="desc">{{ tool.description || 'No description available.' }}</p>
            <div class="badges">
              <Tag v-if="flags.conda" color="green">conda</Tag>
              <Tag v-if="flags.docker" color="blue">docker</Tag>
              <Tag v-if="flags.singularity" color="purple">singularity</Tag>
            </div>
            <h2>Usage</h2>
            <Divider />
            <div v-if="conda">
              <strong>BioConda install</strong>
              <pre class="code">{{ conda }}</pre>
            </div>
            <p class="hint">
              Per-version Docker / Singularity / Conda commands are in the
              <a @click="tab = 'containers'">Packages &amp; Containers</a> tab.
            </p>
          </Col>
          <Col span="8">
            <div class="prop">
              <strong>Downloads</strong>
              <div>{{ tool.total_pulls.toLocaleString() }}</div>
            </div>
            <Divider />
            <div class="prop" v-if="tool.home_url">
              <strong>Homepage</strong>
              <div><a :href="tool.home_url" target="_blank">{{ tool.home_url }}</a></div>
            </div>
            <Divider v-if="tool.home_url" />
            <div class="prop">
              <strong>Versions</strong>
              <div>{{ tool.versions.length }}</div>
            </div>
            <Divider />
            <div class="prop" v-if="tool.license">
              <strong>License</strong>
              <div>{{ tool.license }}</div>
            </div>
          </Col>
        </Row>
      </TabPane>

      <TabPane label="Packages &amp; Containers" name="containers">
        <div v-for="v in tool.versions" :key="v.version" class="ver-block">
          <h3>{{ tool.name }} {{ v.version }} <small>{{ v.last_updated }}</small></h3>
          <div v-for="(c, i) in v.containers" :key="i" class="container-row">
            <Tag>{{ c.type }}</Tag>
            <code v-if="c.type === 'docker'">docker pull {{ c.image }}</code>
            <code v-else-if="c.type === 'singularity'">singularity pull {{ c.url }}</code>
            <code v-else-if="c.type === 'conda'">{{ c.command }}</code>
          </div>
        </div>
      </TabPane>
    </Tabs>
  </div>
  <Spin fix v-else />
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { loadTool } from '../lib/dataClient.js'
import { installFlags, condaCommand } from '../lib/toolView.js'

const route = useRoute()
const tool = ref(null)
const tab = ref('readme')

const flags = computed(() => (tool.value ? installFlags(tool.value) : {}))
const conda = computed(() => (tool.value ? condaCommand(tool.value) : null))

async function load(id) {
  tool.value = null
  tool.value = await loadTool(id)
}
onMounted(() => load(route.params.id))
watch(
  () => route.params.id,
  (id) => id && load(id)
)
</script>

<style scoped>
.content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
}
.desc {
  color: #515a6e;
}
.badges {
  margin: 12px 0;
}
.code,
code {
  background: #f7f7f9;
  padding: 6px 10px;
  border-radius: 4px;
  display: inline-block;
  white-space: pre-wrap;
}
.container-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 6px 0;
}
.prop {
  margin: 8px 0;
}
.hint {
  color: #808695;
  margin-top: 16px;
}
.ver-block {
  margin-bottom: 20px;
}
</style>
