<template>
  <div class="nav-container">
    <a class="logo" @click="$router.push('/')">
      <img src="/static/logo/biocontainers-logo.png" width="40" height="40" alt="" /> BioContainers
    </a>
    <Menu mode="horizontal" class="nav-menu" @on-select="go">
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
  display: flex;
  align-items: center;
  border-bottom: 1px solid #dcdee2;
  padding: 0 8px;
}
.logo {
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 0 8px;
  white-space: nowrap;
}
/* push the menu (Registry / Documentation / GitHub) to the right */
.nav-menu {
  margin-left: auto;
}
/* the container already draws the full-width bottom line */
.nav-menu :deep(.ivu-menu) {
  background: transparent;
}
.nav-menu.ivu-menu-horizontal::after {
  display: none;
}
</style>
