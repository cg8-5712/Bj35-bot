<!--
 * @fileoverview LoginCallback.vue - 企业微信OAuth回调处理页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center">
    <div class="w-full sm:max-w-[480px] p-6">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <img class="mx-auto h-10 w-auto" src="@/assets/favicon.svg" alt="Login" />
        <h2 class="mt-6 text-center text-2xl/9 font-bold tracking-tight text-gray-900">处理登录中...</h2>
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full">
        <div class="bg-white px-6 py-12 shadow-md rounded-lg sm:px-12 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p class="mt-4 text-gray-600">正在处理企业微信登录，请稍候...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import AuthService from '@/services/AuthService'
import NotificationService from '@/services/NotificationService'

const router = useRouter()
const route = useRoute()

onMounted(() => {
  const token = route.query.token
  
  if (token) {
    // 处理回调，保存token
    const success = AuthService.handleOAuthCallback(token)
    
    if (success) {
      NotificationService.notify('企业微信登录成功', 'success')
      // 登录成功，跳转到首页
      router.push('/')
    } else {
      NotificationService.notify('企业微信登录失败', 'error')
      router.push('/login')
    }
  } else {
    NotificationService.notify('企业微信登录失败：缺少令牌', 'error')
    router.push('/login')
  }
})
</script>
