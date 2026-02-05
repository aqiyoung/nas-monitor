<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <h1 class="login-title">NAS Monitor</h1>
      <h2 class="login-subtitle">登录系统</h2>
      
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" class="login-button">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-tips" v-if="errorMessage">
        <el-alert
          :title="errorMessage"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../services/api'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  username: 'admin',
  password: 'admin123'
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
  background-color: #f8f9fa;
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(144, 238, 144, 0.1) 2px, transparent 0),
    radial-gradient(circle at 75px 75px, rgba(144, 238, 144, 0.1) 2px, transparent 0);
  background-size: 50px 50px;
}

/* 登录表单包装 */
.login-form-wrapper {
  background-color: white;
  padding: 48px 40px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  width: 420px;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e9ecef;
}

.login-form-wrapper:hover {
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

/* 标题样式 */
.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeInDown 0.6s ease-out;
}

.login-subtitle {
  font-size: 16px;
  color: #6c757d;
  margin-bottom: 36px;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

/* 表单样式 */
:deep(.el-form) {
  animation: fadeIn 0.8s ease-out 0.4s both;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__label) {
  font-size: 14px;
  color: #495057;
  font-weight: 500;
}

:deep(.el-input) {
  border-radius: 8px;
  overflow: hidden;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1) !important;
}

:deep(.el-input.is-focus .el-input__wrapper) {
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
  border-color: #4CAF50 !important;
}

/* 按钮样式 */
.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: fadeInUp 0.6s ease-out 0.6s both;
}

.login-button:hover {
  background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
  box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
  transform: translateY(-2px);
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
  border-radius: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-form-wrapper {
    width: 90%;
    max-width: 400px;
    padding: 36px 32px;
  }
  
  .login-title {
    font-size: 24px;
  }
  
  .login-subtitle {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .login-form-wrapper {
    padding: 28px 24px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 20px;
  }
  
  .login-button {
    height: 40px;
    font-size: 14px;
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
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 输入框动画 */
:deep(.el-input__inner) {
  transition: all 0.3s ease;
}

:deep(.el-input__inner:focus) {
  letter-spacing: 0.5px;
}
</style>
