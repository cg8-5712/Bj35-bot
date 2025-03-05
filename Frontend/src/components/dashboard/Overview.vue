<template>
  <div>
    <LoadingSpinner v-if="loading" message="加载中..." />
    <div v-else>
      <!-- 如果 value 是一个对象或数组，可以使用更有意义的展示方式 -->
      <div v-if="Array.isArray(value) && value.length > 0" class="mt-4">
        <h2 class="text-xl font-bold mb-4">设备列表</h2>
        <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <li v-for="(device, index) in value" :key="index" class="bg-white p-4 rounded-lg shadow">
            <div class="font-semibold">{{ device.name || '未命名设备' }}</div>
            <div class="text-sm text-gray-500">ID: {{ device.id || '未知' }}</div>
            <div class="text-sm text-gray-500">状态: {{ device.status || '未知' }}</div>
          </li>
        </ul>
      </div>
      <div v-else-if="typeof value === 'object' && value !== null" class="mt-4">
        <pre class="bg-gray-100 p-4 rounded-lg overflow-auto text-sm">{{ JSON.stringify(value, null, 2) }}</pre>
      </div>
      <div v-else-if="Array.isArray(value) && value.length === 0" class="mt-4 text-center py-8">
        <p class="text-gray-500">暂无设备数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'

const value = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    const devices = await ApiServices.getAllDevices()
    value.value = devices
    console.log('设备数据:', devices)
  } catch (error) {
    console.error('获取设备列表失败:', error)
    NotificationService.notify('获取设备列表失败', 'error')
  } finally {
    loading.value = false
  }
})
</script>