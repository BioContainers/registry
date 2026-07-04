import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('./views/Home.vue') },
  { path: '/registry', name: 'registry', component: () => import('./views/Registry.vue') },
  { path: '/tools/:id', name: 'tool', component: () => import('./views/Tool.vue') },
  { path: '/:pathMatch(.*)*', name: 'notfound', component: () => import('./views/NotFound.vue') },
]

export default createRouter({
  history: createWebHistory('/'),
  routes,
})
