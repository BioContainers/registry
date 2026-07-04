<template>
  <div class="nav-container">
    <Menu mode="horizontal" @on-select="go">
      <a class="logo" @click="$router.push('/')">
        <img src="/static/logo/biocontainers-logo.png" width="40" height="40" alt="" /> BioContainers
      </a>
      <MenuItem name="/registry"><Icon type="ios-search" /> Registry</MenuItem>
      <MenuItem name="docs"><Icon type="ios-information-circle-outline" /> Documentation</MenuItem>
      <MenuItem name="github"><Icon type="logo-github" /> GitHub</MenuItem>
    </Menu>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const links = {
  docs: 'https://biocontainers-edu.readthedocs.io/',
  github: 'https://github.com/BioContainers',
}
function go(name) {
  if (String(name).startsWith('/')) router.push(name)
  else if (links[name]) window.open(links[name], '_blank')
}
</script>

<style scoped>
.nav-container {
  border-bottom: 1px solid #e8eaec;
}
.logo {
  font-size: 14px;
  padding: 0 16px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
</style>
