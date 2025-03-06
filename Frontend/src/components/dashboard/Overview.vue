<template>
  <div>
    <LoadingSpinner v-if="loading" message="加载中..." />
    <div v-else>
      <div v-if="typeof value === 'object'" class="mt-4">
        <h2 class="text-xl font-bold mb-4">设备列表</h2>
        <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <li v-for="(group, key) in groupedDevices" :key="key" class="bg-white p-4 rounded-lg shadow">
            <ul>
              <li v-for="device in group" :key="device.deviceId" class="my-2">
                <div class="font-semibold">设备名称: {{ device.productName || '未命名设备' }}</div>
                <div class="text-sm text-gray-500">ID： {{ device.deviceId || '未知' }}</div>
              </li>
            </ul>
          </li>
        </ul>
      </div>
      <div v-else-if="Array.isArray(value) && value.length === 0" class="mt-4 text-center py-8">
        <p class="text-gray-500">暂无设备数据</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'

const value = ref('')
const loading = ref(true)

onMounted(async () => {
  try {
    const devices = await ApiServices.getAllDevices()
    value.value = devices

    console.log('设备数据:', devices)
    console.log('设备数据类型:', typeof devices)
  } catch (error) {
    console.error('获取设备列表失败:', error)
    NotificationService.notify('获取设备列表失败', 'error')
  } finally {
    loading.value = false
  }
})

const groupedDevices = computed(() => {
  const grouped = {}
  if (Array.isArray(value.value.data)) {
    value.value.data.forEach(device => {
      const prefix = device.deviceId.substring(0, 7)
      if (!grouped[prefix]) {
        grouped[prefix] = []
      }
      grouped[prefix].push(device)
    })
  }
  return grouped
})
</script>
