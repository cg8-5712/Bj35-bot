<template>
  <div>
    <MessageInfo ref="messageInfo" />
    <div class="m-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="m-auto max-w-3xl">
        <p>机器人ID: {{ robotIdValue }}</p>
        <p>机器人电量: {{ batteryLevel }}%</p>
        <p>机器人位置: X: {{ position.x }}, Y: {{ position.y }}, Z: {{ position.z }}</p>
        <p>机器人状态: {{ robotStatus }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { status } from "@/api/api.js";

import MessageInfo from "@/components/MessageInfo.vue"
const messageInfo = ref(null)

const robotIdValue = ref('');
const batteryLevel = ref("");
const position = ref({
  x: 0,
  y: 0,
  z: 0
});
const robotStatus = ref("");
const intervalId = ref(null);

const fetchStatus = async () => {
  try {
    const data = await status();

    if ( data === null || data === undefined || data['data'] === undefined) {
      messageInfo.value.setMessage('获取失败：网络错误', 'error')
      return;
    }

    robotIdValue.value = data['data']['deviceInfo']['deviceId'];
    batteryLevel.value = data['data']['deviceStatus']['powerPercent'];
    position.value = data['data']['deviceStatus']['position']['orientation'];
    robotStatus.value = data['data']['deviceStatus']['isIdle'] === true ? "Idle" : "Busy";
    messageInfo.value.closeNotification();

  } catch (error) {
    messageInfo.value.setMessage('获取失败', 'error')
  }
};

onMounted(async () => {
  await fetchStatus();

  intervalId.value = setInterval(fetchStatus, 10000);
});

onBeforeUnmount(() => {
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
});

</script>
