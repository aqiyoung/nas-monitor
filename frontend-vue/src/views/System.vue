<template>
  <div class="system-page">
    <h2>系统状态</h2>
    
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

    <!-- 磁盘S.M.A.R.T信息 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>磁盘S.M.A.R.T信息</span>
        </div>
      </template>
      <div class="smart-info">
        <div v-if="diskSmartInfo.error">
          <el-alert
            :title="diskSmartInfo.error"
            type="warning"
            show-icon
          />
        </div>
        <div v-else-if="diskSmartInfo.length === 0">
          <span>未检测到磁盘</span>
        </div>
        <div v-else>
          <el-tabs type="border-card">
            <el-tab-pane 
              v-for="(disk, index) in diskSmartInfo" 
              :key="index" 
              :label="disk.device"
            >
              <div class="disk-smart-details">
                <div class="smart-item">
                  <span class="label">型号:</span>
                  <span class="value">{{ disk.model }}</span>
                </div>
                <div class="smart-item">
                  <span class="label">序列号:</span>
                  <span class="value">{{ disk.serial }}</span>
                </div>
                <div class="smart-item">
                  <span class="label">固件版本:</span>
                  <span class="value">{{ disk.firmware }}</span>
                </div>
                <div class="smart-item">
                  <span class="label">接口:</span>
                  <span class="value">{{ disk.interface }}</span>
                </div>
                <div class="smart-item">
                  <span class="label">容量:</span>
                  <span class="value">{{ disk.size }}</span>
                </div>
                <div class="smart-item">
                  <span class="label">健康状态:</span>
                  <span class="value" :class="getHealthClass(disk.health)">{{ disk.health }}</span>
                </div>
                <div class="smart-item" v-if="disk.temperature">
                  <span class="label">温度:</span>
                  <span class="value">{{ disk.temperature }}°C</span>
                </div>
                
                <div class="smart-attributes" v-if="disk.smart_attributes.length > 0">
                  <h4>S.M.A.R.T属性</h4>
                  <el-table :data="disk.smart_attributes" style="width: 100%">
                    <el-table-column prop="id" label="ID" width="80" />
                    <el-table-column prop="name" label="名称" />
                    <el-table-column prop="value" label="当前值" width="100" />
                    <el-table-column prop="worst" label="最差值" width="100" />
                    <el-table-column prop="threshold" label="阈值" width="100" />
                    <el-table-column prop="raw_value" label="原始值" />
                    <el-table-column prop="status" label="状态" width="100">
                      <template #default="scope">
                        <span :class="getHealthClass(scope.row.status)">{{ scope.row.status }}</span>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { systemApi } from '../services/api'

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

// 磁盘使用率
const diskUsage = ref([])

// 磁盘S.M.A.R.T信息
const diskSmartInfo = ref([])

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

// 加载磁盘使用率
const loadDiskUsage = async () => {
  try {
    const data = await systemApi.getDiskUsage()
    diskUsage.value = data
  } catch (error) {
    console.error('加载磁盘使用率失败:', error)
  }
}

// 加载磁盘S.M.A.R.T信息
const loadDiskSmartInfo = async () => {
  try {
    const data = await systemApi.getDiskSmartInfo()
    diskSmartInfo.value = data
  } catch (error) {
    console.error('加载磁盘S.M.A.R.T信息失败:', error)
    diskSmartInfo.value = { error: '加载失败' }
  }
}

// 加载所有数据
const loadAllData = () => {
  loadSystemInfo()
  loadCpuUsage()
  loadMemoryUsage()
  loadDiskUsage()
  loadDiskSmartInfo()
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

// 获取健康状态类名
const getHealthClass = (status: string): string => {
  if (status.includes('OK') || status.includes('良好')) {
    return 'status-ok'
  } else if (status.includes('Warning') || status.includes('警告')) {
    return 'status-warning'
  } else {
    return 'status-error'
  }
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
.system-page {
  padding: 20px 0;
}

.system-info-card {
  margin-bottom: 20px;
}

.system-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.value {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.metric-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cpu-info {
  padding: 10px 0;
}

.cpu-total {
  margin-bottom: 15px;
}

.cpu-cores {
  margin-top: 10px;
}

.core-item {
  margin-bottom: 10px;
}

.core-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
  display: block;
}

.memory-info {
  padding: 10px 0;
}

.memory-total {
  margin-bottom: 15px;
}

.memory-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.memory-item {
  display: flex;
  justify-content: space-between;
}

.disk-info {
  padding: 10px 0;
}

.disk-item {
  margin-bottom: 15px;
}

.disk-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.disk-details {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.smart-info {
  padding: 10px 0;
}

.disk-smart-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.smart-item {
  display: flex;
  justify-content: space-between;
}

.smart-attributes {
  margin-top: 20px;
}

.status-ok {
  color: #67C23A;
}

.status-warning {
  color: #E6A23C;
}

.status-error {
  color: #F56C6C;
}

@media (max-width: 768px) {
  .system-info {
    grid-template-columns: 1fr;
  }
}
</style>
