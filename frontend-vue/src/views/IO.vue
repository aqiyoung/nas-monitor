<template>
  <div class="io-page">
    <h2>IO状态</h2>
    
    <!-- IO统计信息 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>IO统计信息</span>
        </div>
      </template>
      <div class="io-info">
        <div v-if="ioStats.error">
          <el-alert
            :title="ioStats.error"
            type="warning"
            show-icon
          />
        </div>
        <div v-else-if="Object.keys(ioStats).length === 0">
          <span>未获取到IO统计信息</span>
        </div>
        <div v-else>
          <el-tabs type="border-card">
            <el-tab-pane label="系统总IO">
              <div class="io-details">
                <div class="io-item">
                  <span class="label">读取字节:</span>
                  <span class="value">{{ formatBytes(ioStats.read_bytes) }}</span>
                </div>
                <div class="io-item">
                  <span class="label">写入字节:</span>
                  <span class="value">{{ formatBytes(ioStats.write_bytes) }}</span>
                </div>
                <div class="io-item">
                  <span class="label">读取次数:</span>
                  <span class="value">{{ ioStats.read_count }}</span>
                </div>
                <div class="io-item">
                  <span class="label">写入次数:</span>
                  <span class="value">{{ ioStats.write_count }}</span>
                </div>
                <div class="io-item">
                  <span class="label">读取时间:</span>
                  <span class="value">{{ ioStats.read_time }} ms</span>
                </div>
                <div class="io-item">
                  <span class="label">写入时间:</span>
                  <span class="value">{{ ioStats.write_time }} ms</span>
                </div>
              </div>
            </el-tab-pane>
            <el-tab-pane 
              v-for="(disk, diskName) in ioStats.disks" 
              :key="diskName" 
              :label="diskName"
            >
              <div class="io-details">
                <div class="io-item">
                  <span class="label">读取字节:</span>
                  <span class="value">{{ formatBytes(disk.read_bytes) }}</span>
                </div>
                <div class="io-item">
                  <span class="label">写入字节:</span>
                  <span class="value">{{ formatBytes(disk.write_bytes) }}</span>
                </div>
                <div class="io-item">
                  <span class="label">读取次数:</span>
                  <span class="value">{{ disk.read_count }}</span>
                </div>
                <div class="io-item">
                  <span class="label">写入次数:</span>
                  <span class="value">{{ disk.write_count }}</span>
                </div>
                <div class="io-item">
                  <span class="label">读取时间:</span>
                  <span class="value">{{ disk.read_time }} ms</span>
                </div>
                <div class="io-item">
                  <span class="label">写入时间:</span>
                  <span class="value">{{ disk.write_time }} ms</span>
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
import { ioApi } from '../services/api'

// IO统计信息
const ioStats = ref({})

// 定时器
let updateTimer: number | undefined

// 加载IO统计信息
const loadIoStats = async () => {
  try {
    const data = await ioApi.getIoStats()
    ioStats.value = data
  } catch (error) {
    console.error('加载IO统计信息失败:', error)
    ioStats.value = { error: '加载失败' }
  }
}

// 加载所有数据
const loadAllData = () => {
  loadIoStats()
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
.io-page {
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

.io-info {
  padding: 10px 0;
}

.io-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.io-item {
  display: flex;
  justify-content: space-between;
}

.label {
  font-size: 14px;
  color: #606266;
}

.value {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

@media (max-width: 768px) {
  .io-details {
    grid-template-columns: 1fr;
  }
}
</style>
