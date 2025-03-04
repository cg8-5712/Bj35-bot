import { createRouter, createWebHistory } from 'vue-router'
import status from '@/components/status.vue'

const routes = [
  { path: '/', name: 'status', component: status }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router