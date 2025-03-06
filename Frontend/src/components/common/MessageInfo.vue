<!--
 * @fileoverview MessageInfo.vue - 通用信息提示组件
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 MIT 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div aria-live="assertive" class="pointer-events-none fixed inset-x-0 bottom-0 sm:bottom-auto sm:top-16 flex items-end px-4 py-6 sm:items-start sm:p-6 z-40">
    <div class="flex w-full flex-col items-center space-y-4 sm:items-end">
      <transition enter-active-class="transform ease-out duration-300 transition" enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2" enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="notificationService.state.show" class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white ring-1 shadow-lg ring-black/5">
          <div class="p-4">
            <div class="flex items-start">
              <div class="shrink-0">
                <CheckCircleIcon v-if="notificationService.state.type === 'success'" class="size-6 text-green-400" aria-hidden="true" />
                <InformationCircleIcon v-else-if="notificationService.state.type === 'info'" class="size-6 text-blue-400" aria-hidden="true" />
                <XCircleIcon v-else class="size-6 text-red-400" aria-hidden="true" />
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p class="text-sm font-medium text-gray-900">{{ notificationService.state.message }}</p>
              </div>
              <div class="ml-4 flex shrink-0">
                <button type="button" @click="notificationService.close" class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:outline-hidden">
                  <span class="sr-only">Close</span>
                  <XMarkIcon class="size-5" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { CheckCircleIcon, XCircleIcon } from '@heroicons/vue/24/outline'
import { XMarkIcon, InformationCircleIcon } from '@heroicons/vue/20/solid'
import notificationService from '@/services/NotificationService'
</script>