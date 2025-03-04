import { createRouter, createWebHistory } from 'vue-router'
import status from '@/views/Status.vue'
import dashboard from '@/views/Dashboard.vue'
import NotFound from '@/views/NotFound.vue'

const routes = [
  { path: '/', name: 'status', component: status },
  { path: '/dashboard', name: 'dashboard', component: dashboard},
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router