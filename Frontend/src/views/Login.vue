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
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import AuthService from '@/services/AuthService'
import NotificationService from '@/services/NotificationService'

const router = useRouter()

const username = ref('')
const password = ref('')
const rememberMe = ref(Boolean)

rememberMe.value = true

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
</script>