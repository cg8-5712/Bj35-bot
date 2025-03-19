<template>
  <div class="max-w-xl mx-auto bg-white shadow rounded p-6">
    <h2 class="text-xl font-bold mb-4">修改信息</h2>

    <!-- 输入密码验证 -->
    <div v-if="!verified" class="mb-4">
      <label class="block mb-2 text-gray-700 font-medium">请输入密码进行验证</label>
      <input
        type="password"
        v-model="password"
        class="border rounded w-full px-3 py-2 mb-2"
        placeholder="当前密码"
      />
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded"
        @click="verifyPassword"
      >
        验证
      </button>
    </div>

    <!-- 已验证，可以修改 -->
    <div v-else>
      <div class="mb-4">
        <label class="block mb-2 text-gray-700 font-medium">姓名</label>
        <input
          type="text"
          v-model="editForm.name"
          class="border rounded w-full px-3 py-2"
        />
      </div>
      <div class="mb-4">
        <label class="block mb-2 text-gray-700 font-medium">常驻教室</label>
        <input
          type="text"
          v-model="editForm.classroom"
          class="border rounded w-full px-3 py-2"
        />
      </div>
      <div class="mb-4">
        <label class="block mb-2 text-gray-700 font-medium">企业微信账号</label>
        <input
          type="text"
          v-model="editForm.wechat"
          class="border rounded w-full px-3 py-2"
        />
      </div>
      <div class="mb-4">
        <label class="block mb-2 text-gray-700 font-medium">头像 URL</label>
        <input
          type="text"
          v-model="editForm.avatar"
          class="border rounded w-full px-3 py-2"
        />
      </div>
      <button
        class="bg-green-600 text-white px-4 py-2 rounded"
        @click="submitEdit"
      >
        保存修改
      </button>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ProfileEdit',
  setup() {
    const verified = ref(false)
    const password = ref('')

    // 用于编辑的表单
    const editForm = reactive({
      name: '',
      classroom: '',
      wechat: '',
      avatar: ''
    })

    const fetchUserInfo = async () => {
      try {
        const res = await axios.get('/api/user')
        editForm.name = res.data.name
        editForm.classroom = res.data.classroom
        editForm.wechat = res.data.wechat
        editForm.avatar = res.data.avatar
      } catch (error) {
        console.error('Failed to fetch user info:', error)
      }
    }

    const verifyPassword = async () => {
      try {
        // 示例：POST /api/verifyPassword, body: { password }
        await axios.post('/api/verifyPassword', { password: password.value })
        verified.value = true
      } catch (error) {
        alert('密码验证失败，请重试')
        console.error('Verify Password Error:', error)
      }
    }

    const submitEdit = async () => {
      try {
        // 示例：PUT /api/user
        await axios.put('/api/user', {
          name: editForm.name,
          classroom: editForm.classroom,
          wechat: editForm.wechat,
          avatar: editForm.avatar
        })
        alert('修改成功')
        // 修改成功后，可刷新或跳转
      } catch (error) {
        alert('修改失败，请重试')
        console.error('Submit Edit Error:', error)
      }
    }

    onMounted(() => {
      fetchUserInfo()
    })

    return {
      verified,
      password,
      editForm,
      verifyPassword,
      submitEdit
    }
  }
}
</script>
