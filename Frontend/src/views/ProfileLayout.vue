<template>
  <header class="absolute inset-x-0 top-0 z-50 flex h-16 border-b border-gray-900/10">
    <div class="mx-auto flex w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
      <!-- 左侧区域：移动菜单按钮、Logo 及 Back 链接 -->
      <div class="flex flex-1 items-center gap-x-6">
        <button type="button" class="-m-3 p-3 md:hidden" @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="h-6 w-6 text-gray-900" aria-hidden="true" />
        </button>
        <img
          class="h-8 w-auto"
          src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
        />
        <!-- Back 链接：包含箭头图标 -->
        <a
          v-for="(item, itemIdx) in navigation"
          :key="itemIdx"
          :href="item.href"
          class="flex items-center text-sm font-semibold text-gray-700 hover:text-indigo-600"
        >
          <component :is="item.icon" class="h-5 w-5 mr-1" aria-hidden="true" />
          {{ item.name }}
        </a>
      </div>
      <div class="flex flex-1 items-center justify-end gap-x-8">
        <button type="button" class="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500">
          <span class="sr-only">View notifications</span>
          <BellIcon class="h-6 w-6" aria-hidden="true" />
        </button>
        <!-- 顶部头像显示，并支持修改头像 -->
        <div class="relative">
          <a href="#" class="-m-1.5 p-1.5">
            <span class="sr-only">Your profile</span>
            <img class="h-8 w-8 rounded-full bg-gray-800" :src="profile.avatar" alt="Your Avatar" />
          </a>
        </div>
      </div>
    </div>

    <Dialog class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
      <div class="fixed inset-0 z-50" />
      <DialogPanel class="fixed inset-y-0 left-0 z-50 w-full overflow-y-auto bg-white px-4 pb-6 sm:max-w-sm sm:px-6 sm:ring-1 sm:ring-gray-900/10">
        <div class="-ml-0.5 flex h-16 items-center gap-x-6">
          <button type="button" class="-m-2.5 p-2.5 text-gray-700" @click="mobileMenuOpen = false">
            <span class="sr-only">Close menu</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
          <div class="-ml-0.5">
            <a href="#" class="-m-1.5 block p-1.5">
              <span class="sr-only">Your Company</span>
              <img class="h-8 w-auto" src="https://tailwindcss.com/plus-assets/img/logos/mark.svg?color=indigo&shade=600" alt="" />
            </a>
          </div>
        </div>
        <div class="mt-2 space-y-2">
          <a v-for="item in navigation" :key="item.name" :href="item.href" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold text-gray-900 hover:bg-gray-50">{{ item.name }}</a>
        </div>
      </DialogPanel>
    </Dialog>
  </header>

  <div class="mx-auto max-w-7xl pt-16 lg:flex lg:gap-x-16 lg:px-8">
    <h1 class="sr-only">General Settings</h1>

    <aside class="flex overflow-x-auto border-b border-gray-900/5 py-4 lg:block lg:w-64 lg:flex-none lg:border-0 lg:py-20">
      <nav class="flex-none px-4 sm:px-6 lg:px-0">
        <ul role="list" class="flex gap-x-3 gap-y-1 whitespace-nowrap lg:flex-col">
          <li v-for="item in secondaryNavigation" :key="item.name">
            <a :href="item.href"
               :class="[item.current ? 'bg-gray-50 text-indigo-600' : 'text-gray-700 hover:bg-gray-50 hover:text-indigo-600', 'group flex gap-x-3 rounded-md py-2 pr-3 pl-2 text-sm font-semibold']"
               @click.prevent="item.action ? item.action() : null"
            >
              <component :is="item.icon" :class="[item.current ? 'text-indigo-600' : 'text-gray-400 group-hover:text-indigo-600', 'h-6 w-6 shrink-0']" aria-hidden="true" />
              {{ item.name }}
            </a>
          </li>
        </ul>
      </nav>
    </aside>

    <main class="px-4 py-16 sm:px-6 lg:flex-auto lg:px-0 lg:py-20">
      <!-- 放大版头像，右侧显示 -->
      <div class="flex justify-end">
        <div class="relative inline-block">
          <img :src="profile.avatar" alt="Avatar" class="w-64 h-64 rounded-full object-cover" />
          <button
            class="absolute bottom-4 right-4 bg-white p-2 rounded-full shadow hover:bg-gray-100"
            @click="updateAvatar"
          >
            <PencilIcon class="w-5 h-5 text-gray-700" />
          </button>
        </div>
      </div>

      <div class="mx-auto max-w-2xl space-y-16 sm:space-y-20 lg:mx-0 lg:max-w-none">
        <!-- Profile 部分 -->
        <div>
          <h2 class="text-base font-semibold text-gray-900">Profile</h2>
          <dl class="mt-6 divide-y divide-gray-100 border-t border-gray-200 text-sm">
            <div v-for="(value, key) in profileData" :key="key" class="py-6 sm:flex">
              <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">{{ key }}</dt>
              <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                <div class="text-gray-900 flex items-center">
                  <template v-if="editingField === key">
                    <input
                      type="text"
                      v-model="editingValue"
                      @keyup.enter="saveField(key)"
                      class="border border-gray-300 rounded p-1"
                    />
                  </template>
                  <template v-else>
                    {{ value }}
                  </template>
                </div>
                <div class="flex items-center gap-x-2">
                  <button
                    type="button"
                    class="font-semibold text-indigo-600 hover:text-indigo-500"
                    @click="editingField === key ? saveField(key) : updateField(key)"
                  >
                    {{ editingField === key ? "Save" : "Update" }}
                  </button>
                </div>
              </dd>
            </div>
          </dl>
        </div>

        <!-- Language and dates 部分 -->
        <div>
          <h2 class="text-base font-semibold text-gray-900">Language and dates</h2>
          <p class="mt-1 text-sm text-gray-500">Choose what language and date format to use throughout your account.</p>
          <dl class="mt-6 divide-y divide-gray-100 border-t border-gray-200 text-sm">
            <div class="py-6 sm:flex">
              <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">Language</dt>
              <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                <div class="text-gray-900">
                  <template v-if="editingLanguage">
                    <select v-model="currentLanguage" class="border border-gray-300 rounded p-1">
                      <option v-for="option in languageOptions" :key="option" :value="option">{{ option }}</option>
                    </select>
                  </template>
                  <template v-else>
                    {{ currentLanguage }}
                  </template>
                </div>
                <button type="button" @click="toggleLanguageEdit" class="font-semibold text-indigo-600 hover:text-indigo-500">
                  {{ editingLanguage ? "Save" : "Update" }}
                </button>
              </dd>
            </div>
            <div class="py-6 sm:flex">
              <dt class="font-medium text-gray-900 sm:w-64 sm:flex-none sm:pr-6">Date format</dt>
              <dd class="mt-1 flex justify-between gap-x-6 sm:mt-0 sm:flex-auto">
                <div class="text-gray-900">DD-MM-YYYY</div>
                <button type="button" class="font-semibold text-indigo-600 hover:text-indigo-500">Update</button>
              </dd>
            </div>
            <SwitchGroup as="div" class="flex pt-6">
              <SwitchLabel as="dt" class="flex-none pr-6 font-medium text-gray-900 sm:w-64" passive>Automatic timezone</SwitchLabel>
              <dd class="flex flex-auto items-center justify-end">
                <Switch v-model="automaticTimezoneEnabled" :class="[automaticTimezoneEnabled ? 'bg-indigo-600' : 'bg-gray-200', 'flex w-8 cursor-pointer rounded-full p-px ring-1 ring-gray-900/5 transition-colors duration-200 ease-in-out ring-inset focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600']">
                  <span aria-hidden="true" :class="[automaticTimezoneEnabled ? 'translate-x-3.5' : 'translate-x-0', 'h-4 w-4 transform rounded-full bg-white ring-1 shadow-xs ring-gray-900/5 transition duration-200 ease-in-out']" />
                </Switch>
              </dd>
            </SwitchGroup>
          </dl>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Dialog, DialogPanel, Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { Bars3Icon, BellIcon, ArrowLeftIcon, CubeIcon, XCircleIcon, PowerIcon, FingerPrintIcon, UserCircleIcon, UsersIcon, XMarkIcon, PencilIcon } from '@heroicons/vue/24/outline'
import AuthService from "@/services/AuthService.js"
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { locale } = useI18n()

const navigation = [
  { name: 'Back', href: '/', icon: ArrowLeftIcon }
]

function logout() {
  AuthService.logout()
  router.push('/login')
}

function goToSecurity() {
  // 跳转到 Security 页面（对应组件：components/profiles/ProfilePassword.vue）
  router.push('/profile/password')
}

const secondaryNavigation = [
  { name: 'General', href: '#', icon: UserCircleIcon, current: true },
  { name: 'Security', href: '#', icon: FingerPrintIcon, current: false, action: goToSecurity },
  { name: 'Notifications', href: '#', icon: BellIcon, current: false },
  { name: 'Team members', href: '#', icon: UsersIcon, current: false },
  { name: 'Logout', href: '#', icon: XCircleIcon, action: logout }
]

const mobileMenuOpen = ref(false)
const automaticTimezoneEnabled = ref(true)

const profile = ref({
  name: "",
  Email: "",
  Title: "",
  Wecom: "",
  avatar: "",
})

const profileData = ref({
  "Name": profile.value.name,
  "Email address": profile.value.Email,
  "Title": profile.value.Title,
  "Wecom": profile.value.Wecom,
})

const editingField = ref(null)
const editingValue = ref('')

function updateField(key) {
  editingField.value = key
  editingValue.value = profileData.value[key]
}

function saveField(key) {
  if (key === "Email address") {
    if (!validateEmail(editingValue.value)) {
      alert("Invalid email address.")
      return
    }
    // 模拟发送验证邮件
    alert(`A verification email has been sent to ${editingValue.value}.`)
  }
  profileData.value[key] = editingValue.value
  editingField.value = null
  editingValue.value = ''
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function updateAvatar() {
  const newAvatar = prompt("Enter new avatar URL:", profile.value.avatar)
  if (newAvatar) {
    profile.value.avatar = newAvatar
    alert("Avatar updated.")
  }
}

const languageOptions = ["English", "中文(简体)", "中文(繁体)"]
const currentLanguage = ref("English")
const editingLanguage = ref(false)

function toggleLanguageEdit() {
  if (editingLanguage.value) {
    // 保存语言并更新全局语言（确保整个页面及 / 路由下页面更新）
    locale.value = currentLanguage.value
    alert(`Language updated to ${currentLanguage.value}`)
  }
  editingLanguage.value = !editingLanguage.value
}
</script>
