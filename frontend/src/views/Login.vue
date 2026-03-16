<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="bg-decoration">
      <div class="bg-gradient"></div>
      <div class="bg-blobs">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
      </div>
    </div>
    
    <!-- 登录表单 -->
    <div class="login-form-wrapper">
      <!-- 品牌标识 -->
      <div class="brand-section">
        <div class="brand-icon">
          <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 8V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1 class="login-title">运维监控中心</h1>
        <p class="login-subtitle">智能监控，一键管理</p>
      </div>
      
      <!-- 登录表单 -->
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="0">
        <el-form-item prop="username">
          <div class="input-wrapper">
            <span class="input-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <el-input v-model="loginForm.username" placeholder="请输入用户名" />
          </div>
        </el-form-item>
        
        <el-form-item prop="password">
          <div class="input-wrapper">
            <span class="input-icon">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 15C15.866 15 19 11.866 19 8C19 4.13401 15.866 1 12 1C8.13401 1 5 4.13401 5 8C5 11.866 8.13401 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 12V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 12H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
          </div>
        </el-form-item>
        
        <el-form-item>
          <div class="form-options">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <a href="#" class="forgot-password">忘记密码？</a>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">
            登录
          </el-button>
        </el-form-item>
        

      </el-form>
      
      <!-- 错误提示 -->
      <div class="login-tips" v-if="errorMessage">
        <el-alert
          :title="errorMessage"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
      
      <!-- 底部信息 -->
      <div class="login-footer">
        <p>© 2026 运维监控中心. 保留所有权利.</p>
        <div class="footer-links">
          <a href="#">隐私政策</a>
          <span>|</span>
          <a href="#">服务条款</a>
        </div>
      </div>
      

      

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  username: 'admin',
  password: 'password',
  remember: false
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  // 表单验证
  await loginFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      errorMessage.value = ''
      
      try {
        // 调用登录API
        const response = await authApi.login(loginForm)
        
        // 存储token
        if (response.access_token) {
          localStorage.setItem('token', response.access_token)
          // 跳转到仪表盘
          router.push('/dashboard')
        } else {
          errorMessage.value = '登录失败：未返回token'
        }
      } catch (error: any) {
        console.error('登录失败:', error)
        errorMessage.value = error.response?.data?.detail || '登录失败，请检查用户名和密码'
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style>
/* 全局CSS变量 */
:root {
  --primary-color: #4F46E5;
  --secondary-color: #7C3AED;
  --accent-color: #8B5CF6;
  --text-color: #1E293B;
  --text-light-color: #64748B;
  --background-light: #FFFFFF;
  --background-dark: #F8FAFC;
  --error-color: #EF4444;
  --success-color: #10B981;
  --warning-color: #F59E0B;
  --gradient-start: #4F46E5;
  --gradient-end: #7C3AED;
  --transition-speed: 0.3s;
  --transition-ease: cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>

<style scoped>
/* 登录容器 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 暗黑模式 */
.login-container.dark-mode {
  background-color: #0f172a;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.bg-gradient {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  opacity: 0.9;
  transition: all var(--transition-speed) var(--transition-ease);
}

.login-container.dark-mode .bg-gradient {
  opacity: 0.7;
}

.bg-blobs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: blob-move 20s infinite alternate ease-in-out;
  transition: all 0.3s ease;
}

.login-container.dark-mode .blob {
  background: rgba(255, 255, 255, 0.05);
}

.blob-1 {
  width: 300px;
  height: 300px;
  top: -50px;
  left: -50px;
  animation-delay: 0s;
}

.blob-2 {
  width: 400px;
  height: 400px;
  bottom: -100px;
  right: -100px;
  animation-delay: 5s;
}

.blob-3 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

/* 登录表单包装 */
.login-form-wrapper {
  background-color: var(--background-light);
  backdrop-filter: blur(10px);
  padding: 60px 48px;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  width: 460px;
  max-width: 90%;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: fadeInUp 0.8s ease-out;
  position: relative;
}

.login-container.dark-mode .login-form-wrapper {
  background-color: var(--background-light);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-form-wrapper:hover {
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.2);
  transform: translateY(-8px);
}

.login-container.dark-mode .login-form-wrapper:hover {
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.4);
}

/* 品牌标识 */
.brand-section {
  margin-bottom: 40px;
  animation: fadeInDown 0.6s ease-out;
}

.brand-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.3);
  animation: pulse 2s infinite;
  transition: all var(--transition-speed) var(--transition-ease);
}

.brand-icon svg {
  color: white;
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all var(--transition-speed) var(--transition-ease);
}

.login-subtitle {
  font-size: 16px;
  color: var(--text-light-color);
  margin-bottom: 0;
  transition: all 0.3s ease;
}

/* 表单样式 */
:deep(.el-form) {
  animation: fadeIn 0.8s ease-out 0.3s both;
  width: 100%;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
  width: 100%;
}

.input-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background-color: var(--background-dark);
  transition: all 0.3s ease;
  width: 100%;
}

.input-wrapper:hover {
  background-color: #f1f3f5;
}



.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light-color);
  z-index: 1;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

:deep(.el-input) {
  border: none !important;
  background: transparent !important;
  width: 100%;
}

:deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
  padding-left: 44px !important;
  height: 52px !important;
  width: 100% !important;
}

:deep(.el-input__inner) {
  font-size: 16px;
  color: var(--text-color);
  height: 52px !important;
  line-height: 52px !important;
  transition: all 0.3s ease;
  width: 100% !important;
  background: transparent !important;
}



:deep(.el-input__inner:focus) {
  letter-spacing: 0.5px;
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  animation: fadeIn 0.8s ease-out 0.4s both;
  width: 100%;
}

:deep(.el-checkbox) {
  display: flex;
  align-items: center;
}

:deep(.el-checkbox__label) {
  font-size: 14px;
  color: var(--text-light-color);
  margin-left: 8px;
  transition: all 0.3s ease;
}

.forgot-password {
  font-size: 14px;
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 4px;
}

.forgot-password:hover {
  color: var(--secondary-color);
  text-decoration: underline;
  background-color: rgba(102, 126, 234, 0.1);
}



/* 按钮样式 */
.login-button {
  width: 100%;
  height: 52px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
  border: none;
  transition: all var(--transition-speed) var(--transition-ease);
  animation: fadeInUp 0.6s ease-out 0.5s both;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  background: linear-gradient(135deg, var(--gradient-end) 0%, var(--gradient-start) 100%);
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4);
  transform: translateY(-4px);
}

.login-button:active {
  transform: translateY(0);
}

/* 提示信息 */
.login-tips {
  margin-top: 24px;
  animation: fadeIn 0.8s ease-out 0.8s both;
}

:deep(.el-alert) {
  border-radius: 12px;
  background-color: rgba(231, 76, 60, 0.1);
  border-color: var(--error-color);
}

:deep(.el-alert__content) {
  color: var(--error-color);
}

/* 底部信息 */
.login-footer {
  margin-top: 40px;
  animation: fadeInUp 0.6s ease-out 0.9s both;
}

.login-footer p {
  font-size: 14px;
  color: var(--text-light-color);
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.footer-links {
  font-size: 14px;
  color: var(--text-light-color);
  transition: all 0.3s ease;
}

.footer-links a {
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.3s ease;
}

.footer-links a:hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

.footer-links span {
  margin: 0 8px;
}





/* 响应式设计 */
@media (max-width: 768px) {
  .login-form-wrapper {
    padding: 48px 36px;
    width: 90%;
    max-width: 400px;
  }
  
  .login-title {
    font-size: 28px;
  }
  
  .brand-icon {
    width: 70px;
    height: 70px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 20px;
  }
  
  .input-wrapper {
    height: 48px;
  }
  
  :deep(.el-input__wrapper) {
    height: 48px !important;
    padding-left: 40px !important;
  }
  
  .input-icon {
    width: 16px;
    height: 16px;
    left: 14px;
  }
  
  :deep(.el-input__inner) {
    height: 48px !important;
    line-height: 48px !important;
    font-size: 15px;
  }
  
  .form-options {
    margin-bottom: 20px;
  }
  
  :deep(.el-checkbox__label) {
    font-size: 13px;
  }
  
  .forgot-password {
    font-size: 13px;
  }
  
  .login-button {
    height: 48px;
    font-size: 16px;
  }
  
  .login-tips {
    margin-top: 20px;
  }
  
  .login-footer {
    margin-top: 32px;
  }
  
  .theme-toggle {
    top: 16px;
    right: 16px;
  }
  
  .theme-button {
    padding: 6px;
  }
  
  .theme-button svg {
    width: 16px;
    height: 16px;
  }
}

@media (max-width: 480px) {
  .login-form-wrapper {
    padding: 36px 24px;
    width: 95%;
    max-width: 360px;
  }
  
  .brand-section {
    margin-bottom: 32px;
  }
  
  .login-title {
    font-size: 24px;
  }
  
  .login-subtitle {
    font-size: 14px;
  }
  
  .brand-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 16px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 16px;
  }
  
  .input-wrapper {
    height: 44px;
  }
  
  :deep(.el-input__wrapper) {
    height: 44px !important;
    padding-left: 36px !important;
  }
  
  .input-icon {
    width: 14px;
    height: 14px;
    left: 12px;
  }
  
  :deep(.el-input__inner) {
    height: 44px !important;
    line-height: 44px !important;
    font-size: 14px;
  }
  
  .form-options {
    margin-bottom: 16px;
  }
  
  :deep(.el-checkbox__label) {
    font-size: 12px;
  }
  
  .forgot-password {
    font-size: 12px;
  }
  
  .login-button {
    height: 44px;
    font-size: 15px;
  }
  
  .login-tips {
    margin-top: 16px;
  }
  
  .login-footer {
    margin-top: 24px;
  }
  
  .login-footer p {
    font-size: 12px;
    margin-bottom: 8px;
  }
  
  .footer-links {
    font-size: 12px;
  }
  
  .footer-links span {
    margin: 0 4px;
  }
  
  .theme-toggle {
    top: 12px;
    right: 12px;
  }
  
  .theme-button {
    padding: 4px;
  }
  
  .theme-button svg {
    width: 14px;
    height: 14px;
  }
  
  .color-scheme-selector {
    margin-top: 16px;
  }
  
  .scheme-button {
    width: 20px;
    height: 20px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  }
  50% {
    box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
  }
  100% {
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  }
}

@keyframes blob-move {
  0% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(50px, 50px) scale(1.1);
  }
  100% {
    transform: translate(100px, 20px) scale(0.9);
  }
}
</style>