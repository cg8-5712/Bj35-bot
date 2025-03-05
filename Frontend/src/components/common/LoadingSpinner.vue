<template>
    <div class="text-center py-4">
      <div 
        class="inline-block animate-spin rounded-full border-4" 
        :class="[
          `h-${size} w-${size}`,
          borderColorClass
        ]"
      ></div>
      <p v-if="message" class="mt-2 text-gray-600">{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  const props = defineProps({
    size: {
      type: [String, Number],
      default: 8
    },
    color: {
      type: String,
      default: 'blue'
    },
    message: {
      type: String,
      default: '加载中...'
    }
  });
  
  const borderColorClass = computed(() => {
    const colorMap = {
      blue: 'border-t-blue-500 border-r-transparent border-b-blue-500 border-l-transparent',
      green: 'border-t-green-500 border-r-transparent border-b-green-500 border-l-transparent',
      red: 'border-t-red-500 border-r-transparent border-b-red-500 border-l-transparent',
      yellow: 'border-t-yellow-500 border-r-transparent border-b-yellow-500 border-l-transparent',
      purple: 'border-t-purple-500 border-r-transparent border-b-purple-500 border-l-transparent',
      indigo: 'border-t-indigo-500 border-r-transparent border-b-indigo-500 border-l-transparent',
      gray: 'border-t-gray-500 border-r-transparent border-b-gray-500 border-l-transparent',
    };
    
    return colorMap[props.color] || colorMap.blue;
  });
</script>