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
  username: '',
  password: '',
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



<style scoped>
/* 登录容器 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
  transition: all var(--transition-normal);
  background-color: var(--bg-secondary);
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
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  opacity: 0.9;
  transition: all var(--transition-normal);
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
  transition: all var(--transition-normal);
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
  background-color: var(--bg-primary);
  backdrop-filter: blur(10px);
  padding: var(--spacing-xxl) var(--spacing-xl);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
  width: 460px;
  max-width: 90%;
  text-align: center;
  transition: all var(--transition-normal);
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: fadeInUp 0.8s ease-out;
  position: relative;
}

.login-form-wrapper:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-8px);
}

/* 品牌标识 */
.brand-section {
  margin-bottom: var(--spacing-xl);
  animation: fadeInDown 0.6s ease-out;
}

.brand-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--spacing-lg);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 8px 24px rgba(51, 112, 255, 0.3);
  animation: pulse 2s infinite;
  transition: all var(--transition-normal);
}

.brand-icon svg {
  color: white;
}

.login-title {
  font-size: var(--font-size-xxl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all var(--transition-normal);
}

.login-subtitle {
  font-size: var(--font-size-md);
  color: var(--text-secondary);
  margin-bottom: 0;
  transition: all var(--transition-normal);
}

/* 表单样式 */
:deep(.el-form) {
  animation: fadeIn 0.8s ease-out 0.3s both;
  width: 100%;
}

:deep(.el-form-item) {
  margin-bottom: var(--spacing-lg);
  width: 100%;
}

.input-wrapper {
  position: relative;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  background-color: var(--bg-secondary);
  transition: all var(--transition-normal);
  width: 100%;
  border: 1px solid var(--border-light);
}

.input-wrapper:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--border-focus);
}

.input-wrapper:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px var(--primary-light);
}

.input-icon {
  position: absolute;
  left: var(--spacing-md);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
  z-index: 1;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
}

.input-wrapper:focus-within .input-icon {
  color: var(--primary-color);
  transform: translateY(-50%) scale(1.1);
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
  font-size: var(--font-size-md);
  color: var(--text-primary);
  height: 52px !important;
  line-height: 52px !important;
  transition: all var(--transition-normal);
  width: 100% !important;
  background: transparent !important;
  font-family: inherit;
}

:deep(.el-input__inner:focus) {
  letter-spacing: 0.5px;
  color: var(--primary-color);
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  animation: fadeIn 0.8s ease-out 0.4s both;
  width: 100%;
}

:deep(.el-checkbox) {
  display: flex;
  align-items: center;
}

:deep(.el-checkbox__label) {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-left: var(--spacing-sm);
  transition: all var(--transition-normal);
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.forgot-password {
  font-size: var(--font-size-sm);
  color: var(--primary-color);
  text-decoration: none;
  transition: all var(--transition-normal);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
}

.forgot-password:hover {
  color: var(--primary-active);
  text-decoration: underline;
  background-color: var(--primary-light);
}

.forgot-password:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

/* 按钮样式 */
.login-button {
  width: 100%;
  height: 52px;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--border-radius-lg);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--info-color) 100%);
  border: none;
  transition: all var(--transition-normal);
  animation: fadeInUp 0.6s ease-out 0.5s both;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
  font-family: inherit;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left var(--transition-slow);
}

.login-button:hover::before {
  left: 100%;
}

.login-button:hover {
  background: linear-gradient(135deg, var(--info-color) 0%, var(--primary-color) 100%);
  box-shadow: 0 8px 24px rgba(51, 112, 255, 0.4);
  transform: translateY(-4px);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

/* 提示信息 */
.login-tips {
  margin-top: var(--spacing-lg);
  animation: fadeIn 0.8s ease-out 0.8s both;
}

:deep(.el-alert) {
  border-radius: var(--border-radius-lg);
  background-color: var(--error-light);
  border-color: var(--error-color);
}

:deep(.el-alert__content) {
  color: var(--error-color);
  font-size: var(--font-size-sm);
}

/* 底部信息 */
.login-footer {
  margin-top: var(--spacing-xl);
  animation: fadeInUp 0.6s ease-out 0.9s both;
}

.login-footer p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-sm);
  transition: all var(--transition-normal);
}

.footer-links {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  transition: all var(--transition-normal);
}

.footer-links a {
  color: var(--primary-color);
  text-decoration: none;
  transition: all var(--transition-normal);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
}

.footer-links a:hover {
  color: var(--primary-active);
  text-decoration: underline;
  background-color: var(--primary-light);
}

.footer-links a:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.footer-links span {
  margin: 0 var(--spacing-sm);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-form-wrapper {
    padding: var(--spacing-xl) var(--spacing-lg);
    width: 90%;
    max-width: 400px;
  }
  
  .login-title {
    font-size: var(--font-size-xl);
  }
  
  .brand-icon {
    width: 70px;
    height: 70px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: var(--spacing-md);
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
    left: var(--spacing-sm);
  }
  
  :deep(.el-input__inner) {
    height: 48px !important;
    line-height: 48px !important;
    font-size: var(--font-size-md);
  }
  
  .form-options {
    margin-bottom: var(--spacing-md);
  }
  
  :deep(.el-checkbox__label) {
    font-size: var(--font-size-xs);
  }
  
  .forgot-password {
    font-size: var(--font-size-xs);
  }
  
  .login-button {
    height: 48px;
    font-size: var(--font-size-md);
  }
  
  .login-tips {
    margin-top: var(--spacing-md);
  }
  
  .login-footer {
    margin-top: var(--spacing-lg);
  }
}

@media (max-width: 480px) {
  .login-form-wrapper {
    padding: var(--spacing-lg) var(--spacing-md);
    width: 95%;
    max-width: 360px;
  }
  
  .brand-section {
    margin-bottom: var(--spacing-lg);
  }
  
  .login-title {
    font-size: var(--font-size-lg);
  }
  
  .login-subtitle {
    font-size: var(--font-size-sm);
  }
  
  .brand-icon {
    width: 60px;
    height: 60px;
    margin-bottom: var(--spacing-md);
  }
  
  :deep(.el-form-item) {
    margin-bottom: var(--spacing-md);
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
    left: var(--spacing-sm);
  }
  
  :deep(.el-input__inner) {
    height: 44px !important;
    line-height: 44px !important;
    font-size: var(--font-size-sm);
  }
  
  .form-options {
    margin-bottom: var(--spacing-md);
  }
  
  :deep(.el-checkbox__label) {
    font-size: var(--font-size-xs);
  }
  
  .forgot-password {
    font-size: var(--font-size-xs);
  }
  
  .login-button {
    height: 44px;
    font-size: var(--font-size-md);
  }
  
  .login-tips {
    margin-top: var(--spacing-md);
  }
  
  .login-footer {
    margin-top: var(--spacing-lg);
  }
  
  .login-footer p {
    font-size: var(--font-size-xs);
    margin-bottom: var(--spacing-xs);
  }
  
  .footer-links {
    font-size: var(--font-size-xs);
  }
  
  .footer-links span {
    margin: 0 var(--spacing-xs);
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
    box-shadow: 0 8px 24px rgba(51, 112, 255, 0.3);
  }
  50% {
    box-shadow: 0 12px 32px rgba(51, 112, 255, 0.4);
  }
  100% {
    box-shadow: 0 8px 24px rgba(51, 112, 255, 0.3);
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

/* 可访问性增强 */
@media (prefers-reduced-motion: reduce) {
  .login-form-wrapper,
  .brand-icon,
  .input-wrapper,
  .input-icon,
  .login-button,
  .forgot-password,
  .footer-links a {
    transition: none;
  }
  
  .login-form-wrapper:hover,
  .input-wrapper:focus-within .input-icon {
    transform: none;
  }
  
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
    }
    to {
      opacity: 1;
    }
  }
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
  
  @keyframes pulse {
    0% {
      box-shadow: 0 8px 24px rgba(51, 112, 255, 0.3);
    }
    100% {
      box-shadow: 0 8px 24px rgba(51, 112, 255, 0.3);
    }
  }
  
  @keyframes blob-move {
    0% {
      transform: translate(0, 0) scale(1);
    }
    100% {
      transform: translate(0, 0) scale(1);
    }
  }
}
</style>