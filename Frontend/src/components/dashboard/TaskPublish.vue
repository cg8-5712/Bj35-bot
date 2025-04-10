<template>
  <div class="task-publish-container">
    <!-- 页面标题 -->
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">发布新任务</h1>
      <p class="mt-1 text-sm text-gray-500">创建机器人任务序列并发送执行</p>
    </div>

    <!-- 机器人选择与状态部分 -->
    <div class="grid grid-cols-1 gap-6 mb-8 lg:grid-cols-3">
      <!-- 机器人选择 -->
      <div class="p-5 bg-white rounded-lg shadow">
        <h2 class="mb-4 text-lg font-medium text-gray-900">选择机器人</h2>

        <div v-if="loading" class="flex items-center justify-center py-4">
          <div class="w-5 h-5 border-2 border-t-transparent border-gray-500 rounded-full animate-spin"></div>
          <span class="ml-2 text-gray-500">加载机器人列表...</span>
        </div>

        <div v-else-if="!robots.length" class="py-4 text-center text-gray-500">
          没有可用的机器人
        </div>

        <div v-else class="space-y-2">
          <div
            v-for="robot in robots"
            :key="robot.id"
            :class="['flex items-center p-3 rounded-md cursor-pointer border hover:bg-gray-50',
              selectedRobot?.id === robot.id ? 'border-indigo-500 bg-indigo-50' : 'border-gray-200']"
            @click="selectRobot(robot)"
          >
            <div class="flex-shrink-0 p-2 rounded-full" :class="robot.status.isOnline ? 'bg-green-50' : 'bg-red-50'">
              <div class="w-3 h-3 rounded-full" :class="robot.status.isOnline ? 'bg-green-500' : 'bg-red-500'"></div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">{{ robot.name }}</p>
              <p class="text-xs text-gray-500">ID: {{ robot.id.substring(0, 8) }}...</p>
            </div>
            <div class="ml-auto text-xs px-2 py-1 rounded" :class="getStatusClass(robot.status.status)">
              {{ robot.status.status }}
            </div>
          </div>
        </div>
      </div>

      <!-- 机器人状态 -->
      <div class="p-5 bg-white rounded-lg shadow lg:col-span-2">
        <h2 class="mb-4 text-lg font-medium text-gray-900">机器人状态</h2>

        <div v-if="!selectedRobot" class="py-8 text-center text-gray-500">
          请先选择一个机器人
        </div>

        <div v-else class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 bg-gray-50 rounded-md">
              <p class="text-xs text-gray-500">当前位置</p>
              <p class="mt-1 text-sm font-medium">{{ selectedRobot.status.location || '未知' }}</p>
            </div>
            <div class="p-3 bg-gray-50 rounded-md">
              <p class="text-xs text-gray-500">电池电量</p>
              <div class="mt-1 flex items-center">
                <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full"
                    :class="getBatteryColorClass(selectedRobot.status.power)"
                    :style="{width: `${selectedRobot.status.power}%`}">
                  </div>
                </div>
                <span class="ml-2 text-sm font-medium">{{ selectedRobot.status.power }}%</span>
              </div>
            </div>
          </div>

          <div class="flex items-center">
            <span class="px-2 py-1 text-xs rounded"
                  :class="getStatusClass(selectedRobot.status.status)">
              {{ selectedRobot.status.status }}
            </span>
            <span class="ml-2 text-sm text-gray-500">{{ selectedRobot.status.message }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务创建部分 -->
    <div class="p-5 bg-white rounded-lg shadow mb-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-medium text-gray-900">创建任务流</h2>
        <div>
          <button
            class="px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            @click="addTaskNode"
          >
            添加任务节点
          </button>
        </div>
      </div>

      <!-- 任务流构建区域 -->
      <div class="mt-6 mb-4">
        <div v-if="!taskNodes.length" class="py-8 text-center text-gray-500 border-2 border-dashed border-gray-200 rounded-lg">
          尚未添加任务节点，点击"添加任务节点"按钮开始创建任务流
        </div>

        <TransitionGroup
          name="task-list"
          tag="div"
          class="space-y-3"
        >
          <div
            v-for="(node, index) in taskNodes"
            :key="node.id"
            class="flex items-start p-4 bg-gray-50 rounded-lg border border-gray-200"
          >
            <!-- 任务节点序号 -->
            <div class="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 font-medium">
              {{ index + 1 }}
            </div>

            <!-- 任务节点内容 -->
            <div class="ml-4 flex-grow">
              <div class="flex items-center mb-2">
                <select
                  v-model="node.type"
                  @change="updateNodeParams(node)"
                  class="block w-36 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                >
                  <option value="move">前往教室</option>
                  <option value="back">返回充电桩</option>
                  <option value="send">发送信息</option>
                </select>

                <button
                  @click="removeTaskNode(index)"
                  class="ml-3 text-red-600 hover:text-red-800"
                >
                  <span class="sr-only">删除</span>
                  <TrashIcon class="size-6" aria-hidden="true" />
                </button>

                <div class="ml-auto flex items-center">
                  <button
                    v-if="index > 0"
                    @click="moveNodeUp(index)"
                    class="text-gray-500 hover:text-gray-700"
                  >
                    <span class="sr-only">上移</span>
                    <ArrowUpIcon class="size-6" aria-hidden="true" />
                  </button>
                  <button
                    v-if="index < taskNodes.length - 1"
                    @click="moveNodeDown(index)"
                    class="ml-2 text-gray-500 hover:text-gray-700"
                  >
                    <span class="sr-only">下移</span>
                    <ArrowDownIcon class="size-6" aria-hidden="true" />
                  </button>
                </div>
              </div>

              <!-- 根据任务类型显示不同的参数 -->
              <div class="mt-2">
                <!-- move 命令：两个带搜索的下拉框(target, user) 和 一个输入框(message) -->
                <div v-if="node.type === 'move'" class="grid grid-cols-3 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">目标</label>
                    <input
                      v-model="node.params.target"
                      :list="`move-target-options-${node.id}`"
                      type="text"
                      placeholder="搜索目标"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`move-target-options-${node.id}`">
                      <option
                        v-for="(optionData, index) in targetOptions"
                        :key="index"
                        :value="optionData.value"
                      >
                        {{ optionData.label }}
                      </option>
                    </datalist>

                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">用户</label>
                    <input
                      v-model="node.params.user"
                      :list="`move-user-options-${node.id}`"
                      type="text"
                      placeholder="搜索用户"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`move-user-options-${node.id}`">
                      <option
                        v-for="option in userOptions"
                        :key="option.value"
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </datalist>
                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">消息</label>
                    <input
                      v-model="node.params.message"
                      type="text"
                      placeholder="输入消息"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>

                <!-- back 命令：下拉框选择充电桩 -->
                <div v-else-if="node.type === 'back'" class="grid grid-cols-1 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">充电桩</label>
                    <select
                      v-model="node.params.charge_point"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="" disabled>选择充电桩</option>
                      <option value="3F">3F</option>
                      <option value="1F">1F</option>
                    </select>
                  </div>
                </div>

                <!-- send 命令：带搜索下拉框(user) 和 输入框(message) -->
                <div v-else-if="node.type === 'send'" class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">用户</label>
                    <input
                      v-model="node.params.user"
                      :list="`send-user-options-${node.id}`"
                      type="text"
                      placeholder="搜索用户"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <datalist :id="`send-user-options-${node.id}`">
                      <option
                        v-for="option in userOptions"
                        :key="option.value"
                        :value="option.value"
                      >
                        {{ option.label }}
                      </option>
                    </datalist>
                  </div>
                  <div>
                    <label class="block text-xs text-gray-500">消息</label>
                    <input
                      v-model="node.params.message"
                      type="text"
                      placeholder="输入消息"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>
                </div>

                <!-- 如果需要扩展其他任务类型，可在此添加 -->
                <div v-else class="mt-2">
                  <p class="text-sm text-gray-600">请配置任务参数</p>
                </div>
              </div>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <!-- 提交按钮 -->
      <div class="flex justify-end space-x-3 mt-6">
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="resetTaskNodes"
        >
          重置
        </button>
        <button
          class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="publishTask"
        >
          发布任务
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { TransitionGroup } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import ApiServices from '@/services/ApiServices'
import NotificationService from '@/services/NotificationService'

import {
  ArrowUpIcon,
  ArrowDownIcon,
  TrashIcon
} from '@heroicons/vue/20/solid'

// 定义组件的 props
const props = defineProps({
  isOpen: Boolean,
  robot: {
    type: Object,
    default: () => ({})
  }
})

// 状态样式映射
const statusClasses = {
  '空闲': 'bg-green-50 text-text-700',
  '执行任务中': 'bg-yellow-50 text-yellow-600',
  '未知': 'bg-gray-50 text-gray-600',
  '错误': 'bg-red-50 text-red-700'
}

// 状态数据
const robots = ref([])
const loading = ref(true)
const selectedRobot = ref(null)

// 任务节点
const taskNodes = ref([])

// 教室列表
const targetOptions = ref([])

const fetchTargets = async () => {
  try {
    const data = await ApiServices.getTargetlist()
    // 假设 data 是数组格式
    targetOptions.value = data
    // 可选：打印结果确认赋值
    console.log(targetOptions.value)
  } catch (error) {
    console.error('获取任务数据失败:', error)
  } finally {
    loading.value = false
  }
}

const userOptions = ref([
  { value: '用户1', label: '用户1' },
  { value: '用户2', label: '用户2' },
  { value: '用户3', label: '用户3' }
])

// 获取状态样式类
function getStatusClass(status) {
  return statusClasses[status] || statusClasses['未知']
}

// 获取电量颜色
function getBatteryColorClass(power) {
  if (power > 50) return 'bg-green-600'
  if (power > 20) return 'bg-yellow-600'
  return 'bg-red-600'
}

// 选择机器人
function selectRobot(robot) {
  selectedRobot.value = robot
}

// 添加任务节点，默认类型为 move，新格式的参数结构
function addTaskNode() {
  console.log(selectedRobot.value)
  if (!selectedRobot.value) {
    showNotification('请先选择一个机器人', 'warning')
    return
  }
  taskNodes.value.push({
    id: uuidv4(),
    type: 'move',
    params: {
      target: '',
      user: '',
      message: ''
    }
  })
}

// 移除任务节点
function removeTaskNode(index) {
  taskNodes.value.splice(index, 1)
}

// 节点上移
function moveNodeUp(index) {
  if (index > 0) {
    const temp = taskNodes.value[index]
    taskNodes.value[index] = taskNodes.value[index - 1]
    taskNodes.value[index - 1] = temp
  }
}

// 节点下移
function moveNodeDown(index) {
  if (index < taskNodes.value.length - 1) {
    const temp = taskNodes.value[index]
    taskNodes.value[index] = taskNodes.value[index + 1]
    taskNodes.value[index + 1] = temp
  }
}

// 重置任务节点
function resetTaskNodes() {
  taskNodes.value = []
}

// 根据任务节点类型切换，重置对应的参数数据
function updateNodeParams(node) {
  switch (node.type) {
    case 'move':
      node.params = { target: '', user: '', message: '' }
      break
    case 'back':
      node.params = { charge_point: '' }
      break
    case 'send':
      node.params = { user: '', message: '' }
      break
    default:
      node.params = {}
  }
}

// 判断是否可以发布任务
const canPublish = computed(() => {
  return selectedRobot.value &&
         selectedRobot.value.status.isOnline &&
         taskNodes.value.length > 0
})

// 发布任务
async function publishTask() {
  if (!canPublish.value) {
    NotificationService.notify('无法发布任务，请检查机器人状态和任务配置', 'error')
    return
  }

  try {
    // 处理所有任务节点
    for (const node of taskNodes.value) {
      if (node.type === 'send') {
        // 发送消息节点
        if (!node.params.user || !node.params.message) {
          NotificationService.notify('发送消息需要指定用户和消息内容', 'warning')
          continue
        }

        try {
          await ApiServices.sendMessage(node.params.message, node.params.user)
          NotificationService.notify(`消息已发送给 ${node.params.user}`, 'success')
        } catch (error) {
          NotificationService.notify(`发送消息失败: ${error.message}`, 'error')
        }
      }
    }

    // 将移动任务节点转换为位置列表
    const locations = taskNodes.value
      .filter(node => ['move', 'back'].includes(node.type))
      .map(node => {
        if (node.type === 'move') {
          return node.params.target
        } else if (node.type === 'back') {
          return node.params.charge_point
        }
        return null
      })
      .filter(Boolean)

    // 如果有移动任务，调用RUN API
    if (locations.length > 0) {
      NotificationService.notify('任务已发布！', 'info');
      const response = await ApiServices.post(`/run-task/${selectedRobot.value.id}`, {
        locations: locations
      })

      if (!response) {
        throw new Error('API响应为空')
      }

      if (response.code === 0) {
        NotificationService.notify('任务已执行成功', 'success')
        return response.data
      } else {
        throw new Error(response.message || '未知错误')
      }
    }

    NotificationService.notify('所有任务已处理完成', 'info')
    return []
  } catch (error) {
    console.error('发布任务失败:', error)
    NotificationService.notify(`发布任务失败: ${error.message || '未知错误'}`, 'error')
  }
}

// 获取所有设备
async function fetchRobots() {
  try {
    loading.value = true

    // 调用API获取机器人列表
    const response = await ApiServices.get('/robot_list')

    if (response.code === 0) {
      // 格式化数据以匹配前端结构
      robots.value = response.data.map(robot => ({
        id: robot.deviceId,
        name: robot.name,
        imageUrl: robot.imageUrl || '',
        status: {
          isOnline: robot.status.isOnline,
          power: robot.status.power,
          message: robot.status.message,
          status: robot.status.status,
          location: robot.status.location
        }
      }))
    } else {
      NotificationService.notify(`获取机器人列表失败: ${response.message}`, 'error')
      robots.value = []
    }
  } catch (error) {
    console.error('获取机器人列表失败:', error)
    NotificationService.notify(`获取机器人列表失败: ${error.message || '未知错误'}`, 'error')
  } finally {
    loading.value = false
  }
}

// 提示方法
function showNotification(message, type) {
  NotificationService.notify(message, type)
}

// 组件挂载时获取机器人列表
onMounted(() => {
  fetchRobots()
  fetchTargets()
})

// 监听传递的机器人信息并设置为选中的机器人
watch(
  () => props.robot,
  (newRobot) => {
    console.log('[Watch] props.robot changed:', newRobot)
    if (newRobot && newRobot.cabinId) {
      // 封装绑定逻辑
      const bindRobot = () => {
        console.log('[bindRobot] robots array:', robots.value)
        const matchedRobot = robots.value.find(r => r.id === newRobot.id)
        if (matchedRobot) {
          console.log('[bindRobot] Matched robot found:', matchedRobot)
        } else {
          console.log('[bindRobot] No matching robot found, using newRobot:', newRobot)
        }
        selectedRobot.value = matchedRobot || newRobot
        if (taskNodes.value.length === 0) {
          console.log('[bindRobot] taskNodes empty, adding default task node')
          addTaskNode()
        }
      }

      // 定义等待 robots 数组加载的函数，每隔 500 毫秒检查一次
      const waitForRobots = () => {
        console.log('[waitForRobots] robots.length:', robots.value.length)
        if (robots.value.length > 0) {
          console.log('[waitForRobots] robots list loaded, proceeding to bind')
          bindRobot()
        } else {
          console.log('[waitForRobots] robots not loaded yet, retrying in 500ms...')
          setTimeout(waitForRobots, 500)
        }
      }

      if (robots.value.length === 0) {
        console.log('[Watch] robots array is empty at the moment, starting waitForRobots()')
        waitForRobots()
      } else {
        console.log('[Watch] robots array already loaded')
        bindRobot()
      }
    }
  },
  { immediate: true }
)

</script>


<style scoped>
.task-list-move,
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.5s ease;
}

.task-list-enter-from,
.task-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.task-list-leave-active {
  position: absolute;
}
</style>