<!--
 * @fileoverview App.vue - 应用主组件
 * @copyright Copyright (c) 2020-2025 The ESAP Project.
 * @author AptS:1547 <esaps@esaps.net>
 * @Link https://esaps.net/
 * @version 0.1.0
 * @license
 * 使用本代码需遵循 MIT 协议，以及 Tailwind Plus Personal 许可证
-->

<script setup>
  import { RouterView } from 'vue-router'
  import MessageInfo from '@/components/common/MessageInfo.vue'
</script>

<template>
  <MessageInfo />
  <RouterView />
</template>
