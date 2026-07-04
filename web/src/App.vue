<template>
  <div id="app">
    <SiteNav />
    <router-view />
  </div>
</template>

<script setup>
import SiteNav from './components/Nav.vue'
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}
</style>
