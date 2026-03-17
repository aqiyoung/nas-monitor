<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isSidebarCollapsed ? '64px' : '200px'" :class="['sidebar', { collapsed: isSidebarCollapsed }]">
      <div class="logo">
        <h1>运维监控中心</h1>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        router
        @select="handleMenuSelect"
      >
        <el-menu-item index="/dashboard">
          <template #icon>
            <el-icon><HomeFilled /></el-icon>
          </template>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/network">
          <template #icon>
            <el-icon><Connection /></el-icon>
          </template>
          <span>网络监控</span>
        </el-menu-item>
        <el-menu-item index="/io">
          <template #icon>
            <el-icon><DataAnalysis /></el-icon>
          </template>
          <span>IO状态</span>
        </el-menu-item>
        <el-menu-item index="/docker">
          <template #icon>
            <el-icon><Box /></el-icon>
          </template>
          <span>Docker监控</span>
        </el-menu-item>
        <el-menu-item index="/alarm">
          <template #icon>
            <el-icon><WarningFilled /></el-icon>
          </template>
          <span>告警管理</span>
        </el-menu-item>
        <el-menu-item index="/notification">
          <template #icon>
            <el-icon><Bell /></el-icon>
          </template>
          <span>通知管理</span>
        </el-menu-item>
        <el-menu-item index="/monitoring">
          <template #icon>
            <el-icon><DataAnalysis /></el-icon>
          </template>
          <span>监控中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-left">
          <el-button type="text" @click="toggleSidebar">
            <el-icon><Menu /></el-icon>
          </el-button>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user">
              <el-avatar :size="32">
                <User />
              </el-avatar>
              <span class="username">{{ username }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区 -->
      <el-main class="content">
        <transition name="fade" mode="out-in">
          <slot></slot>
        </transition>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  HomeFilled,
  Monitor,
  Connection,
  DataAnalysis,
  Box,
  WarningFilled,
  Bell,
  Menu,
  User
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const isSidebarCollapsed = ref(false)
const username = ref('管理员')

// 计算当前激活的菜单
const activeMenu = computed(() => {
  return route.path
})

// 处理菜单选择
const handleMenuSelect = (key: string) => {
  router.push(key)
}

// 切换侧边栏折叠状态
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

// 检查是否已登录
onMounted(() => {
  // 暂时注释掉登录检查，以便测试仪表盘
  // const token = localStorage.getItem('token')
  // if (!token && route.path !== '/login') {
  //   router.push('/login')
  // }
})
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: var(--bg-secondary);
  margin: 0;
  padding: 0;
}

/* 侧边栏样式 */
.sidebar {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
  z-index: var(--z-index-fixed);
  border-right: 1px solid var(--border-primary);
  position: relative;
  overflow: hidden;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(51, 112, 255, 0.05), transparent);
  transition: left var(--transition-slow);
}

.sidebar:hover::before {
  left: 100%;
}

.sidebar.collapsed {
  width: 64px;
}

/* Logo样式 */
.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-primary);
  padding: 0 var(--spacing-lg);
  transition: all var(--transition-normal);
  background: linear-gradient(135deg, var(--primary-light), var(--bg-primary));
}

.sidebar.collapsed .logo {
  padding: 0;
}

.logo h1 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  margin: 0;
  color: var(--primary-color);
  transition: all var(--transition-normal);
  text-align: center;
}

.sidebar.collapsed .logo h1 {
  font-size: 0;
}

/* 菜单样式 */
.el-menu-vertical-demo {
  background-color: transparent !important;
  border-right: none !important;
  height: calc(100vh - 64px);
  overflow-y: auto;
}

.el-menu-item {
  color: var(--text-regular) !important;
  height: 56px !important;
  line-height: 56px !important;
  margin: var(--spacing-xs) var(--spacing-sm) !important;
  border-radius: var(--border-radius-md) !important;
  transition: all var(--transition-normal) !important;
  border: 1px solid transparent !important;
  position: relative;
  overflow: hidden;
}

.el-menu-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: var(--primary-color);
  transform: scaleY(0);
  transition: transform var(--transition-normal);
  border-radius: 0 var(--border-radius-sm) var(--border-radius-sm) 0;
}

.el-menu-item:hover {
  background-color: var(--bg-secondary) !important;
  border-color: var(--border-focus) !important;
  color: var(--primary-color) !important;
  transform: translateX(4px);
}

.el-menu-item.is-active {
  background-color: var(--primary-light) !important;
  border-color: var(--primary-color) !important;
  color: var(--primary-color) !important;
  font-weight: var(--font-weight-medium) !important;
}

.el-menu-item.is-active::before {
  transform: scaleY(1);
}

.el-menu-item .el-icon {
  font-size: 20px !important;
  margin-right: var(--spacing-md) !important;
  transition: all var(--transition-normal) !important;
}

.sidebar.collapsed .el-menu-item .el-icon {
  margin-right: 0 !important;
  font-size: 24px !important;
}

.sidebar.collapsed .el-menu-item span {
  font-size: 0 !important;
}

/* 主内容区 */
.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all var(--transition-normal);
}

/* 顶部导航栏 */
.header {
  height: 64px;
  background-color: var(--bg-primary);
  border-bottom: 1px solid var(--border-primary);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  z-index: var(--z-index-sticky);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.header-left .el-button {
  transition: all var(--transition-normal);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
}

.header-left .el-button:hover {
  color: var(--primary-color);
  background-color: var(--primary-light);
  border-color: var(--primary-color);
}

/* 用户信息 */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}

.user::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(51, 112, 255, 0.1), transparent);
  transition: left var(--transition-slow);
}

.user:hover::before {
  left: 100%;
}

.user:hover {
  background-color: var(--bg-secondary);
  border-color: var(--border-focus);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.username {
  margin-left: var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  transition: all var(--transition-normal);
  white-space: nowrap;
}

.el-avatar {
  transition: all var(--transition-normal);
  border: 2px solid var(--primary-light);
}

.user:hover .el-avatar {
  transform: scale(1.1);
  box-shadow: 0 0 12px var(--primary-light);
  border-color: var(--primary-color);
}

/* 内容区 */
.content {
  flex: 1;
  padding: var(--spacing-lg);
  overflow-y: auto;
  background-color: var(--bg-secondary);
  transition: all var(--transition-normal);
}

/* 滚动条样式 */
.content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.content::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: var(--border-radius-full);
}

.content::-webkit-scrollbar-thumb {
  background: var(--text-placeholder);
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
  border: 2px solid var(--bg-tertiary);
}

.content::-webkit-scrollbar-thumb:hover {
  background: var(--text-secondary);
  transform: scaleY(1.1);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .sidebar {
    width: 180px;
  }
  
  .sidebar.collapsed {
    width: 64px;
  }
  
  .logo h1 {
    font-size: var(--font-size-md);
  }
  
  .el-menu-item {
    height: 52px !important;
    line-height: 52px !important;
  }
  
  .content {
    padding: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: var(--z-index-modal);
    width: 200px;
  }
  
  .sidebar.collapsed {
    left: -200px;
  }
  
  .content {
    padding: var(--spacing-sm);
  }
  
  .header {
    padding: 0 var(--spacing-sm);
    height: 56px;
  }
  
  .username {
    display: none;
  }
  
  .user {
    padding: var(--spacing-xs);
  }
  
  .logo {
    height: 56px;
  }
  
  .el-menu-vertical-demo {
    height: calc(100vh - 56px);
  }
  
  .el-menu-item {
    height: 48px !important;
    line-height: 48px !important;
  }
}

@media (max-width: 480px) {
  .content {
    padding: var(--spacing-xs);
  }
  
  .header {
    padding: 0 var(--spacing-xs);
  }
  
  .el-menu-item .el-icon {
    font-size: 18px !important;
  }
  
  .sidebar.collapsed .el-menu-item .el-icon {
    font-size: 20px !important;
  }
}

/* 可访问性增强 */
.el-menu-item:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.user:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.header-left .el-button:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

/* 键盘导航增强 */
.el-menu-item:focus {
  background-color: var(--primary-light) !important;
  color: var(--primary-color) !important;
}

/* 屏幕阅读器支持 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .sidebar {
    background-color: var(--bg-primary-high-contrast);
    border-right: 2px solid var(--border-primary-high-contrast);
  }
  
  .header {
    background-color: var(--bg-primary-high-contrast);
    border-bottom: 2px solid var(--border-primary-high-contrast);
  }
  
  .el-menu-item {
    border: 1px solid var(--border-primary-high-contrast) !important;
  }
  
  .el-menu-item:hover,
  .el-menu-item.is-active {
    border-color: var(--primary-color-high-contrast) !important;
  }
}
</style>
