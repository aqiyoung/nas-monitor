<template>
  <div class="docker-page">
    <h2>Docker监控</h2>
    
    <!-- 容器列表 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>容器列表</span>
        </div>
      </template>
      <div class="containers-info">
        <el-table :data="containers" style="width: 100%">
          <el-table-column prop="name" label="容器名称" />
          <el-table-column prop="id" label="容器ID" width="120">
            <template #default="scope">
              {{ scope.row.id.substring(0, 12) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="getContainerStatusType(scope.row.status)">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="image" label="镜像" />
          <el-table-column prop="created" label="创建时间" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button-group>
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="handleStartContainer(scope.row.id)"
                  :disabled="scope.row.status === 'running'"
                >
                  启动
                </el-button>
                <el-button 
                  type="warning" 
                  size="small" 
                  @click="handleStopContainer(scope.row.id)"
                  :disabled="scope.row.status !== 'running'"
                >
                  停止
                </el-button>
                <el-button 
                  type="info" 
                  size="small" 
                  @click="handleRestartContainer(scope.row.id)"
                >
                  重启
                </el-button>
                <el-button 
                  type="success" 
                  size="small" 
                  @click="handleViewLogs(scope.row.id, scope.row.name)"
                >
                  日志
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 容器日志 -->
    <el-dialog
      v-model="logsDialogVisible"
      :title="`容器日志 - ${selectedContainerName}`"
      width="80%"
    >
      <div class="logs-content">
        <pre v-if="containerLogs">{{ containerLogs }}</pre>
        <div v-else-if="logsLoading" class="loading">加载中...</div>
        <div v-else class="error">无法获取日志</div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="logsDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 镜像列表 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>镜像列表</span>
          <el-button type="primary" size="small" @click="showPullImageDialog = true">
            拉取镜像
          </el-button>
        </div>
      </template>
      <div class="images-info">
        <el-table :data="images" style="width: 100%">
          <el-table-column prop="id" label="镜像ID" width="120">
            <template #default="scope">
              {{ scope.row.id.substring(7, 19) }}
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="标签">
            <template #default="scope">
              <div v-for="(tag, index) in scope.row.tags" :key="index">
                {{ tag }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="size" label="大小">
            <template #default="scope">
              {{ formatBytes(scope.row.size) }}
            </template>
          </el-table-column>
          <el-table-column prop="created" label="创建时间" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button 
                type="danger" 
                size="small" 
                @click="handleDeleteImage(scope.row.id)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 拉取镜像 -->
    <el-dialog
      v-model="showPullImageDialog"
      title="拉取镜像"
      width="50%"
    >
      <el-form :model="pullImageForm" :rules="pullImageRules" ref="pullImageFormRef" label-width="80px">
        <el-form-item label="镜像名称" prop="image_name">
          <el-input v-model="pullImageForm.image_name" placeholder="例如: nginx:latest" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPullImageDialog = false">取消</el-button>
          <el-button type="primary" @click="handlePullImage" :loading="pullImageLoading">
            拉取
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { dockerApi } from '../services/api'

// 容器列表
const containers = ref([])

// 镜像列表
const images = ref([])

// 容器日志
const logsDialogVisible = ref(false)
const selectedContainerName = ref('')
const containerLogs = ref('')
const logsLoading = ref(false)

// 拉取镜像
const showPullImageDialog = ref(false)
const pullImageFormRef = ref()
const pullImageLoading = ref(false)
const pullImageForm = ref({
  image_name: ''
})

const pullImageRules = {
  image_name: [
    { required: true, message: '请输入镜像名称', trigger: 'blur' }
  ]
}

// 定时器
let updateTimer: number | undefined

// 加载容器列表
const loadContainers = async () => {
  try {
    const data = await dockerApi.getContainers()
    containers.value = data
  } catch (error) {
    console.error('加载容器列表失败:', error)
  }
}

// 加载镜像列表
const loadImages = async () => {
  try {
    const data = await dockerApi.getImages()
    images.value = data
  } catch (error) {
    console.error('加载镜像列表失败:', error)
  }
}

// 加载所有数据
const loadAllData = () => {
  loadContainers()
  loadImages()
}

// 获取容器状态类型
const getContainerStatusType = (status: string): string => {
  switch (status) {
    case 'running':
      return 'success'
    case 'exited':
      return 'info'
    case 'created':
      return 'warning'
    default:
      return 'danger'
  }
}

// 启动容器
const handleStartContainer = async (containerId: string) => {
  try {
    const response = await dockerApi.startContainer(containerId)
    if (response.success) {
      // 重新加载容器列表
      loadContainers()
    }
  } catch (error) {
    console.error('启动容器失败:', error)
  }
}

// 停止容器
const handleStopContainer = async (containerId: string) => {
  try {
    const response = await dockerApi.stopContainer(containerId)
    if (response.success) {
      // 重新加载容器列表
      loadContainers()
    }
  } catch (error) {
    console.error('停止容器失败:', error)
  }
}

// 重启容器
const handleRestartContainer = async (containerId: string) => {
  try {
    const response = await dockerApi.restartContainer(containerId)
    if (response.success) {
      // 重新加载容器列表
      loadContainers()
    }
  } catch (error) {
    console.error('重启容器失败:', error)
  }
}

// 查看容器日志
const handleViewLogs = async (containerId: string, containerName: string) => {
  selectedContainerName.value = containerName
  logsLoading.value = true
  containerLogs.value = ''
  logsDialogVisible.value = true
  
  try {
    const response = await dockerApi.getContainerLogs(containerId, 1000)
    if (response.success) {
      containerLogs.value = response.logs
    }
  } catch (error) {
    console.error('获取容器日志失败:', error)
  } finally {
    logsLoading.value = false
  }
}

// 删除镜像
const handleDeleteImage = async (imageId: string) => {
  try {
    const response = await dockerApi.deleteImage(imageId)
    if (response.success) {
      // 重新加载镜像列表
      loadImages()
    }
  } catch (error) {
    console.error('删除镜像失败:', error)
  }
}

// 拉取镜像
const handlePullImage = async () => {
  if (!pullImageFormRef.value) return
  
  // 表单验证
  await pullImageFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      pullImageLoading.value = true
      
      try {
        const response = await dockerApi.pullImage(pullImageForm.value.image_name)
        if (response.success) {
          // 重新加载镜像列表
          loadImages()
          showPullImageDialog.value = false
        }
      } catch (error) {
        console.error('拉取镜像失败:', error)
      } finally {
        pullImageLoading.value = false
      }
    }
  })
}

// 格式化字节
const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 组件挂载时加载数据
onMounted(() => {
  loadAllData()
  // 每5秒更新一次数据
  updateTimer = window.setInterval(loadAllData, 5000)
})

// 组件卸载时清除定时器
onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
})
</script>

<style scoped>
.docker-page {
  padding: 20px 0;
}

.metric-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.containers-info,
.images-info {
  padding: 10px 0;
}

.logs-content {
  max-height: 500px;
  overflow-y: auto;
}

.logs-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
}

.loading,
.error {
  text-align: center;
  padding: 20px;
}

.loading {
  color: #409eff;
}

.error {
  color: #f56c6c;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>
