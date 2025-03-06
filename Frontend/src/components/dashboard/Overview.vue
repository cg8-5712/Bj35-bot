<!--
 * @fileoverview Overview.vue - 概览页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 MIT 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div>
    <LoadingSpinner v-if="loading" message="加载中..." />
    <div v-else>
      <div class="border-b border-gray-200 pb-5 m-5">
        <h3 class="text-2xl font-semibold text-gray-900">机器人状态列表</h3>
        <p class="mt-2 max-w-4xl text-sm text-gray-500">点击查看机器人详细信息</p>
      </div>
      <ul role="list" class="grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8">
        <li v-for="robot in robots" :key="robots.id" class="overflow-hidden rounded-xl border border-gray-200">
          <div class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6">
            <img :src="robot.imageUrl" :alt="robot.name" class="size-12 flex-none rounded-lg bg-white object-cover ring-1 ring-gray-900/10" />
            <div class="text-sm/6 font-medium text-gray-900">{{ robot.name }}</div>
            <Menu as="div" class="relative ml-auto">
              <MenuButton class="-m-2.5 block p-2.5 text-gray-400 hover:text-gray-500">
                <span class="sr-only">查看更多</span>
                <EllipsisHorizontalIcon class="size-5" aria-hidden="true" />
              </MenuButton>
              <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
                <MenuItems class="absolute right-0 z-10 mt-0.5 w-32 origin-top-right rounded-md bg-white py-2 ring-1 shadow-lg ring-gray-900/5 focus:outline-hidden">
                  <MenuItem v-slot="{ active }">
                    <a href="#" :class="[active ? 'bg-gray-50 outline-hidden' : '', 'block px-3 py-1 text-sm/6 text-gray-900']"
                      >状态预览<span class="sr-only">, {{ robot.name }}</span></a
                    >
                  </MenuItem>
                </MenuItems>
              </transition>
            </Menu>
          </div>
          <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm/6">
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">电量</dt>
              <dd class="text-gray-700"> {{ robot.status.power }} </dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">任务状态</dt>
              <dd class="flex items-start gap-x-2">
                <div class="font-medium text-gray-900">{{ robot.status.amount }}</div>
                <div :class="[statuses[robot.status.status], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">{{ robot.status.status }}</div>
              </dd>
            </div>
          </dl>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { EllipsisHorizontalIcon } from '@heroicons/vue/20/solid'

import { ref, onMounted, computed } from 'vue'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'

const statuses = {
  空闲: 'text-green-700 bg-green-50 ring-green-600/20',
  执行任务中: 'text-yellow-600 bg-yellow-50 ring-yellow-500/30',
}

const robots = [
  {
    id: 1,
    name: 'Tuple',
    imageUrl: 'https://tailwindcss.com/plus-assets/img/logos/48x48/tuple.svg',
    status: { power: 'December 13, 2022', dateTime: '2022-12-13', amount: '$2,000.00', status: '执行任务中' },
  },
  {
    id: 2,
    name: 'SavvyCal',
    imageUrl: 'https://tailwindcss.com/plus-assets/img/logos/48x48/savvycal.svg',
    status: { power: 'January 22, 2023', dateTime: '2023-01-22', amount: '$14,000.00', status: '空闲' },
  },
]

const loading = ref(true)

onMounted(async () => {
  try {
    const devices = await ApiServices.getAllDevices()

    console.log('设备数据:', devices)
    console.log('设备数据类型:', typeof devices)
  } catch (error) {
    console.error('获取设备列表失败:', error)
    NotificationService.notify('获取设备列表失败', 'error')
  } finally {
    loading.value = false
  }
})

</script>
