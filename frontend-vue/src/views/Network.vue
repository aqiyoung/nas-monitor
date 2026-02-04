<template>
  <div class="network-page">
    <h2>网络监控</h2>
    
    <!-- 网络流量 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>网络流量</span>
        </div>
      </template>
      <div class="network-info">
        <div class="network-item">
          <span class="label">发送字节:</span>
          <span class="value">{{ formatBytes(networkTraffic.bytes_sent) }}</span>
        </div>
        <div class="network-item">
          <span class="label">接收字节:</span>
          <span class="value">{{ formatBytes(networkTraffic.bytes_recv) }}</span>
        </div>
        <div class="network-item">
          <span class="label">发送数据包:</span>
          <span class="value">{{ networkTraffic.packets_sent }}</span>
        </div>
        <div class="network-item">
          <span class="label">接收数据包:</span>
          <span class="value">{{ networkTraffic.packets_recv }}</span>
        </div>
        <div class="network-item">
          <span class="label">输入错误:</span>
          <span class="value">{{ networkTraffic.errin }}</span>
        </div>
        <div class="network-item">
          <span class="label">输出错误:</span>
          <span class="value">{{ networkTraffic.errout }}</span>
        </div>
        <div class="network-item">
          <span class="label">WiFi名称:</span>
          <span class="value">{{ networkTraffic.wifi_name || '未连接' }}</span>
        </div>
      </div>
    </el-card>

    <!-- 网络接口 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>网络接口</span>
        </div>
      </template>
      <div class="interfaces-info">
        <el-table :data="networkInterfaces" style="width: 100%">
          <el-table-column prop="name" label="接口名称" />
          <el-table-column prop="mac_address" label="MAC地址" />
          <el-table-column prop="is_up" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.is_up ? 'success' : 'danger'">
                {{ scope.row.is_up ? 'UP' : 'DOWN' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="speed" label="速度" />
          <el-table-column prop="mtu" label="MTU" />
          <el-table-column prop="ip_addresses" label="IP地址">
            <template #default="scope">
              <div v-for="(ip, index) in scope.row.ip_addresses" :key="index">
                {{ ip.ip }}
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 网络抓包 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>网络抓包</span>
        </div>
      </template>
      <div class="capture-info">
        <el-form :model="captureForm" :rules="captureRules" ref="captureFormRef" label-width="80px">
          <el-form-item label="接口" prop="interface">
            <el-select v-model="captureForm.interface" placeholder="选择网络接口">
              <el-option 
                v-for="iface in networkInterfaces" 
                :key="iface.name" 
                :label="iface.name" 
                :value="iface.name"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="时长" prop="duration">
            <el-input-number v-model="captureForm.duration" :min="1" :max="3600" :step="1" placeholder="抓包时长（秒）" />
          </el-form-item>
          
          <el-form-item label="输出文件">
            <el-input v-model="captureForm.output_file" placeholder="网络抓包日志文件" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleCapture" :loading="captureLoading">
              开始抓包
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="capture-result" v-if="captureResult">
          <el-alert
            :title="captureResult.success ? '抓包成功' : '抓包失败'"
            :type="captureResult.success ? 'success' : 'error'"
            :description="captureResult.message || captureResult.error"
            show-icon
          />
        </div>
      </div>
    </el-card>

    <!-- 网络日志 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>网络日志</span>
        </div>
      </template>
      <div class="logs-info">
        <el-form :model="logsForm" ref="logsFormRef" label-width="80px">
          <el-form-item label="日志文件">
            <el-input v-model="logsForm.log_file" placeholder="网络日志文件" />
          </el-form-item>
          
          <el-form-item label="行数">
            <el-input-number v-model="logsForm.lines" :min="1" :max="1000" :step="10" placeholder="显示行数" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleGetLogs" :loading="logsLoading">
              获取日志
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="logs-result" v-if="logsResult">
          <div v-if="logsResult.success">
            <el-collapse>
              <el-collapse-item title="网络日志">
                <pre>{{ logsResult.logs.join('\n') }}</pre>
              </el-collapse-item>
            </el-collapse>
          </div>
          <div v-else>
            <el-alert
              :title="'获取日志失败'"
              type="error"
              :description="logsResult.error"
              show-icon
            />
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { networkApi } from '../services/api'

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

// 网络接口
const networkInterfaces = ref([])

// 抓包表单
const captureFormRef = ref()
const captureLoading = ref(false)
const captureResult = ref(null)
const captureForm = ref({
  interface: '',
  duration: 60,
  output_file: 'network_capture.log'
})

const captureRules = {
  interface: [
    { required: true, message: '请选择网络接口', trigger: 'blur' }
  ],
  duration: [
    { required: true, message: '请输入抓包时长', trigger: 'blur' }
  ]
}

// 日志表单
const logsFormRef = ref()
const logsLoading = ref(false)
const logsResult = ref(null)
const logsForm = ref({
  log_file: 'network_capture.log',
  lines: 100
})

// 定时器
let updateTimer: number | undefined

// 加载网络流量
const loadNetworkTraffic = async () => {
  try {
    const data = await networkApi.getTraffic()
    networkTraffic.value = data
  } catch (error) {
    console.error('加载网络流量失败:', error)
  }
}

// 加载网络接口
const loadNetworkInterfaces = async () => {
  try {
    const data = await networkApi.getInterfaces()
    networkInterfaces.value = data
  } catch (error) {
    console.error('加载网络接口失败:', error)
  }
}

// 加载所有数据
const loadAllData = () => {
  loadNetworkTraffic()
  loadNetworkInterfaces()
}

// 开始抓包
const handleCapture = async () => {
  if (!captureFormRef.value) return
  
  // 表单验证
  await captureFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      captureLoading.value = true
      captureResult.value = null
      
      try {
        // 调用抓包API
        const response = await networkApi.capturePackets(captureForm.value)
        captureResult.value = response
      } catch (error: any) {
        console.error('抓包失败:', error)
        captureResult.value = {
          success: false,
          error: error.response?.data?.error || '抓包失败'
        }
      } finally {
        captureLoading.value = false
      }
    }
  })
}

// 获取日志
const handleGetLogs = async () => {
  logsLoading.value = true
  logsResult.value = null
  
  try {
    // 调用获取日志API
    const response = await networkApi.getLogs(logsForm.value)
    logsResult.value = response
  } catch (error: any) {
    console.error('获取日志失败:', error)
    logsResult.value = {
      success: false,
      error: error.response?.data?.error || '获取日志失败'
    }
  } finally {
    logsLoading.value = false
  }
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
.network-page {
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

.network-info {
  padding: 10px 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.network-item {
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

.interfaces-info {
  padding: 10px 0;
}

.capture-info {
  padding: 10px 0;
}

.capture-result {
  margin-top: 20px;
}

.logs-info {
  padding: 10px 0;
}

.logs-result {
  margin-top: 20px;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  max-height: 400px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .network-info {
    grid-template-columns: 1fr;
  }
}
</style>
