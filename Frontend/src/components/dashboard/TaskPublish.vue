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
            :disabled="!selectedRobot || !selectedRobot.status.isOnline"
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
                <!-- move 命令：教室选择 -->
                <div v-if="node.type === 'move'" class="grid grid-cols-1 gap-3">
                  <div>
                    <label class="block text-xs text-gray-500">教室</label>
                    <select
                      v-model="node.params.target"
                      class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      <option value="" disabled>选择教室</option>
                      <option v-for="(value, key) in classesList" :key="key" :value="key">
                        {{ value }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- back 命令：充电桩选择 -->
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
          :disabled="!canPublish"
        >
          发布任务
        </button>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue';
import { TransitionGroup } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import ApiServices from '@/services/ApiServices.js';
import NotificationService from '@/services/NotificationService.js';

import {
  ArrowUpIcon,
  ArrowDownIcon,
  TrashIcon
} from '@heroicons/vue/20/solid';

// 状态样式映射
const statusClasses = {
  '空闲': 'bg-green-50 text-green-700',
  '执行任务中': 'bg-yellow-50 text-yellow-600',
  '未知': 'bg-gray-50 text-gray-600',
  '错误': 'bg-red-50 text-red-700'
};

// 状态数据
const robots = ref([]);
const loading = ref(true);
const selectedRobot = ref(null);

// 任务节点
const taskNodes = ref([]);

// 教室列表
const classesList = ref({
  "B101": "B101",
  "B102": "B102",
  "B103": "B103",
  "B104": "B104",
  "B105": "B105",
  "B201": "B201",
  "B202": "B202",
  "B203": "B203",
  "B204": "B204",
  "B205": "B205",
  "B206": "B206",
  "B207": "B207",
  "B208": "B208",
  "B209": "B209",
  "B210": "B210",
  "B211": "B211",
  "B212": "B212",
  "B213": "B213",
  "B214": "B214",
  "B215": "B215",
  "B216": "B216",
  "B217": "B217",
  "B218": "B218",
  "B219": "B219",
  "B220": "B220",
  "B301": "B301",
  "B302": "B302",
  "B303": "B303",
  "B304": "B304",
  "B305": "B305",
  "B308": "B308",
  "B309": "B309",
  "B310": "B310",
  "B311": "B311",
  "B312": "B312",
  "B313": "B313",
  "B314": "B314",
  "B315": "B315",
  "B401": "B401",
  "B402": "B402",
  "B403": "B403",
  "C101": "C101",
  "C102": "C102",
  "C103": "C103",
  "C104": "C104",
  "C201": "C201",
  "C202": "C202",
  "C203": "C203",
  "C204": "C204",
  "C205": "C205",
  "C206": "C206",
  "C301": "C301",
  "C302": "C302",
  "C303": "C303",
  "C304": "C304",
  "C305": "C305",
  "C306": "C306",
  "Y101": "Y101",
  "Y102": "Y102",
  "Y103": "Y103",
  "Y201": "Y201",
  "Y202": "Y202",
  "Y203": "Y203",
  "Y204": "Y204",
  "Y301": "Y301",
  "Y302": "Y302",
  "Y303": "Y303",
  "Y401": "Y401",
  "Y402": "Y402",
  "Q101": "Q101",
  "Q103": "Q103",
  "Q201": "Q201",
  "Q202": "Q202",
  "Q203": "Q203",
  "Q205": "Q205",
  "Q301": "Q301",
  "Q302": "Q302",
  "Q304": "Q304",
  "Q401": "Q401",
  "S101": "S101",
  "S201": "S201",
  "S202": "S202",
  "S203": "S203",
  "S204": "S204",
  "S205": "S205",
  "S206": "S206",
  "S207": "S207",
  "S301": "S301",
  "S302": "S302",
  "S303": "S303",
  "S304": "S304",
  "S305": "S305",
  "S306": "S306",
  "S307": "S307",
  "S308": "S308",
  "S309": "S309",
  "S401": "S401",
  "S402": "S402",
  "S403": "S403",
  "S404": "S404",
  "S405": "S405",
  "S406": "S406",
  "S407": "S407",
  "S408": "S408",
  "S409": "S409",
  "一楼作业柜": "一楼作业柜",
  "二楼作业柜": "二楼作业柜",
  "三楼作业柜": "三楼作业柜"
});

// 获取状态样式类
function getStatusClass(status) {
  return statusClasses[status] || statusClasses['未知'];
}

// 获取电量颜色
function getBatteryColorClass(power) {
  if (power > 50) return 'bg-green-600';
  if (power > 20) return 'bg-yellow-600';
  return 'bg-red-600';
}

// 选择机器人
function selectRobot(robot) {
  selectedRobot.value = robot;
}

// 添加任务节点，默认类型为 move，新格式的参数结构
function addTaskNode() {
  taskNodes.value.push({
    id: uuidv4(),
    type: 'move',
    params: {
      target: ""
    }
  });
}

// 移除任务节点
function removeTaskNode(index) {
  taskNodes.value.splice(index, 1);
}

// 节点上移
function moveNodeUp(index) {
  if (index > 0) {
    const temp = taskNodes.value[index];
    taskNodes.value[index] = taskNodes.value[index - 1];
    taskNodes.value[index - 1] = temp;
  }
}

// 节点下移
function moveNodeDown(index) {
  if (index < taskNodes.value.length - 1) {
    const temp = taskNodes.value[index];
    taskNodes.value[index] = taskNodes.value[index + 1];
    taskNodes.value[index + 1] = temp;
  }
}

// 重置任务节点
function resetTaskNodes() {
  taskNodes.value = [];
}

// 根据任务节点类型切换，重置对应的参数数据
function updateNodeParams(node) {
  switch (node.type) {
    case 'move':
      node.params = { target: "" };
      break;
    case 'back':
      node.params = { charge_point: "" };
      break;
    default:
      node.params = {};
  }
}

// 判断是否可以发布任务
const canPublish = computed(() => {
  return selectedRobot.value &&
         selectedRobot.value.status.isOnline &&
         taskNodes.value.length > 0;
});

// 发布任务
async function publishTask() {
  if (!canPublish.value) {
    NotificationService.notify('无法发布任务，请检查机器人状态和任务配置', 'error');
    return;
  }

  try {
    // 将任务节点转换为位置列表
    const locations = taskNodes.value.map(node => {
      if (node.type === 'move') {
        return node.params.target;
      } else if (node.type === 'back') {
        return node.params.charge_point;
      }
      return null;
    }).filter(Boolean);

    // 调用新的RUN API
    const response = await ApiServices.post(`/run-task/${selectedRobot.value.id}`, {
      locations: locations
    });

    if (!response) {
      throw new Error('API响应为空');
    }

    if (response.code === 0) {
      NotificationService.notify('任务已成功发布', 'success');
      // 返回结果已经是list格式
      return response.data;
    } else {
      NotificationService.notify(`发布任务失败: ${response.message || '未知错误'}`, 'error');
      return [];
    }
  } catch (error) {
    console.error('发布任务失败:', error);
    NotificationService.notify(`发布任务失败: ${error.message || '未知错误'}`, 'error');
  }
}

// 获取所有设备
async function fetchRobots() {
  try {
    loading.value = true;
    
    // 调用API获取机器人列表
    const response = await ApiServices.get('/robot_list');
    
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
      }));
    } else {
      NotificationService.notify(`获取机器人列表失败: ${response.message}`, 'error');
      robots.value = [];
    }
  } catch (error) {
    console.error('获取机器人列表失败:', error);
    NotificationService.notify(`获取机器人列表失败: ${error.message || '未知错误'}`, 'error');
  } finally {
    loading.value = false;
  }
}

// 组件挂载时获取机器人列表
onMounted(() => {
  fetchRobots();
});
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
