<!--
 * @fileoverview Login.vue - 登录页面
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
        <h2 class="mt-6 text-center text-2xl/9 font-bold tracking-tight text-gray-900">登录您的账户</h2>
      </div>

      <div class="mt-10 sm:mx-auto sm:w-full">
        <div class="bg-white px-6 py-12 shadow-md rounded-lg sm:px-12">
          <form class="space-y-6" @submit.prevent="handleLogin">
            <div>
              <label for="username" class="block text-sm/6 font-medium text-gray-900">用户名</label>
              <div class="mt-2">
                <input v-model="username" type="text" name="username" id="username" autocomplete="username" required="" class="border border-solid border-zinc-200 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
              </div>
            </div>

            <div>
              <label for="password" class="block text-sm/6 font-medium text-gray-900">密码</label>
              <div class="mt-2">
                <input v-model="password" type="password" name="password" id="password" autocomplete="current-password" required="" class="border border-solid border-zinc-200 block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 outline-gray-300 placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6" />
              </div>
            </div>

            <div class="flex items-center justify-between">
              <div class="flex gap-3">
                <div class="flex h-6 shrink-0 items-center">
                  <div class="group grid size-4 grid-cols-1">
                    <input v-model="rememberMe" id="remember-me" name="remember-me" type="checkbox" class="col-start-1 row-start-1 appearance-none rounded-sm border border-gray-300 bg-white checked:border-indigo-600 checked:bg-indigo-600 indeterminate:border-indigo-600 indeterminate:bg-indigo-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100 forced-colors:appearance-auto"/>
                    <svg class="pointer-events-none col-start-1 row-start-1 size-3.5 self-center justify-self-center stroke-white group-has-disabled:stroke-gray-950/25" viewBox="0 0 14 14" fill="none">
                      <path class="opacity-0 group-has-checked:opacity-100" d="M3 8L6 11L11 3.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                      <path class="opacity-0 group-has-indeterminate:opacity-100" d="M3 7H11" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </div>
                </div>
                <label for="remember-me" class="block text-sm/6 text-gray-900">记住我</label>
              </div>
            </div>

            <div>
              <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">登录</button>
            </div>

            <div class="relative mt-6">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-200"></div>
              </div>
              <div class="relative flex justify-center text-sm font-medium leading-6">
                <span class="bg-white px-6 text-gray-500">或者</span>
              </div>
            </div>

            <div class="mt-6">
              <button
                type="button"
                @click="handleWeComLogin"
                class="flex w-full justify-center items-center gap-3 rounded-md bg-green-500 px-3 py-1.5 text-sm/6 font-semibold text-white shadow-xs hover:bg-green-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-green-500"
              >
                <img src="https://wwcdn.weixin.qq.com/node/wework/images/WeComlogo_215x20.png" alt="WeChat Work" class="h-4" />
                使用企业微信登录
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import AuthService from '@/services/AuthService'
import NotificationService from '@/services/NotificationService'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const rememberMe = ref(Boolean)

rememberMe.value = true

// 检查URL中是否有错误信息
onMounted(() => {
  const error = route.query.error
  if (error === 'missing_code') {
    NotificationService.notify('企业微信登录失败：缺少授权码', 'error')
  } else if (error === 'auth_failed') {
    NotificationService.notify('企业微信登录失败：认证失败', 'error')
  }
})

async function handleLogin() {
  try {
    NotificationService.notify('登录中……', 'info')
    await AuthService.login(username.value, password.value, rememberMe.value)

    if (AuthService.isAuthenticated()) {
      NotificationService.notify('登录成功', 'success')
      router.push('/')
    } else {
      NotificationService.notify('登录失败，请检查您的用户名和密码', 'error')
    }
  } catch (error) {
    console.error('Failed to login:', error.message)
    NotificationService.notify('系统错误：' + error.message, 'error')
  }
}

async function handleWeComLogin() {
  try {
    NotificationService.notify('正在跳转到企业微信登录……', 'info')
    const authUrl = await AuthService.getWeComAuthUrl()
    window.location.href = authUrl
  } catch (error) {
    console.error('Failed to get WeChat Work auth URL:', error)
    NotificationService.notify('获取企业微信登录链接失败：' + error.message, 'error')
  }
}
</script>