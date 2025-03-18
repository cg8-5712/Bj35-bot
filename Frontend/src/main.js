import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import LoadingSpinner from './components/common/LoadingSpinner.vue'
import { createI18n } from 'vue-i18n'

// 配置国际化信息
const messages = {
  en: {
    message: {
      hello: 'Hello World',
      switch: 'Switch Language'
    }
  },
  zh: {
    message: {
      hello: '你好，世界',
      switch: '切换语言'
    }
  }
}

// 创建 i18n 实例，**关闭 legacy 模式**
const i18n = createI18n({
  legacy: false, // 关键点：使用 Vue 3 方式
  locale: 'en',  // 默认语言
  fallbackLocale: 'en',
  globalInjection: true, // 允许直接使用 $t()
  messages
})

const app = createApp(App)

app.component('LoadingSpinner', LoadingSpinner)

app.use(router)
app.use(i18n) // 安装 i18n

app.mount('#app')
