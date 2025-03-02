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
import { robotId, powerPercent } from "@/api/api.js";

const robotIdValue = ref('');
const batteryLevel = ref("");
const position = ref({
  x: 0,
  y: 0,
  z: 0
});
const robotStatus = ref("Idle");

onMounted(async () => {
  try {
    const botid = await robotId();
    robotIdValue.value = botid;
    const power = await powerPercent();
    batteryLevel.value = power;
  } catch (error) {
    console.error(error);
  }
});
</script>

<style scoped>
/* 你的样式代码 */
</style>
