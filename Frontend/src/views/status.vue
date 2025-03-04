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

:root {
  font-family: system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #1a1a1a;
  cursor: pointer;
  transition: border-color 0.25s;
}
button:hover {
  border-color: #646cff;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

.card {
  padding: 2em;
}

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
  a:hover {
    color: #747bff;
  }
  button {
    background-color: #f9f9f9;
  }
}


.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>