<template>
  <div class="task-publish-container">
    <!-- 页面标题 -->
    <div class="mb-5">
      <h1 class="text-2xl font-semibold text-gray-900">发布任务</h1>
      <p class="mt-1 text-sm text-gray-500">发布单个机器人任务</p>
    </div>

    <!-- 任务发布部分 -->
    <div class="p-5 bg-white rounded-lg shadow mb-6">
      <div class="space-y-4">
        <!-- 教室选择 -->
        <div>
          <label class="block text-xs text-gray-500">教室</label>
          <select
            v-model="selectedClassroom"
            class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="" disabled>选择教室</option>
            <option v-for="(value, key) in classesList" :key="key" :value="key">
              {{ value }}
            </option>
          </select>
        </div>

        <!-- 充电桩选择 -->
        <div>
          <label class="block text-xs text-gray-500">充电桩</label>
          <select
            v-model="chargePoint"
            class="block w-full mt-1 px-3 py-2 text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          >
            <option value="" disabled>选择充电桩</option>
            <option value="3F">3F</option>
            <option value="1F">1F</option>
          </select>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="flex justify-end space-x-3 mt-6">
        <button
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          @click="resetForm"
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
// import ApiServices from '@/services/ApiServices';
import NotificationService from '@/services/NotificationService';

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
      target: "",
      user: "",
      message: ""
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
      node.params = { target: "", user: "", message: "" };
      break;
    case 'back':
      node.params = { charge_point: "" };
      break;
    case 'send':
      node.params = { user: "", message: "" };
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
    // Make a task list for return
    const taskData = {
      deviceId: selectedRobot.value.id,
      taskName: `Task-${Date.now()}`,
      nodes: taskNodes.value.map(node => ({
        type: node.type,
        params: node.params
      }))
    };

    // 转换任务节点为API需要的格式
    const apiTasks = taskData.nodes.map(node => {
      if (node.type === 'back') {
        return {
          type: 'dock_cabin_and_move_target_with_wait_action',
          params: {
            dockCabinId: taskData.deviceId,
            target: node.params.charge_point,
            overtime: 200,
            overtimeEvent: 'back'
          }
        }
      } else if (node.type === 'move') {
        return {
          type: 'dock_cabin_and_move_target_with_wait_action',
          params: {
            dockCabinId: taskData.deviceId,
            target: node.params.target,
            overtime: 200,
            overtimeEvent: 'back'
          }
        }
      }
      return null;
    }).filter(Boolean);

    // 调用API发布任务
    try {
      const response = await ApiServices.post('/task/docking-cabin-move', {
        deviceId: taskData.deviceId,
        tasks: apiTasks
      });

      if (response.code === 0) {
        NotificationService.notify('任务已成功发布', 'success');
      } else {
        NotificationService.notify(`发布任务失败: ${response.message}`, 'error');
      }
    } catch (error) {
      NotificationService.notify(`发布任务失败: ${error.message || '未知错误'}`, 'error');
    } finally {
      resetTaskNodes(); // 重置任务节点
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
    // 这里预留API调用代码

    // mock 数据
    const mockRobots = [
      {
        id: 'robot-001-abcd',
        name: 'Robot-001',
        imageUrl: '',
        status: {
          isOnline: true,
          power: 85,
          message: '系统正常',
          status: '空闲',
          location: '区域A-01'
        }
      },
      {
        id: 'robot-002-efgh',
        name: 'Robot-002',
        imageUrl: '',
        status: {
          isOnline: true,
          power: 42,
          message: '执行任务中',
          status: '执行任务中',
          location: '区域B-03'
        }
      },
      {
        id: 'robot-003-ijkl',
        name: 'Robot-003',
        imageUrl: '',
        status: {
          isOnline: false,
          power: 15,
          message: '连接断开',
          status: '错误',
          location: '未知位置'
        }
      }
    ];

    robots.value = mockRobots;
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
