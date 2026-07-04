<template>
  <div id="app">
    <SiteNav />
    <div v-if="showApiNotice" class="api-notice">
      <span>
        The BioContainers REST API (<code>api.biocontainers.pro</code>) has been
        <strong>deprecated</strong>. This registry is now a fully static site — search runs in
        your browser and the catalog is rebuilt nightly from Bioconda &amp; BioContainers.
      </span>
      <a class="close" title="Dismiss" @click="dismissApiNotice">×</a>
    </div>
    <router-view />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SiteNav from './components/Nav.vue'

const dismissed =
  typeof sessionStorage !== 'undefined' && sessionStorage.getItem('apiNoticeDismissed') === '1'
const showApiNotice = ref(!dismissed)

function dismissApiNotice() {
  showApiNotice.value = false
  if (typeof sessionStorage !== 'undefined') sessionStorage.setItem('apiNoticeDismissed', '1')
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}
.api-notice {
  background: #fff9e6;
  border-bottom: 1px solid #ffe58f;
  color: #664d03;
  padding: 8px 16px;
  font-size: 13px;
  line-height: 1.5;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.api-notice code {
  background: #fff1c2;
  padding: 1px 5px;
  border-radius: 3px;
}
.api-notice .close {
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
  color: #997404;
  flex: none;
}
</style>
