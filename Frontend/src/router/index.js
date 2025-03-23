import { createRouter, createWebHistory } from 'vue-router'
import AuthService from '@/services/AuthService'

const routes = [
  { path: '/', name: 'Dashboard', component: () => import('@/views/dashboard.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },

  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && !AuthService.isAuthenticated()) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && AuthService.isAuthenticated()) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router