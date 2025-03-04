<template>
  <div>
    <MessageInfo ref="messageInfo" />
    <div class="m-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="m-auto max-w-3xl">
        <p>JWT: {{ jwt }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { login_post } from "@/api/api.js";

import MessageInfo from "@/components/MessageInfo.vue"
const messageInfo = ref(null)
const jwt = ref(null)

onMounted(async () => {
  const response = await login_post("test", "test", true);
  jwt.value = response.data;
});
</script>