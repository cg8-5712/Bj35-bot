<template>
  <div class="p-4">
    <!-- 标题与说明 -->
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">任务看板</h1>
      <p class="mt-1 text-sm text-gray-500">点击查看详细信息</p>
    </div>

    <!-- 加载中状态 -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="text-gray-500">加载中...</div>
    </div>

    <!-- 数据展示 -->
    <div v-else>
      <!-- 每页展示条数选择 -->
      <div class="mb-4 flex justify-end items-center">
        <label class="mr-2 text-sm text-gray-700">每页显示</label>
        <select v-model.number="pageSize" class="border border-gray-300 rounded-md p-1">
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
      </div>

      <!-- 任务列表表格 -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">任务 NO</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">创建时间</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">目标</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="task in pagedTasks"
              :key="task.no"
              class="cursor-pointer hover:bg-gray-100"
              @click="openTaskDetail(task)"
            >

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ task.no }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatTime(task.createdAt) }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div :class="[statuses[task.status], 'rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset']">{{ task.status }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ task.target }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页控件，集成了移动端和桌面端样式 -->
      <div class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 mt-4">
        <!-- 移动端视图 -->
        <div class="flex flex-1 justify-between sm:hidden">
          <button
            @click="prevPage"
            :disabled="currentPage === 1"
            class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Previous
          </button>
          <button
            @click="nextPage"
            :disabled="currentPage === totalPages"
            class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Next
          </button>
        </div>
        <!-- 桌面端视图 -->
        <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing
              <span class="font-medium">{{ firstItem }}</span>
              to
              <span class="font-medium">{{ lastItem }}</span>
              of
              <span class="font-medium">{{ totalResults }}</span>
              results
            </p>
          </div>
          <div>
            <nav class="isolate inline-flex -space-x-px rounded-md shadow-xs" aria-label="Pagination">
              <button
                @click="prevPage"
                :disabled="currentPage === 1"
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
              >
                <span class="sr-only">Previous</span>
                <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
              </button>
              <template v-for="page in pages" :key="page">
                <template v-if="page === '...'">
                  <span class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-700 ring-1 ring-gray-300 ring-inset">
                    ...
                  </span>
                </template>
                <template v-else>
                  <button
                    @click="setPage(page)"
                    :aria-current="page === currentPage ? 'page' : null"
                    :class="page === currentPage ? 'relative z-10 inline-flex items-center bg-indigo-600 px-4 py-2 text-sm font-semibold text-white focus:z-20 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600' : 'relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0'"
                  >
                    {{ page }}
                  </button>
                </template>
              </template>
              <button
                @click="nextPage"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-gray-300 ring-inset hover:bg-gray-50 focus:z-20 focus:outline-offset-0"
              >
                <span class="sr-only">Next</span>
                <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <transition name="fade">
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
      >
        <div class="bg-white rounded-lg shadow-lg p-6 w-96">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-900">任务详情</h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">&times;</button>
          </div>
          <div class="space-y-2 text-sm text-gray-800">
            <div><span class="font-medium">任务 NO:</span> {{ selectedTask.no }}</div>
            <div><span class="font-medium">Task ID:</span> {{ selectedTask.taskId }}</div>
            <div><span class="font-medium">Out Task ID:</span> {{ selectedTask.outTaskId }}</div>
            <div>
              <span class="font-medium">创建时间:</span>
              {{ formatTime(selectedTask.createdAt) }}
            </div>
            <div>
              <span class="font-medium">更新时间:</span>
              {{ formatTime(selectedTask.updatedAt) }}
            </div>
            <div><span class="font-medium">状态:</span> {{ selectedTask.status }}</div>
            <div><span class="font-medium">任务类型:</span> {{ selectedTask.taskType }}</div>
            <div><span class="font-medium">目标:</span> {{ selectedTask.target }}</div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ApiServices from '@/services/ApiServices'
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/20/solid'

const statuses = {
  'SUCCESS': 'text-green-700 bg-green-50 ring-green-600/20 max-w-[70px]',
  'FAILED': 'text-red-700 bg-red-50 ring-red-600/10 max-w-[55px]',
  'CREATED': 'text-yellow-600 bg-yellow-50 ring-yellow-500/30 max-w-[70px]'
}

// Initial data
const tasks = ref([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = ref(10)
const showModal = ref(false)
const selectedTask = ref({})

// 获取模拟数据（可扩展以测试分页）
const fetchTasks = async () => {
  try {
    const Data = await ApiServices.getTasklist()
    tasks.value = Data
    console.log('获取任务数据成功:', Data)
  } catch (error) {
    console.error('获取任务数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTasks()
})

// 分页相关计算
const totalPages = computed(() => Math.ceil(tasks.value.length / pageSize.value) || 1)
const pagedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return tasks.value.slice(start, start + pageSize.value)
})
const firstItem = computed(() => (tasks.value.length === 0 ? 0 : (currentPage.value - 1) * pageSize.value + 1))
const lastItem = computed(() => Math.min(currentPage.value * pageSize.value, tasks.value.length))
const totalResults = computed(() => tasks.value.length)

// 简单的分页页码算法，若页码较多时自动显示省略号
const pages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  if (current <= 4) {
    return [1, 2, 3, 4, 5, '...', total]
  } else if (current > total - 4) {
    return [1, '...', total - 4, total - 3, total - 2, total - 1, total]
  } else {
    return [1, '...', current - 1, current, current + 1, '...', total]
  }
})

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
const setPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

// 详情弹窗控制
const openTaskDetail = (task) => {
  selectedTask.value = task
  showModal.value = true
}
const closeModal = () => {
  showModal.value = false
}
const formatTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp).toLocaleString()
}

watch(pageSize, () => {
  currentPage.value = 1
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
