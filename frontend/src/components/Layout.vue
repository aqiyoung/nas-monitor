<template>
  <div class="layout-container">
    <!-- 侧边栏 -->
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h1>NAS Monitor</h1>
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
        <el-menu-item index="/system">
          <template #icon>
            <el-icon><Monitor /></el-icon>
          </template>
          <span>系统状态</span>
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
  const token = localStorage.getItem('token')
  if (!token && route.path !== '/login') {
    router.push('/login')
  }
})
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  background-color: #ffffff;
  margin: 0;
  padding: 0;
}

/* 侧边栏样式 */
.sidebar {
  background-color: #ffffff;
  color: #303133;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
  border-right: 1px solid #e8e8e8;
}

.sidebar.collapsed {
  width: 64px;
}

/* Logo样式 */
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 20px;
  transition: all 0.3s ease;
}

.sidebar.collapsed .logo {
  padding: 0;
}

.logo h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #409EFF;
  transition: all 0.3s ease;
}

.sidebar.collapsed .logo h1 {
  font-size: 0;
}

/* 菜单样式 */
.el-menu-vertical-demo {
  background-color: transparent !important;
  border-right: none !important;
}

.el-menu-item {
  color: #606266 !important;
  height: 56px !important;
  line-height: 56px !important;
  margin: 4px 8px !important;
  border-radius: 8px !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: 1px solid transparent !important;
}

.el-menu-item:hover {
  background-color: #f5f7fa !important;
  border-color: rgba(64, 158, 255, 0.3) !important;
  color: #409EFF !important;
}

.el-menu-item.is-active {
  background-color: #ecf5ff !important;
  border-color: #409EFF !important;
  color: #409EFF !important;
}

.el-menu-item .el-icon {
  font-size: 18px !important;
  margin-right: 12px !important;
}

.sidebar.collapsed .el-menu-item .el-icon {
  margin-right: 0 !important;
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
  transition: all 0.3s ease;
}

/* 顶部导航栏 */
.header {
  height: 60px;
  background-color: white;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-left .el-button {
  transition: all 0.3s ease;
}

.header-left .el-button:hover {
  color: #409EFF;
  background-color: rgba(64, 158, 255, 0.1);
}

/* 用户信息 */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.user:hover {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
}

.username {
  margin-left: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  transition: all 0.3s ease;
}

.el-avatar {
  transition: all 0.3s ease;
}

.user:hover .el-avatar {
  transform: scale(1.05);
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.3);
}

/* 内容区 */
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #ffffff;
  transition: all 0.3s ease;
}

/* 滚动条样式 */
.content::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 4px;
}

.content::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.content::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
  }
  
  .sidebar.collapsed {
    left: -200px;
  }
  
  .content {
    padding: 16px;
  }
  
  .header {
    padding: 0 16px;
  }
}
</style>
