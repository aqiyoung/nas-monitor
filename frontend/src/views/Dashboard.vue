<template>
  <div class="dashboard">
    <h2>仪表盘</h2>
    
    <!-- 系统基本信息 -->
    <el-card class="system-info-card">
      <template #header>
        <div class="card-header">
          <span>系统基本信息</span>
        </div>
      </template>
      <div class="system-info">
        <div class="info-item">
          <span class="label">主机名:</span>
          <span class="value">{{ systemInfo.hostname || '加载中...' }}</span>
        </div>
        <div class="info-item">
          <span class="label">操作系统:</span>
          <span class="value">{{ systemInfo.os }} {{ systemInfo.os_version }}</span>
        </div>
        <div class="info-item">
          <span class="label">架构:</span>
          <span class="value">{{ systemInfo.architecture }}</span>
        </div>
        <div class="info-item">
          <span class="label">启动时间:</span>
          <span class="value">{{ systemInfo.boot_time }}</span>
        </div>
        <div class="info-item">
          <span class="label">运行时间:</span>
          <span class="value">{{ systemInfo.uptime }}</span>
        </div>
      </div>
    </el-card>

    <!-- 核心指标卡片 -->
    <div class="metrics-grid">
      <!-- CPU使用率 -->
      <el-card class="metric-card">
        <template #header>
          <div class="card-header">
            <span>CPU使用率</span>
          </div>
        </template>
        <div class="cpu-info">
          <div class="cpu-total">
            <el-progress 
              :percentage="cpuUsage.total_usage" 
              :format="formatProgress" 
              :color="getProgressColor(cpuUsage.total_usage)"
            />
          </div>
          <div class="cpu-cores" v-if="cpuUsage.per_core_usage.length > 0">
            <div class="core-item" v-for="(usage, index) in cpuUsage.per_core_usage" :key="index">
              <span class="core-label">核心 {{ index + 1 }}:</span>
              <el-progress 
                :percentage="usage" 
                :format="formatProgress" 
                :color="getProgressColor(usage)"
                :stroke-width="6"
              />
            </div>
          </div>
        </div>
      </el-card>

      <!-- 内存使用率 -->
      <el-card class="metric-card">
        <template #header>
          <div class="card-header">
            <span>内存使用率</span>
          </div>
        </template>
        <div class="memory-info">
          <div class="memory-total">
            <el-progress 
              :percentage="memoryUsage.memory.percent" 
              :format="formatProgress" 
              :color="getProgressColor(memoryUsage.memory.percent)"
            />
          </div>
          <div class="memory-details">
            <div class="memory-item">
              <span class="label">已用:</span>
              <span class="value">{{ formatBytes(memoryUsage.memory.used) }}</span>
            </div>
            <div class="memory-item">
              <span class="label">可用:</span>
              <span class="value">{{ formatBytes(memoryUsage.memory.available) }}</span>
            </div>
            <div class="memory-item">
              <span class="label">总量:</span>
              <span class="value">{{ formatBytes(memoryUsage.memory.total) }}</span>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 网络流量 -->
      <el-card class="metric-card">
        <template #header>
          <div class="card-header">
            <span>网络流量</span>
          </div>
        </template>
        <div class="network-info">
          <div class="network-item">
            <span class="label">发送:</span>
            <span class="value">{{ formatBytes(networkTraffic.bytes_sent) }}</span>
          </div>
          <div class="network-item">
            <span class="label">接收:</span>
            <span class="value">{{ formatBytes(networkTraffic.bytes_recv) }}</span>
          </div>
          <div class="network-item">
            <span class="label">WiFi名称:</span>
            <span class="value">{{ networkTraffic.wifi_name || '未连接' }}</span>
          </div>
        </div>
      </el-card>

      <!-- 磁盘使用率 -->
      <el-card class="metric-card">
        <template #header>
          <div class="card-header">
            <span>磁盘使用率</span>
          </div>
        </template>
        <div class="disk-info">
          <div class="disk-item" v-for="(disk, index) in diskUsage" :key="index">
            <div class="disk-label">
              <span>{{ disk.mountpoint }}</span>
            </div>
            <el-progress 
              :percentage="disk.percent" 
              :format="formatProgress" 
              :color="getProgressColor(disk.percent)"
            />
            <div class="disk-details">
              <span class="value">{{ formatBytes(disk.used) }} / {{ formatBytes(disk.total) }}</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Docker容器状态 -->
    <el-card class="docker-card">
      <template #header>
        <div class="card-header">
          <span>Docker容器状态</span>
        </div>
      </template>
      <div class="docker-info">
        <div class="docker-stats" v-if="dockerStats.length > 0">
          <div class="container-item" v-for="container in dockerStats" :key="container.name">
            <div class="container-header">
              <span class="container-name">{{ container.name }}</span>
            </div>
            <div class="container-metrics">
              <div class="metric">
                <span class="label">CPU:</span>
                <span class="value">{{ container.cpu_usage }}%</span>
              </div>
              <div class="metric">
                <span class="label">内存:</span>
                <span class="value">{{ formatBytes(container.memory_usage) }} / {{ formatBytes(container.memory_limit) }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          <span>没有运行中的容器</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { systemApi, networkApi, dockerApi } from '../services/api'

// 系统信息
const systemInfo = ref({
  hostname: '',
  os: '',
  os_version: '',
  architecture: '',
  boot_time: '',
  uptime: ''
})

// CPU使用率
const cpuUsage = ref({
  total_usage: 0,
  per_core_usage: [],
  cpu_count: {
    physical: 0,
    logical: 0
  }
})

// 内存使用率
const memoryUsage = ref({
  memory: {
    total: 0,
    available: 0,
    used: 0,
    percent: 0
  },
  swap: {
    total: 0,
    used: 0,
    free: 0,
    percent: 0
  }
})

// 网络流量
const networkTraffic = ref({
  bytes_sent: 0,
  bytes_recv: 0,
  packets_sent: 0,
  packets_recv: 0,
  errin: 0,
  errout: 0,
  dropin: 0,
  dropout: 0,
  wifi_name: null
})

// 磁盘使用率
const diskUsage = ref([])

// Docker容器状态
const dockerStats = ref([])

// 定时器
let updateTimer: number | undefined

// 加载系统信息
const loadSystemInfo = async () => {
  try {
    const data = await systemApi.getStatus()
    systemInfo.value = data
  } catch (error) {
    console.error('加载系统信息失败:', error)
  }
}

// 加载CPU使用率
const loadCpuUsage = async () => {
  try {
    const data = await systemApi.getCpuUsage()
    cpuUsage.value = data
  } catch (error) {
    console.error('加载CPU使用率失败:', error)
  }
}

// 加载内存使用率
const loadMemoryUsage = async () => {
  try {
    const data = await systemApi.getMemoryUsage()
    memoryUsage.value = data
  } catch (error) {
    console.error('加载内存使用率失败:', error)
  }
}

// 加载网络流量
const loadNetworkTraffic = async () => {
  try {
    const data = await networkApi.getTraffic()
    networkTraffic.value = data
  } catch (error) {
    console.error('加载网络流量失败:', error)
  }
}

// 加载磁盘使用率
const loadDiskUsage = async () => {
  try {
    const data = await systemApi.getDiskUsage()
    diskUsage.value = data
  } catch (error) {
    console.error('加载磁盘使用率失败:', error)
  }
}

// 加载Docker容器状态
const loadDockerStats = async () => {
  try {
    const data = await dockerApi.getStats()
    dockerStats.value = data
  } catch (error) {
    console.error('加载Docker容器状态失败:', error)
  }
}

// 加载所有数据
const loadAllData = () => {
  loadSystemInfo()
  loadCpuUsage()
  loadMemoryUsage()
  loadNetworkTraffic()
  loadDiskUsage()
  loadDockerStats()
}

// 格式化字节
const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化进度条
const formatProgress = (percentage: number): string => {
  return `${percentage.toFixed(1)}%`
}

// 获取进度条颜色
const getProgressColor = (percentage: number): string => {
  if (percentage > 80) return '#F56C6C'
  if (percentage > 50) return '#E6A23C'
  return '#67C23A'
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
/* 主容器 */
.dashboard {
  padding: 0;
  min-height: 100%;
}

/* 页面标题 */
.dashboard h2 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.dashboard h2::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(180deg, #409EFF 0%, #69c0ff 100%);
  border-radius: 2px;
}

/* 系统信息卡片 */
.system-info-card {
  margin-bottom: 24px;
  border-radius: 12px !important;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

.system-info-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  height: 48px;
}

.card-header span {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 系统信息网格 */
.system-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

/* 信息项 */
.info-item {
  display: flex;
  flex-direction: column;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-item:hover {
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-color: #409EFF;
}

/* 标签和值 */
.label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 400;
}

.value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
}

/* 指标网格 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

/* 指标卡片 */
.metric-card {
  min-height: 220px;
  border-radius: 12px !important;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

.metric-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* CPU信息 */
.cpu-info {
  padding: 20px 0;
}

.cpu-total {
  margin-bottom: 20px;
}

.cpu-cores {
  margin-top: 16px;
}

.core-item {
  margin-bottom: 12px;
}

.core-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  display: block;
  font-weight: 500;
}

/* 内存信息 */
.memory-info {
  padding: 20px 0;
}

.memory-total {
  margin-bottom: 20px;
}

.memory-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.memory-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.memory-item .value {
  font-size: 16px;
  font-weight: 500;
  color: #409EFF;
}

/* 网络信息 */
.network-info {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.network-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.network-item:hover {
  background-color: white;
  border-color: #409EFF;
}

.network-item .value {
  font-size: 16px;
  font-weight: 500;
  color: #67C23A;
}

/* 磁盘信息 */
.disk-info {
  padding: 20px 0;
}

.disk-item {
  margin-bottom: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.disk-item:hover {
  background-color: white;
  border-color: #409EFF;
}

.disk-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 12px;
  font-weight: 500;
}

.disk-details {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
  text-align: right;
}

/* Docker卡片 */
.docker-card {
  margin-top: 24px;
  border-radius: 12px !important;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

.docker-card:hover {
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.docker-info {
  padding: 20px 0;
}

/* Docker容器状态 */
.docker-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.container-item {
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.container-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
  transform: translateY(-2px);
}

.container-header {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}

.container-name {
  font-weight: 600;
  color: #303133;
  font-size: 16px;
}

.container-metrics {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric .label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 0;
}

.metric .value {
  font-size: 15px;
  font-weight: 500;
  color: #409EFF;
}

/* 无数据状态 */
.no-data {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #e9ecef;
  margin: 20px 0;
}

.no-data::before {
  content: '';
  display: block;
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23c0c4cc"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14h-2v-4H8v-2h2V9h2v2h2v2h-2v4z"/></svg>') no-repeat center;
  background-size: contain;
}

/* 进度条样式 */
:deep(.el-progress__text) {
  font-size: 14px !important;
  font-weight: 500 !important;
  color: #303133 !important;
}

:deep(.el-progress-bar__outer) {
  border-radius: 10px !important;
  overflow: hidden !important;
  background-color: #f0f2f5 !important;
}

:deep(.el-progress-bar__inner) {
  border-radius: 10px !important;
  transition: width 1s ease-in-out !important;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .metrics-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 0;
  }
  
  .dashboard h2 {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .system-info {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
  }
  
  .docker-stats {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .metric-card,
  .system-info-card,
  .docker-card {
    margin-bottom: 16px;
  }
  
  .card-header span {
    font-size: 14px;
  }
}

/* 加载动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.info-item.loading,
.memory-details.loading,
.network-item.loading,
.disk-item.loading,
.container-item.loading {
  animation: pulse 1.5s ease-in-out infinite;
}
</style>
