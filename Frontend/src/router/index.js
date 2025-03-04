import { createRouter, createWebHistory } from 'vue-router'
import status from '@/views/Status.vue'
import dashboard from '@/views/Dashboard.vue'
import NotFound from '@/views/NotFound.vue'
import login from '@/views/login.vue'

const routes = [
  { path: '/', name: 'status', component: status },
  { path: '/dashboard', name: 'dashboard', component: dashboard},
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  { path: '/login', name: 'login', component: login }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router