<!--
 * @fileoverview RobotDetail.vue - 机器人详情模态框
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 MIT 协议，以及 Tailwind Plus Personal 许可证
-->

<template>
    <TransitionRoot as="template" :show="isOpen">
      <Dialog as="div" class="relative z-50" @close="closeModal">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
            <div class="fixed inset-0 backdrop-blur-xs transition-opacity" />
        </TransitionChild>
  
        <div class="fixed inset-0 z-10 overflow-y-auto">
          <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <TransitionChild
              as="template"
              enter="ease-out duration-300"
              enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enter-to="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leave-from="opacity-100 translate-y-0 sm:scale-100"
              leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <DialogPanel
                class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6"
              >
                <div>
                  <div class="flex items-center justify-between border-b pb-4">
                    <div class="flex items-center">
                      <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-indigo-100">
                        <img
                          v-if="robot.imageUrl"
                          :src="robot.imageUrl"
                          :alt="robot.name"
                          class="h-10 w-10 rounded-full object-cover"
                        />
                        <IdentificationIcon v-else class="h-6 w-6 text-indigo-600" aria-hidden="true" />
                      </div>
                      <div class="mt-3 ml-3 text-center sm:text-left">
                        <DialogTitle as="h3" class="text-base font-semibold leading-6 text-gray-900">
                          {{ robot.name }}
                        </DialogTitle>
                        <div class="text-xs text-gray-500" :title="robot.id">ID: {{ robot.id }}</div>
                      </div>
                    </div>
                    
                    <div :class="[statusClasses[robot.status?.status || '未知'], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">
                      {{ robot.status?.status || '未知状态' }}
                    </div>
                  </div>
                  
                  <div class="mt-4">
                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">在线状态</div>
                      <div class="text-sm text-gray-900 flex items-center">
                        <span class="inline-block h-2 w-2 rounded-full mr-2" 
                          :class="robot.status?.isOnline ? 'bg-green-400' : 'bg-red-400'" />
                        {{ robot.status?.isOnline ? '在线' : '离线' }}
                      </div>
                    </div>
                    
                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">电量</div>
                      <div class="text-sm text-gray-900">
                        <div class="w-24 bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                          <div 
                            class="h-2.5 rounded-full" 
                            :class="batteryColorClass"
                            :style="`width: ${batteryPercentage}%`"
                          ></div>
                        </div>
                        <div class="text-xs mt-1 text-right">、
                          <span v-if="robot.status?.isCharging" class="text-xs text-gray-500">充电中</span>
                          {{ batteryPercentage }}%
                        </div>
                      </div>
                    </div>

                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">充电状态</div>
                      <div class="text-sm text-gray-900">

                        <div class="text-xs mt-1 text-right">{{ chargingStatusText.value }}</div>
                      </div>
                    </div>
                    
                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">货仓ID</div>
                      <div class="text-sm text-gray-900">{{ robot.cabinId || '未知' }}</div>
                    </div>

                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">位置</div>
                      <div class="text-sm text-gray-900">{{ robot.status?.location || '未知位置' }}</div>
                    </div>
                    
                    <div class="mt-2 flex justify-between border-b py-2">
                      <div class="text-sm font-medium text-gray-500">最近消息</div>
                      <div class="text-sm text-gray-900 max-w-xs truncate" :title="robot.status?.message">
                        {{ robot.status?.message || '无消息' }}
                      </div>
                    </div>
                    
                    <div class="mt-2 flex justify-between py-2">
                      <div class="text-sm font-medium text-gray-500">最近活动</div>
                      <div class="text-sm text-gray-900">{{ formatDate(robot.lastActivity) }}</div>
                    </div>
                  </div>
                </div>
                
                <div class="mt-5 sm:mt-6 flex justify-between">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    控制机器人
                  </button>
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                    @click="closeModal"
                  >
                    关闭
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue'
  import { IdentificationIcon } from '@heroicons/vue/24/outline'
  
  const props = defineProps({
    isOpen: Boolean,
    robot: {
      type: Object,
      default: () => ({
        id: '',
        name: '',
        imageUrl: '',
        status: {
          isOnline: false,
          power: 0,
          isCharging: false,
          status: '未知',
          message: '',
          location: ''
        },
        lastActivity: new Date()
      })
    }
  })
  
  const emit = defineEmits(['update:isOpen'])
  
  const statusClasses = {
    '空闲': 'text-green-700 bg-green-50 ring-green-600/20',
    '执行任务中': 'text-yellow-600 bg-yellow-50 ring-yellow-500/30',
    '未知': 'text-gray-600 bg-gray-50 ring-gray-500/10',
    '错误': 'text-red-700 bg-red-50 ring-red-600/10'
  }
  
  const batteryPercentage = computed(() => {
    const power = props.robot.status?.power || 0
    return typeof power === 'number' ? power : parseInt(power) || 0
  })

  const chargingStatusText = computed(() => {
  return props.robot.status.isCharging ? '正在充电' : '未充电'
})

  const batteryColorClass = computed(() => {
    if (batteryPercentage.value > 50) return 'bg-green-600'
    if (batteryPercentage.value > 20) return 'bg-yellow-300'
    return 'bg-red-600'
  })
  
  function closeModal() {
    emit('update:isOpen', false)
  }
  
  function formatDate(date) {
    if (!date) return '未知'
    
    try {
      const dateObj = new Date(date)
      return new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(dateObj)
    } catch (e) {
      return '无效日期'
    }
  }
  
  </script>