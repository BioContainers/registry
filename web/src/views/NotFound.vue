<template>
  <div class="nf">
    <h1>404</h1>
    <p>Tool or page not found.</p>
    <a @click="$router.push('/registry')">Back to registry</a>
  </div>
</template>

<style scoped>
.nf {
  text-align: center;
  padding: 80px 16px;
}
.nf a {
  color: #2d8cf0;
  cursor: pointer;
}
</style>
