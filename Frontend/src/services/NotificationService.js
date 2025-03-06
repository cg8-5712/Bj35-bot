import { ref, reactive } from 'vue'

const state = reactive({
  message: '',
  type: 'info',
  show: false
})

let hideTimeout = null

const notify = (message, type = 'info') => {

  if (hideTimeout !== null) {
    clearTimeout(hideTimeout)
    hideTimeout = null
  }

  state.message = message
  state.type = type
  state.show = true

  hideTimeout = setTimeout(() => {
    state.show = false
    hideTimeout = null
  }, 3000)
}

const close = () => {
  if (hideTimeout !== null) {
    clearTimeout(hideTimeout)
    hideTimeout = null
  }

  state.show = false
}

export default {
  state,
  notify,
  close
}