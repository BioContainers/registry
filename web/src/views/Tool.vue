<template>
  <div class="content" v-if="tool">
    <Tabs v-model="tab">
      <TabPane label="Readme" name="readme">
        <Row :gutter="40">
          <Col span="16">
            <h1>{{ tool.name }}</h1>
            <p class="desc">{{ tool.description || 'No description available.' }}</p>
            <p class="long-desc" v-if="tool.long_description && tool.long_description !== tool.description">
              {{ tool.long_description }}
            </p>
            <div class="badges">
              <Tag v-if="flags.conda" color="green">conda</Tag>
              <Tag v-if="flags.docker" color="blue">docker</Tag>
              <Tag v-if="flags.singularity" color="purple">singularity</Tag>
            </div>
            <h2>Usage</h2>
            <Divider />
            <div v-if="conda" class="usage-block">
              <strong>Conda</strong>
              <p class="usage-note">
                With the <a href="https://bioconda.github.io/user/install.html#set-up-channels">bioconda channel</a>
                configured, install the latest version with:
              </p>
              <pre class="code">{{ conda }}</pre>
            </div>
            <div v-if="docker" class="usage-block">
              <strong>Docker</strong>
              <p class="usage-note">
                <a href="https://biocontainers-edu.readthedocs.io/en/latest/getting_started.html">With Docker installed</a>,
                pull the container:
              </p>
              <pre class="code">{{ docker }}</pre>
            </div>
            <div v-if="singularity" class="usage-block">
              <strong>Singularity</strong>
              <p class="usage-note">
                <a href="https://sylabs.io/guides/3.5/user-guide/quick_start.html">With Singularity installed</a>,
                pull the image:
              </p>
              <pre class="code">{{ singularity }}</pre>
            </div>
            <p class="hint">
              All versions and their pull commands are in the
              <a @click="tab = 'containers'">Packages &amp; Containers</a> tab.
            </p>

            <h2>How to cite</h2>
            <Divider />
            <p class="usage-note">If you use this container, please cite:</p>
            <ul class="cite-list">
              <li v-for="c in toolCitations" :key="c.key">
                {{ c.text }}
                <a :href="c.url" target="_blank">{{ c.url.replace('https://doi.org/', 'doi:') }}</a>
              </li>
            </ul>
          </Col>
          <Col span="8">
            <div class="prop" v-if="tool.total_pulls > 0">
              <strong>Downloads</strong>
              <div>{{ tool.total_pulls.toLocaleString() }}</div>
            </div>

            <div class="prop">
              <strong>Versions</strong>
              <div>{{ tool.versions.length }} · latest {{ tool.versions[0]?.version }}</div>
            </div>

            <div class="prop" v-if="tool.license || tool.license_family">
              <strong>License</strong>
              <div>{{ tool.license || tool.license_family }}</div>
            </div>

            <div class="prop links" v-if="tool.home_url || tool.doc_url || tool.dev_url">
              <strong>Links</strong>
              <div v-if="tool.home_url"><a :href="tool.home_url" target="_blank">Homepage</a></div>
              <div v-if="tool.doc_url"><a :href="tool.doc_url" target="_blank">Documentation</a></div>
              <div v-if="tool.dev_url"><a :href="tool.dev_url" target="_blank">Source repository</a></div>
            </div>

            <div class="prop links" v-if="identifierLinks.length">
              <strong>Identifiers</strong>
              <div v-for="ide in identifierLinks" :key="ide.label">
                <a v-if="ide.url" :href="ide.url" target="_blank">{{ ide.label }}</a>
                <span v-else>{{ ide.label }}</span>
              </div>
            </div>

            <div class="prop links" v-if="registryLinks(tool).length">
              <strong>Registry &amp; recipe</strong>
              <div v-for="l in registryLinks(tool)" :key="l.label">
                <a :href="l.url" target="_blank">{{ l.label }}</a>
              </div>
            </div>

            <div class="prop" v-if="tool.dependencies && tool.dependencies.length">
              <strong>Dependencies</strong>
              <div class="deps">
                <Tag v-for="d in tool.dependencies.slice(0, 15)" :key="d" size="small">{{ d }}</Tag>
                <span v-if="tool.dependencies.length > 15" class="more">
                  +{{ tool.dependencies.length - 15 }} more
                </span>
              </div>
            </div>

            <div class="prop links" v-if="tool.maintainers && tool.maintainers.length">
              <strong>Maintainers</strong>
              <div v-for="m in tool.maintainers" :key="m">
                <a :href="maintainerUrl(m)" target="_blank">@{{ m }}</a>
              </div>
            </div>
          </Col>
        </Row>
      </TabPane>

      <TabPane label="Packages &amp; Containers" name="containers">
        <div v-for="v in tool.versions" :key="v.version" class="ver-block">
          <h3>{{ tool.name }} {{ v.version }} <small>{{ v.last_updated }}</small></h3>
          <div v-for="(c, i) in versionContainers(tool.name, v)" :key="i" class="container-row">
            <Tag>{{ c.type }}</Tag>
            <code v-if="c.type === 'docker'">docker pull {{ c.image }}</code>
            <code v-else-if="c.type === 'singularity'">{{ c.command || `singularity pull ${c.url}` }}</code>
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
import {
  installFlags,
  condaCommand,
  dockerCommand,
  singularityCommand,
  versionContainers,
} from '../lib/containers.js'
import { parseIdentifier, registryLinks, maintainerUrl, citations } from '../lib/toolLinks.js'

const route = useRoute()
const tool = ref(null)
const tab = ref('readme')

const flags = computed(() => (tool.value ? installFlags(tool.value) : {}))
const conda = computed(() => (tool.value ? condaCommand(tool.value) : null))
const docker = computed(() => (tool.value ? dockerCommand(tool.value) : null))
const singularity = computed(() => (tool.value ? singularityCommand(tool.value) : null))
const identifierLinks = computed(() => (tool.value?.identifiers || []).map(parseIdentifier))
const toolCitations = computed(() => (tool.value ? citations(tool.value) : []))

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
.long-desc {
  color: #515a6e;
  margin: 8px 0 4px;
  white-space: pre-wrap;
}
.badges {
  margin: 12px 0;
}
.prop.links a {
  color: #2d8cf0;
}
.deps {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 4px;
}
.usage-block {
  margin-bottom: 18px;
}
.usage-note {
  color: #515a6e;
  margin: 4px 0;
}
.code,
code {
  background: #f7f7f9;
  padding: 6px 10px;
  border-radius: 4px;
  display: inline-block;
  white-space: pre-wrap;
}
.code {
  display: block;
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
.cite-list {
  padding-left: 18px;
  color: #515a6e;
}
.cite-list li {
  margin-bottom: 10px;
  line-height: 1.5;
}
.cite-list a {
  color: #2d8cf0;
  margin-left: 4px;
}
.ver-block {
  margin-bottom: 20px;
}
</style>
