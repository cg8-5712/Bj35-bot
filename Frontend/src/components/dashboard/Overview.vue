<!--
 * @fileoverview Overview.vue - 概览页面
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 GPL3.0 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
  <div>
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">机器人状态列表</h1>
      <p class="mt-1 text-sm text-gray-500">点击查看机器人详细信息</p>
    </div>
    <LoadingSpinner v-if="loading" message="加载中..." />
    <div v-else>
      <TransitionGroup 
        name="stagger-fade" 
        tag="ul" 
        class="grid grid-cols-1 gap-x-6 gap-y-8 lg:grid-cols-3 xl:gap-x-8"
        role="list"
      >
        <li 
          v-for="(robot, index) in robots" 
          :key="robot.id" 
          class="overflow-hidden rounded-xl border border-gray-200 slide-in-right cursor-pointer hover:shadow-md transition-shadow"
          :style="{ animationDelay: `${index * 150}ms` }"
          @click="showRobotDetail(robot)"
        >
          <div class="flex items-center gap-x-4 border-b border-gray-900/5 bg-gray-50 p-6">
            <img :src="robot.imageUrl" :alt="robot.name" class="size-12 flex-none rounded-lg bg-white object-cover ring-1 ring-gray-900/10" />
            <div class="flex flex-col min-w-0 flex-1">
              <div class="text-sm font-medium text-gray-900">{{ robot.name }}</div>
              <div class="text-xs text-gray-500 truncate" :title="robot.id">ID: {{ robot.id }}</div>
            </div>
            <div class="flex-shrink-0 p-2 rounded-full" :class="robot.status.isOnline ? 'bg-green-50' : 'bg-red-50'">
              <div class="w-3 h-3 rounded-full" :class="robot.status.isOnline ? 'bg-green-500' : 'bg-red-500'"></div>
            </div>
          </div>
          <dl class="-my-3 divide-y divide-gray-100 px-6 py-4 text-sm/6">
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">电量</dt>
              <dd class="text-gray-700 flex items-center">
                <div class="w-16 bg-gray-200 rounded-full h-1.5 mr-2 dark:bg-gray-700">
                  <div 
                    class="h-1.5 rounded-full" 
                    :class="getBatteryColorClass(robot.status.power)"
                    :style="`width: ${robot.status.power}%`"
                  ></div>
                </div>
                {{ robot.status.power }}%
                <div v-if="robot.status.isCharging" class="ml-2 text-xs text-gray-500">充电中</div>
              </dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">任务状态</dt>
              <dd class="flex items-start gap-x-2">
                <div class="font-medium text-gray-900">{{ robot.status.message }}</div>
                <div :class="[statuses[robot.status.status], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">{{ robot.status.status }}</div>
              </dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">位置</dt>
              <dd class="text-gray-700">{{ robot.status.location }}</dd>
            </div>
            <div class="flex justify-between gap-x-4 py-3">
              <dt class="text-gray-500">货仓ID</dt>
              <dd class="text-gray-700">{{ robot.cabinId }}</dd>
            </div>
          </dl>
        </li>
      </TransitionGroup>
      
      <!-- 没有数据时显示 -->
      <div v-if="robots.length === 0" class="text-center py-20">
        <div class="mx-auto h-12 w-12 text-gray-400">
          <svg class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="mt-2 text-sm font-semibold text-gray-900">暂无机器人数据</h3>
        <p class="mt-1 text-sm text-gray-500">检查网络连接或联系管理员</p>
      </div>
    </div>
    
    <!-- 机器人详情模态框 -->
    <RobotDetail 
      v-model:isOpen="isDetailOpen" 
      :robot="selectedRobot" 
      class="bg-opacity-50"
    />
  </div>
</template>

<script setup>
import { TransitionGroup } from 'vue'

import { ref, onMounted, onBeforeUnmount } from 'vue'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import RobotDetail from '@/components/dashboard/RobotDetail.vue'

// 状态样式映射
const statuses = {
  '空闲': 'text-green-700 bg-green-50 ring-green-600/20',
  '执行任务中': 'text-yellow-600 bg-yellow-50 ring-yellow-500/30',
  '未知': 'text-gray-600 bg-gray-50 ring-gray-500/10',
  '错误': 'text-red-700 bg-red-50 ring-red-600/10'
}

// 状态数据
const robots = ref([])
const loading = ref(true)

// 模态框状态
const isDetailOpen = ref(false)
const selectedRobot = ref({})

// 显示机器人详情
function showRobotDetail(robot) {
  selectedRobot.value = {
    ...robot,
    lastActivity: new Date() // 这里可以从 robot 对象中获取真实的最后活动时间
  }
  console.log(selectedRobot.value.status.isCharging)
  isDetailOpen.value = true
}

// 获取电量颜色类
function getBatteryColorClass(power) {
  if (power > 50) return 'bg-green-600'
  if (power > 20) return 'bg-yellow-300'
  return 'bg-red-600'
}

// 获取设备列表
async function fetchRobots() {
  try {
    loading.value = true
    const response = await ApiServices.getRobotList()
    robots.value = response.data
  } catch (error) {
    console.error('获取机器人列表失败:', error)
    NotificationService.notify('获取机器人列表失败: ' + error.message, 'error')
  } finally {
    loading.value = false
  }
}

function startAutoRefresh() {
  refreshTimer = setInterval(() => {
    fetchRobots()
  }, REFRESH_INTERVAL)
}

// 生命周期钩子
onMounted(() => {
  fetchRobots()
})

</script>

<style scoped>
@keyframes slideInRight {
  from {
    transform: translateX(30px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in-right {
  animation: slideInRight 0.6s ease-out forwards;
  opacity: 0; /* 初始状态是透明的 */
}

/* 列表进入/离开过渡 */
.stagger-fade-enter-active,
.stagger-fade-leave-active {
  transition: all 0.3s ease;
}
.stagger-fade-enter-from,
.stagger-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 确保列表项在离开时有正确的定位 */
.stagger-fade-leave-active {
  position: absolute;
}

/* 确保列表在项目移动时平滑过渡 */
.stagger-fade-move {
  transition: transform 0.5s ease;
}
</style>