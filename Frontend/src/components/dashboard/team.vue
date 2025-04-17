<template>
  <section class="text-gray-600 body-font">
    <div class="container px-5 py-24 mx-auto">
      <div class="flex">
        <!-- 左侧技术栈滚动展示 -->
        <div class="w-1/4 pr-8">
          <!-- TagScrollWrapper 和 TagScrollRow 在本文件中定义，无需额外文件 -->
          <TagScrollWrapper>
            <TagScrollRow :tags="tagsRow1" />
            <TagScrollRow :tags="tagsRow2" />
            <TagScrollRow :tags="tagsRow3" />
          </TagScrollWrapper>
        </div>
        <!-- 右侧团队展示 -->
        <div class="w-3/4">
          <div class="flex flex-col text-center w-full mb-20">
            <h1 class="text-2xl font-medium title-font mb-4 text-gray-900 tracking-widest">OUR TEAM</h1>
            <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
              Whatever cardigan tote bag tumblr hexagon brooklyn asymmetrical gentrify, subway tile poke farm-to-table.
              Franzen you probably haven't heard of them.
            </p>
          </div>
          <div class="flex flex-wrap -m-4">
            <div v-for="member in team" :key="member.name" class="p-4 lg:w-1/2">
              <div class="h-full flex sm:flex-row flex-col items-center sm:justify-start justify-center text-center sm:text-left">
                <img
                  alt="team"
                  class="flex-shrink-0 rounded-lg w-48 h-48 object-cover object-center sm:mb-0 mb-4"
                  :src="member.image"
                />
                <div class="flex-grow sm:pl-8">
                  <h2 class="title-font font-medium text-lg text-gray-900">{{ member.name }}</h2>
                  <h3 class="text-gray-500 mb-3">{{ member.position }}</h3>
                  <p class="mb-4">{{ member.description }}</p>
                  <span class="inline-flex">
                    <!-- GitHub 图标 -->
                    <a :href="member.github" target="_blank" class="text-gray-500">
                      <svg class="w-5 h-5" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.19 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                      </svg>
                    </a>
                    <!-- Telegram 图标 -->
                    <a :href="member.telegram" target="_blank" class="ml-2 text-gray-500">
                      <svg class="w-5 h-5" viewBox="0 0 240 240" fill="currentColor" aria-hidden="true">
                        <path d="M120 0C53.7 0 0 53.7 0 120s53.7 120 120 120 120-53.7 120-120S186.3 0 120 0zm58.1 80.4l-17.8 84.4c-1.3 5.8-4.8 7.3-9.8 4.5l-27.1-20-13 12.5c-1.4 1.4-2.6 2.6-5.3 2.6l1.9-27.4 49.9-45.1c2.2-1.9-.5-3-3.4-1.1l-61.7 38.9-26.6-8.3c-5.8-1.8-5.9-5.8 1.3-8.6l103.9-40.1c4.8-1.8 9-0.2 7.3 8.7z"/>
                      </svg>
                    </a>
                    <!-- 网站图标 -->
                    <a :href="member.website" target="_blank" class="ml-2 text-gray-500">
                      <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="w-5 h-5" viewBox="0 0 24 24">
                        <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>
                      </svg>
                    </a>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'TeamSection',
  components: {
    TagScrollWrapper: {
      template: `<div class="space-y-4"><slot /></div>`
    },
    TagScrollRow: {
      props: { tags: { type: Array, required: true } },
      template: `
        <div class="overflow-hidden">
          <div class="flex whitespace-nowrap animate-scroll">
            <span v-for="tag in tags" :key="tag" class="inline-block mr-4 px-2 py-1 bg-gray-200 rounded">
              {{ tag }}
            </span>
          </div>
        </div>
      `
    }
  },
  data() {
    return {
      tagsRow1: ['Vue.js', 'Vite', 'HTML', 'CSS', 'CORS', 'Tailwind', 'RESTFUL API', 'yarn', 'i18n'],
      tagsRow2: ['JavaScript', 'Python', 'Quart', 'JWT', 'async', 'pydantic', 'asncpg', 'oauth2', 'Wecom'],
      tagsRow3: ['Docker', 'Compose', 'Jenkins', 'Nginx', 'Jumpserver', 'golocproxy', 'PostgreSQL'],
      team: [
        {
          name: 'Zhicheng Dong',
          position: 'All Stack Developer',
          description: '',
          image: 'https://avatars.githubusercontent.com/u/163859507',
          github: 'https://github.com/cg8-5712',
          telegram: 'cg85712.t.me',
          website: '5712.cg8@gmail.com'
      ]
    };
  }
};
</script>

<style scoped>
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}
.animate-scroll {
  animation: scroll 10s linear infinite;
}
</style>
