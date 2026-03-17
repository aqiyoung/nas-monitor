<template>
  <router-view v-slot="{ Component }">
    <template v-if="isLoginPage">
      <transition name="page-fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </template>
    <template v-else>
      <Layout>
        <transition name="page-slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </Layout>
    </template>
  </router-view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Layout from './components/Layout.vue'

const route = useRoute()

const isLoginPage = computed(() => {
  return route.path === '/login'
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f0f2f5;
}

#app {
  width: 100%;
  height: 100%;
}

/* 页面淡入淡出动画 */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* 页面滑动动画 */
.page-slide-enter-active,
.page-slide-leave-active {
  transition: all 0.3s ease;
}

.page-slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
  .page-fade-enter-active,
  .page-fade-leave-active,
  .page-slide-enter-active,
  .page-slide-leave-active {
    transition: none;
  }
  
  .page-fade-enter-from,
  .page-fade-leave-to,
  .page-slide-enter-from,
  .page-slide-leave-to {
    transform: none;
  }
}
</style>
