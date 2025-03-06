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
            <div class="flex flex-col min-w-0 flex-1">
              <div class="text-sm font-medium text-gray-900">{{ robot.name }}</div>
              <div class="text-xs text-gray-500 truncate" :title="robot.id">ID: {{ robot.id }}</div>
            </div>
            <div :class="[onlines[robot.status.isOnline], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">
              {{ robot.status.isOnline ? '在线' : '离线' }}
            </div>
          </div>
          <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm/6">
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">电量</dt>
              <dd class="text-gray-700"> {{ robot.status.power }} % </dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">任务状态</dt>
              <dd class="flex items-start gap-x-2">
                <div class="font-medium text-gray-900">{{ robot.status.message }}</div>
                <div :class="[statuses[robot.status.status], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">{{ robot.status.status }}</div>
              </dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">当前位置</dt>
              <dd class="text-gray-700"> {{ robot.status.location }} </dd>
            </div>
          </dl>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'

const loading = ref(true)

const onlines = {
  true: 'text-green-700 bg-green-50 ring-green-600/20',
  false: 'text-red-700 bg-red-50 ring-red-600/20',
}

const statuses = {
  空闲: 'text-green-700 bg-green-50 ring-green-600/20',
  执行任务中: 'text-yellow-600 bg-yellow-50 ring-yellow-500/30',
}

const robots = ref([])

async function generateRobotStatusList(devices) {
  const deviceID = devices.data.map((device) => device.deviceId);

  try {
    const deviceStatuses = await Promise.all(
      deviceID.map(id => ApiServices.getDeviceById(id))
    );
  
    const robotList = deviceStatuses.map((response, index) => {
        const id = deviceID[index];
        const data = response.data || {};
        
        return {
          id: id,
          name: `Robot-${id.substring(0, 9)}`,
          imageUrl: 'https://tailwindcss.com/plus-assets/img/logos/48x48/tuple.svg',
          status: { 
            isOnline: data.deviceStatus.isOffline === false,
            power: data.deviceStatus.powerPercent || '未知',
            message: data.message || '无信息',
            status: data.deviceStatus.isIdle ? '空闲' : '执行任务中',
            location: data.deviceStatus.currentPositionMarker || '未知位置',
          }
        };
      });

      robots.value = robotList.length > 0 ? robotList : robot;
  } catch (error) {
    console.error('获取设备状态失败:', error)
    NotificationService.notify('获取设备状态失败', 'error')
  }
}

onMounted(async () => {
  try {
    const devices = await ApiServices.getAllDevices()

    generateRobotStatusList(devices)
  } catch (error) {
    console.error('获取设备列表失败:', error)
    NotificationService.notify('获取设备列表失败', 'error')
  } finally {
    loading.value = false
  }
})

</script>
