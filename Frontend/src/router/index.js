import { createRouter, createWebHistory } from 'vue-router'
import status from '@/views/status.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  { path: '/', name: 'status', component: status },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router