import { ref, reactive } from 'vue'

// 创建响应式状态
const state = reactive({
  message: '',
  type: 'info',
  show: false
})

// 添加方法
const notify = (message, type = 'info') => {
  state.message = message
  state.type = type
  state.show = true

  // 自动隐藏（可选）
  setTimeout(() => {
    state.show = false
  }, 3000)
}

const close = () => {
  state.show = false
}

export default {
  state,
  notify,
  close
}