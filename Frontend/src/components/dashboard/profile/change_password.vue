<!-- /profile/change_password.vue -->
<template>
  <div class="max-w-7xl lg:px-16 pt-16">
    <h1 class="sr-only">Change Password</h1>
    <main class="px-4 py-16 sm:px-0 lg:px-0 lg:py-20">
      <div class="mx-auto max-w-2xl space-y-16 sm:space-y-20">
        <div>
          <h2 class="text-base font-semibold text-gray-900">Change Password</h2>
          <form @submit.prevent="changePassword">
            <div class="mt-6 divide-y divide-gray-100 border-t border-gray-200 text-sm">
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">Current Password</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <input
                    type="password"
                    v-model="currentPassword"
                    class="border border-gray-300 rounded p-1 flex-1"
                    required
                  />
                </dd>
              </div>
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">New Password</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <input
                    type="password"
                    v-model="newPassword"
                    class="border border-gray-300 rounded p-1 flex-1"
                    required
                  />
                </dd>
              </div>
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">Confirm New Password</dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <input
                    type="password"
                    v-model="confirmNewPassword"
                    class="border border-gray-300 rounded p-1 flex-1"
                    required
                  />
                </dd>
              </div>
              <div class="py-6 sm:flex">
                <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6"></dt>
                <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                  <button type="submit" class="px-4 py-2 bg-indigo-600 text-white rounded">Change Password</button>
                </dd>
              </div>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AuthService from '@/services/AuthService.js'
import ApiServices from "@/services/ApiServices.js"
import { useRouter } from 'vue-router'

const router = useRouter()

const currentPassword = ref('')
const newPassword = ref('')
const confirmNewPassword = ref('')

async function changePassword() {
  if (newPassword.value !== confirmNewPassword.value) {
    alert("New password and confirm new password do not match.")
    return
  }

  try {
    const response = await ApiServices.changeUserPassword({
      currentPassword: currentPassword.value,
      newPassword: newPassword.value
    })

    if (response.success) {
      alert('Password changed successfully!');
      AuthService.logout()
      await router.push('/login')
    } else {
      alert(`Failed to change password. Reason: ${response.message}`)
    }
  } catch (error) {
    console.error('Error changing password:', error);
    alert('Error changing password. Please try again.');
  } finally {
    currentPassword.value = ''
    newPassword.value = ''
    confirmNewPassword.value = ''
  }
}
</script>

<style scoped>
/* 你可以在这里添加特定的样式，但这里保持与现有UI一致 */
</style>
