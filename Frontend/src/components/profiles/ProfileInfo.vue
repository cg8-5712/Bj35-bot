<template>
  <div class="max-w-xl mx-auto bg-white shadow rounded p-6">
    <h2 class="text-xl font-bold mb-4">用户信息</h2>
    <div class="flex items-center mb-4">
      <img
        v-if="user.avatar"
        :src="user.avatar"
        alt="头像"
        class="w-16 h-16 rounded-full mr-4"
      />
      <div v-else class="w-16 h-16 rounded-full mr-4 bg-gray-200 flex items-center justify-center text-gray-500">
        无头像
      </div>
      <div>
        <p class="text-gray-700"><strong>姓名：</strong>{{ user.name }}</p>
        <p class="text-gray-700"><strong>常驻教室：</strong>{{ user.classroom }}</p>
        <p class="text-gray-700"><strong>企业微信账号：</strong>{{ user.wechat }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ProfileInfo',
  setup() {
    const user = ref({ avatar: '', name: '', classroom: '', wechat: '' })

    const fetchUserInfo = async () => {
      try {
        const res = await axios.get('/api/user')
        user.value = res.data
      } catch (error) {
        console.error('Failed to fetch user info:', error)
      }
    }

    onMounted(() => {
      fetchUserInfo()
    })

    return { user }
  }
}
</script>
