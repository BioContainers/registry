<template>
  <div class="home">
    <section class="hero">
      <img class="hero-img" src="/static/images/containers.png" alt="BioContainers" />
      <h2 class="subtitle">BioContainers</h2>
      <h1 class="title" v-if="stats">
        {{ stats.tools.toLocaleString() }} tools, {{ stats.versions.toLocaleString() }} versions,
        packages and containers
      </h1>
      <Spin v-else size="large" />
      <div class="cta">
        <a class="btn" href="https://biocontainers-edu.readthedocs.io/en/latest/">Quick Start</a>
        <a class="btn" @click="$router.push('/registry')">Registry</a>
      </div>
    </section>

    <section class="flow" v-if="stats">
      <h3>BioContainers Flow</h3>
      <div class="flow-row">
        <span>SOFTWARE</span>
        <Icon type="md-arrow-round-forward" size="28" />
        <span>CONTAINER</span>
        <Icon type="md-arrow-round-forward" size="28" />
        <span>WORKFLOW</span>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadStats } from '../lib/dataClient.js'

const stats = ref(null)
onMounted(async () => {
  stats.value = await loadStats()
})
</script>

<style scoped>
.hero {
  text-align: center;
  padding: 64px 16px;
}
.hero-img {
  width: 160px;
  margin-bottom: 24px;
}
.subtitle {
  color: #808695;
}
.title {
  font-size: 28px;
  margin: 16px 0;
}
.cta {
  margin-top: 24px;
  display: flex;
  gap: 12px;
  justify-content: center;
}
.btn {
  padding: 8px 20px;
  border: 1px solid #2d8cf0;
  border-radius: 4px;
  color: #2d8cf0;
  cursor: pointer;
}
.flow {
  text-align: center;
  padding: 32px 16px 64px;
}
.flow-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  font-weight: bold;
  color: #515a6e;
  margin-top: 16px;
}
</style>
