<template>
  <div class="max-w-xl mx-auto bg-white shadow rounded p-6">
    <h2 class="text-xl font-bold mb-4">修改密码</h2>
    <div class="mb-4">
      <label class="block mb-2 text-gray-700 font-medium">旧密码</label>
      <input
        type="password"
        v-model="oldPassword"
        class="border rounded w-full px-3 py-2"
      />
    </div>
    <div class="mb-4">
      <label class="block mb-2 text-gray-700 font-medium">新密码</label>
      <input
        type="password"
        v-model="newPassword"
        class="border rounded w-full px-3 py-2"
      />
    </div>
    <div class="mb-4">
      <label class="block mb-2 text-gray-700 font-medium">确认新密码</label>
      <input
        type="password"
        v-model="confirmPassword"
        class="border rounded w-full px-3 py-2"
      />
    </div>
    <button
      class="bg-blue-600 text-white px-4 py-2 rounded"
      @click="changePassword"
    >
      提交
    </button>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'ProfilePassword',
  setup() {
    const oldPassword = ref('')
    const newPassword = ref('')
    const confirmPassword = ref('')

    const changePassword = async () => {
      if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
        alert('请完整填写表单')
        return
      }
      if (newPassword.value !== confirmPassword.value) {
        alert('两次新密码输入不一致')
        return
      }
      try {
        // 示例：POST /api/changePassword
        await axios.post('/api/changePassword', {
          oldPassword: oldPassword.value,
          newPassword: newPassword.value
        })
        alert('密码修改成功')
        oldPassword.value = ''
        newPassword.value = ''
        confirmPassword.value = ''
      } catch (error) {
        alert('修改密码失败，请重试')
        console.error('Change Password Error:', error)
      }
    }

    return {
      oldPassword,
      newPassword,
      confirmPassword,
      changePassword
    }
  }
}
</script>
