import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import LoadingSpinner from './components/common/LoadingSpinner.vue'

const app = createApp(App)

app.component('LoadingSpinner', LoadingSpinner)

app.use(router)
app.mount('#app')