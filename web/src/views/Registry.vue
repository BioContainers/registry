<template>
  <div class="content">
    <h1>Search</h1>
    <Input
      v-model="keywords"
      search
      placeholder="Search tools…"
      @on-search="onSearch"
      @on-enter="onSearch"
    />

    <div class="options">
      <span>Sort by:</span>
      <Select v-model="sortKey" style="width: 130px" @on-change="refresh">
        <Option value="name">Name</Option>
        <Option value="versionCount">Versions</Option>
      </Select>
      <Select v-model="sortOrder" style="width: 110px" @on-change="refresh">
        <Option value="desc">Desc</Option>
        <Option value="asc">Asc</Option>
      </Select>
      <span>Refine:</span>
      <Select v-model="facetName" style="width: 130px" @on-change="onFacetName" clearable>
        <Option v-for="f in facets" :key="f.facet" :value="f.facet">{{ f.facet }}</Option>
      </Select>
      <Select v-model="facetValue" style="width: 220px" @on-change="refresh" filterable clearable>
        <Option v-for="v in facetValues" :key="v.value" :value="v.value">
          {{ v.value }} ({{ v.count }})
        </Option>
      </Select>
    </div>

    <div class="results">
      <Spin fix v-if="loading" />
      <Card v-for="item in pageItems" :key="item.id" class="card">
        <template #title>
          <a class="tool-name" @click="$router.push(`/tools/${item.id}`)">{{ item.name }}</a>
        </template>
        <p class="desc">{{ item.description || 'No description available.' }}</p>
        <div class="meta">
          <Tag v-for="r in item.registries" :key="r" color="primary">{{ r }}</Tag>
          <Tag v-if="item.license" color="default">{{ item.license }}</Tag>
          <span class="ver">v{{ item.latest_version }} · {{ item.versionCount }} versions</span>
        </div>
      </Card>
      <div v-if="!loading && !pageItems.length" class="no-data">No matching tools.</div>
    </div>

    <Page
      :total="filtered.length"
      :current="page"
      :page-size="pageSize"
      show-elevator
      class="pager"
      @on-change="(p) => (page = p)"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { loadIndex, loadFacets } from '../lib/dataClient.js'
import { buildIndex, runSearch } from '../lib/search.js'
import { applyFacet, sortRecords, paginate } from '../lib/registryState.js'

const keywords = ref('')
const sortKey = ref('name')
const sortOrder = ref('asc')
const facetName = ref('')
const facetValue = ref('')
const page = ref(1)
const pageSize = ref(30)
const loading = ref(true)
const records = ref([])
const facets = ref([])
const searched = ref(null)
let mini = null

const facetValues = computed(
  () => facets.value.find((f) => f.facet === facetName.value)?.values || []
)
const baseRecords = computed(() => searched.value ?? records.value)
const filtered = computed(() =>
  sortRecords(
    applyFacet(baseRecords.value, facetName.value, facetValue.value),
    sortKey.value,
    sortOrder.value
  )
)
const pageItems = computed(() => paginate(filtered.value, page.value, pageSize.value))

function onSearch() {
  searched.value = runSearch(mini, keywords.value)
  page.value = 1
}
function onFacetName() {
  facetValue.value = ''
  refresh()
}
function refresh() {
  page.value = 1
}

onMounted(async () => {
  const [idx, fac] = await Promise.all([loadIndex(), loadFacets()])
  records.value = idx
  facets.value = fac
  mini = buildIndex(idx)
  loading.value = false
})
</script>

<style scoped>
.content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px 16px;
}
.options {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 16px 0;
}
.results {
  position: relative;
  min-height: 120px;
}
.card {
  margin-bottom: 12px;
}
.tool-name {
  font-weight: bold;
  cursor: pointer;
}
.desc {
  color: #515a6e;
  margin: 8px 0;
}
.meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.ver {
  color: #808695;
  font-size: 12px;
  margin-left: auto;
}
.no-data {
  text-align: center;
  color: #808695;
  padding: 40px;
}
.pager {
  margin-top: 16px;
  text-align: center;
}
</style>
