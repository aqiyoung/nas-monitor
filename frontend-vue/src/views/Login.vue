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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form-wrapper {
  background-color: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 400px;
  text-align: center;
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.login-subtitle {
  font-size: 16px;
  color: #606266;
  margin-bottom: 30px;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

.login-tips {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .login-form-wrapper {
    width: 90%;
    padding: 30px;
  }
}
</style>
