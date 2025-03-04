<template>
  <div>
    <p>机器人ID: {{ robotIdValue }}</p>
    <p>机器人电量: {{ batteryLevel }}%</p>
    <p>机器人位置: X: {{ position.x }}, Y: {{ position.y }}, Z: {{ position.z }}</p>
    <p>机器人状态: {{ robotStatus }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { status } from "@/api/api.js";

const robotIdValue = ref('');
const batteryLevel = ref("");
const position = ref({
  x: 0,
  y: 0,
  z: 0
});
const robotStatus = ref("");

// 封装获取状态的函数
const fetchStatus = async () => {
  try {
    const data = await status();
    robotIdValue.value = data['data']['deviceInfo']['deviceId'];
    batteryLevel.value = data['data']['deviceStatus']['powerPercent'];
    position.value = data['data']['deviceStatus']['position']['orientation'];
    robotStatus.value = data['data']['deviceStatus']['isIdle'] === true ? "Idle" : "Busy";
  } catch (error) {
    console.error(error);
  }
};

// 在组件挂载时立即获取一次状态
onMounted(async () => {
  await fetchStatus();
  
  // 设置定时器定期更新状态
  setInterval(fetchStatus, 10000);
});
</script>

<style scoped>
/* Add your styles here */
</style>