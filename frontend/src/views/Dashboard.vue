<template>
  <div class="dashboard">
    <!-- 标签页 -->
    <el-tabs v-model="activeTab" class="status-tabs">
      <el-tab-pane label="总览" name="overview">
        <!-- 总览卡片 -->
        <div class="overview-cards">
          <!-- 系统信息卡片 -->
          <el-card class="overview-card system-card" @click="activeTab = 'overview'">
            <div class="card-title">
              <el-icon><Monitor /></el-icon>
              <span>threelnas</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">本次运行</span>
                <span class="value">{{ systemInfo.uptime }}</span>
              </div>
            </div>
          </el-card>

          <!-- CPU卡片 -->
          <el-card class="overview-card cpu-card" @click="activeTab = 'cpu'">
            <div class="card-title">
              <el-icon><Cpu /></el-icon>
              <span>CPU</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">温度</span>
                <span class="value">{{ cpuInfo.temperature }}°C</span>
              </div>
              <div class="gauge-container">
                <div class="gauge" :style="{ '--percentage': cpuInfo.usage + '%' }">
                  <div class="gauge-value">{{ cpuInfo.usage }}%</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 内存卡片 -->
          <el-card class="overview-card memory-card" @click="activeTab = 'memory'">
            <div class="card-title">
              <el-icon><DataAnalysis /></el-icon>
              <span>内存</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">可用</span>
                <span class="value">{{ memoryInfo.available }}</span>
              </div>
              <div class="gauge-container">
                <div class="gauge" :style="{ '--percentage': memoryInfo.usage + '%' }">
                  <div class="gauge-value">{{ memoryInfo.usage }}%</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 网络卡片 -->
          <el-card class="overview-card network-card" @click="activeTab = 'network'">
            <div class="card-title">
              <el-icon><Connection /></el-icon>
              <span>网络</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">发送</span>
                <span class="value">↑ {{ networkInfo.sent }}</span>
              </div>
              <div class="info-item">
                <span class="label">接收</span>
                <span class="value">↓ {{ networkInfo.received }}</span>
              </div>
            </div>
          </el-card>

          <!-- GPU卡片 -->
          <el-card class="overview-card gpu-card" @click="activeTab = 'gpu'">
            <div class="card-title">
              <el-icon><Monitor /></el-icon>
              <span>GPU</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">温度</span>
                <span class="value">-</span>
              </div>
              <div class="gauge-container">
                <div class="gauge" :style="{ '--percentage': gpuInfo.usage + '%' }">
                  <div class="gauge-value">{{ gpuInfo.usage }}%</div>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 硬盘卡片 -->
          <el-card class="overview-card disk-card" @click="activeTab = 'overview'">
            <div class="card-title">
              <el-icon><DataAnalysis /></el-icon>
              <span>硬盘</span>
            </div>
            <div class="card-content">
              <div class="info-item">
                <span class="label">读取</span>
                <span class="value">{{ diskInfo.read }}</span>
              </div>
              <div class="info-item">
                <span class="label">写入</span>
                <span class="value">{{ diskInfo.write }}</span>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 硬盘信息表格 -->
        <el-card class="disk-table-card">
          <template #header>
            <div class="card-header">
              <span>硬盘信息</span>
            </div>
          </template>
          <div class="disk-table">
            <el-table :data="diskTableData" style="width: 100%">
              <el-table-column prop="id" label="" width="50">
                <template #default="scope">
                  {{ scope.$index + 1 }}
                </template>
              </el-table-column>
              <el-table-column prop="type" label="内置硬盘">
                <template #default="scope">
                  <div class="disk-type">
                    <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=SSD%20hard%20disk%20icon&image_size=square" alt="SSD" class="disk-icon">
                    <span>{{ scope.row.capacity }}</span>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="temperature" label="温度" width="100">
                <template #default="scope">
                  {{ scope.row.temperature }}
                </template>
              </el-table-column>
              <el-table-column prop="busy" label="繁忙度" width="100">
                <template #default="scope">
                  {{ scope.row.busy }}
                </template>
              </el-table-column>
              <el-table-column prop="readSpeed" label="读取速度" width="120">
                <template #default="scope">
                  {{ scope.row.readSpeed }}
                </template>
              </el-table-column>
              <el-table-column prop="writeSpeed" label="写入速度" width="120">
                <template #default="scope">
                  {{ scope.row.writeSpeed }}
                </template>
              </el-table-column>
              <el-table-column prop="usage" label="用途">
                <template #default="scope">
                  {{ scope.row.usage }}
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="CPU" name="cpu">
        <div class="tab-content">
          <div class="cpu-details">
            <div class="cpu-header">
              <h3>CPU</h3>
              <div class="cpu-info">
                <span>Intel(R) Core(TM) m3-7Y30 CPU @ 1.00GHz</span>
                <span>2核 | 4线程</span>
              </div>
            </div>
            <div class="cpu-chart">
              <div class="chart-container">
                <div class="chart"></div>
              </div>
              <div class="cpu-stats">
                <div class="stat-item">
                  <div class="stat-label">利用率</div>
                  <div class="stat-value">
                    <span class="usage">{{ cpuInfo.usage }}%</span>
                    <div class="sub-stats">
                      <span>用户: 15%</span>
                      <span>系统: 9%</span>
                      <span>I/O等待: 0%</span>
                    </div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">CPU温度</div>
                  <div class="stat-value temperature">{{ cpuInfo.temperature }}°C</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">平均负载</div>
                  <div class="stat-value">
                    <span>1.05 /分钟</span>
                    <span>0.88 /5分钟</span>
                    <span>1.42 /15分钟</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="内存" name="memory">
        <div class="tab-content">
          <div class="memory-details">
            <div class="memory-header">
              <h3>内存</h3>
              <div class="memory-type">
                <span>物理内存</span>
                <el-dropdown>
                  <span class="el-dropdown-link">▼</span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item>物理内存</el-dropdown-item>
                      <el-dropdown-item>虚拟内存</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div class="memory-chart">
              <div class="chart-container">
                <div class="chart"></div>
              </div>
              <div class="memory-bar">
                <div class="bar-item system-reserved" style="width: 7%"></div>
                <div class="bar-item used" style="width: 63%"></div>
                <div class="bar-item buffer" style="width: 1%"></div>
                <div class="bar-item cache" style="width: 33%"></div>
                <div class="bar-item free" style="width: 3%"></div>
              </div>
              <div class="memory-legend">
                <div class="legend-item">
                  <span class="color system-reserved"></span>
                  <span>系统保留 281.7 MB</span>
                </div>
                <div class="legend-item">
                  <span class="color used"></span>
                  <span>已使用 2.5 GB</span>
                </div>
                <div class="legend-item">
                  <span class="color buffer"></span>
                  <span>缓冲 35.1 MB</span>
                </div>
                <div class="legend-item">
                  <span class="color cache"></span>
                  <span>缓存 1.3 GB</span>
                </div>
                <div class="legend-item">
                  <span class="color free"></span>
                  <span>空闲 124.2 MB</span>
                </div>
              </div>
              <div class="memory-stats">
                <div class="stat-item">
                  <div class="stat-label">利用率</div>
                  <div class="stat-value usage">{{ memoryInfo.usage }}%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">总大小</div>
                  <div class="stat-value">4 GB</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">已使用</div>
                  <div class="stat-value">2.54 GB</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">可用</div>
                  <div class="stat-value">{{ memoryInfo.available }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="网络" name="network">
        <div class="tab-content">
          <div class="network-details">
            <div class="network-header">
              <h3>网络总计</h3>
              <div class="network-settings">
                <span>网络设置</span>
              </div>
            </div>
            <div class="network-chart">
              <div class="chart-container">
                <div class="chart"></div>
              </div>
              <div class="network-stats">
                <div class="stat-item">
                  <div class="stat-label">接收速度</div>
                  <div class="stat-value received">678 B/s</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">发送速度</div>
                  <div class="stat-value sent">795 B/s</div>
                </div>
              </div>
              <div class="network-interfaces">
                <div class="interface">
                  <h4>网口1 - 43a65079c85-ovs</h4>
                  <div class="interface-chart">
                    <div class="chart"></div>
                  </div>
                </div>
                <div class="interface">
                  <h4>无线网卡2 - wlp2s0</h4>
                  <div class="interface-chart">
                    <div class="chart"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
      <el-tab-pane label="GPU" name="gpu">
        <div class="tab-content">
          <div class="gpu-details">
            <div class="gpu-header">
              <h3>GPU</h3>
              <div class="gpu-info">
                <span>Intel HD Graphics 615</span>
              </div>
            </div>
            <div class="gpu-chart">
              <div class="chart-container">
                <div class="chart"></div>
              </div>
              <div class="gpu-memory">
                <div class="memory-bar">
                  <div class="bar-item used" style="width: 1%"></div>
                  <div class="bar-item free" style="width: 99%"></div>
                </div>
                <div class="memory-legend">
                  <div class="legend-item">
                    <span class="color used"></span>
                    <span>已使用 448 KB</span>
                  </div>
                  <div class="legend-item">
                    <span class="color free"></span>
                    <span>空闲 3.72 GB</span>
                  </div>
                </div>
              </div>
              <div class="gpu-stats">
                <div class="stat-item">
                  <div class="stat-label">GPU 利用率</div>
                  <div class="stat-value usage">{{ gpuInfo.usage }}%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">显存利用率</div>
                  <div class="stat-value">0%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">Video</div>
                  <div class="stat-value">0%</div>
                </div>
                <div class="stat-item">
                  <div class="stat-label">Render</div>
                  <div class="stat-value">0%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import {
  Cpu,
  DataAnalysis,
  Connection,
  Monitor
} from '@element-plus/icons-vue'

// 激活的标签页
const activeTab = ref('overview')

// 系统信息
const systemInfo = ref({
  uptime: '0天 15时 56分 24秒'
})

// CPU信息
const cpuInfo = ref({
  temperature: 42,
  usage: 21
})

// 内存信息
const memoryInfo = ref({
  available: '1.18 GB',
  usage: 63
})

// 网络信息
const networkInfo = ref({
  sent: '908 B/s',
  received: '832 B/s'
})

// GPU信息
const gpuInfo = ref({
  usage: 0
})

// 硬盘信息
const diskInfo = ref({
  read: '0 B/s',
  write: '4 KB/s'
})

// 硬盘表格数据
const diskTableData = ref([
  {
    id: 1,
    type: 'SSD',
    capacity: '953.87 GB',
    temperature: '45°C',
    busy: '0%',
    readSpeed: '0 B/s',
    writeSpeed: '4 KB/s',
    usage: '系统安装、存储空间 1'
  },
  {
    id: 2,
    type: 'SSD',
    capacity: '119.24 GB',
    temperature: '28°C',
    busy: '0%',
    readSpeed: '0 B/s',
    writeSpeed: '0 B/s',
    usage: '挂载为外接存储'
  }
])

// 定时器
let updateTimer: number | undefined

// 生成随机数据
const getRandomValue = (min: number, max: number): number => {
  return Math.random() * (max - min) + min
}

// 模拟CPU信息
const mockCpuInfo = () => {
  return {
    temperature: Math.floor(getRandomValue(35, 50)),
    usage: Math.floor(getRandomValue(10, 30))
  }
}

// 模拟网络信息
const mockNetworkInfo = () => {
  return {
    sent: `${Math.floor(getRandomValue(500, 1500))} B/s`,
    received: `${Math.floor(getRandomValue(500, 1500))} B/s`
  }
}

// 模拟硬盘信息
const mockDiskInfo = () => {
  return {
    read: `${Math.floor(getRandomValue(0, 100))} B/s`,
    write: `${Math.floor(getRandomValue(0, 10))} KB/s`
  }
}

// 加载系统信息
const loadSystemInfo = async () => {
  try {
    // 系统信息保持不变
  } catch (error) {
    console.error('加载系统信息失败:', error)
  }
}

// 加载CPU信息
const loadCpuInfo = async () => {
  try {
    const data = mockCpuInfo()
    cpuInfo.value = data
  } catch (error) {
    console.error('加载CPU信息失败:', error)
  }
}

// 加载网络信息
const loadNetworkInfo = async () => {
  try {
    const data = mockNetworkInfo()
    networkInfo.value = data
  } catch (error) {
    console.error('加载网络信息失败:', error)
  }
}

// 加载硬盘信息
const loadDiskInfo = async () => {
  try {
    const data = mockDiskInfo()
    diskInfo.value = data
  } catch (error) {
    console.error('加载硬盘信息失败:', error)
  }
}

// 加载所有数据
const loadAllData = () => {
  loadSystemInfo()
  loadCpuInfo()
  loadNetworkInfo()
  loadDiskInfo()
}

// 组件挂载时加载数据
onMounted(async () => {
  // 先加载初始数据
  await loadAllData()
  
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
  padding: var(--spacing-md);
  height: 100%;
  min-height: 100%;
  background-color: var(--bg-secondary);
}

/* 标签页 */
.status-tabs {
  background-color: var(--bg-primary);
  border-radius: var(--border-radius-lg);
  margin: 0;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

:deep(.el-tabs__header) {
  margin: 0 !important;
  border-bottom: 1px solid var(--border-primary);
  background-color: var(--bg-primary);
  position: sticky;
  top: 0;
  z-index: 10;
}

:deep(.el-tabs__item) {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-regular);
  padding: 0 var(--spacing-lg);
  height: 56px;
  line-height: 56px;
  transition: all var(--transition-normal);
  position: relative;
}

:deep(.el-tabs__item:hover) {
  color: var(--primary-color);
  background-color: var(--bg-secondary);
}

:deep(.el-tabs__item.is-active) {
  color: var(--primary-color);
  font-weight: var(--font-weight-semibold);
  background-color: var(--primary-light);
}

:deep(.el-tabs__active-bar) {
  background-color: var(--primary-color);
  height: 3px;
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
}

/* 总览卡片容器 */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
}

/* 总览卡片 */
.overview-card {
  border-radius: var(--border-radius-lg) !important;
  border: none !important;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
  padding: var(--spacing-md) 0;
}

.overview-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--info-color));
  transform: scaleX(0);
  transition: transform var(--transition-normal);
}

.overview-card::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(51, 112, 255, 0.1) 0%, transparent 70%);
  transform: scale(0);
  transition: transform var(--transition-slow);
  border-radius: 50%;
}

.overview-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px) scale(1.02);
}

.overview-card:hover::before {
  transform: scaleX(1);
}

.overview-card:hover::after {
  transform: scale(1);
}

.overview-card:active {
  transform: translateY(-2px) scale(0.98);
  transition: transform var(--transition-fast);
}

/* 卡片标题 */
.card-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  padding: 0 var(--spacing-md) var(--spacing-sm);
  border-bottom: 1px solid var(--border-light);
}

.card-title i {
  font-size: 20px;
  color: var(--primary-color);
  transition: all var(--transition-normal);
}

.overview-card:hover .card-title i {
  transform: scale(1.1) rotate(5deg);
  color: var(--primary-active);
}

/* 卡片内容 */
.card-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding: 0 var(--spacing-md);
}

/* 信息项 */
.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xs) 0;
  transition: all var(--transition-fast);
}

.info-item:hover {
  background-color: rgba(51, 112, 255, 0.05);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
}

.info-item .label {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: var(--font-weight-normal);
  transition: color var(--transition-fast);
}

.info-item:hover .label {
  color: var(--text-regular);
}

.info-item .value {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.info-item:hover .value {
  color: var(--primary-color);
  transform: scale(1.05);
}

/* 仪表盘容器 */
.gauge-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
}

.overview-card:hover .gauge-container {
  background-color: var(--primary-light);
}

/* 仪表盘 */
.gauge {
  position: relative;
  width: 90px;
  height: 90px;
  transition: all var(--transition-normal);
}

.gauge::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: conic-gradient(var(--primary-color) var(--percentage), var(--border-primary) 0%);
  -webkit-mask: radial-gradient(transparent 60%, black 60%);
  mask: radial-gradient(transparent 60%, black 60%);
  transition: all var(--transition-normal);
}

.overview-card:hover .gauge::before {
  background: conic-gradient(var(--primary-active) var(--percentage), var(--border-secondary) 0%);
  transform: scale(1.05);
}

.gauge-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  transition: all var(--transition-normal);
}

.overview-card:hover .gauge-value {
  color: var(--primary-active);
  transform: translate(-50%, -50%) scale(1.1);
}

/* 硬盘表格卡片 */
.disk-table-card {
  margin: var(--spacing-lg) 0;
  border-radius: var(--border-radius-lg) !important;
  border: none !important;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-light);
}

/* 硬盘表格 */
.disk-table {
  padding: var(--spacing-lg);
  background-color: var(--bg-primary);
}

:deep(.el-table) {
  border-radius: var(--border-radius-md);
  overflow: hidden;
}

:deep(.el-table th) {
  background-color: var(--bg-secondary) !important;
  font-weight: var(--font-weight-semibold) !important;
  color: var(--text-primary) !important;
  border-bottom: 1px solid var(--border-primary) !important;
}

:deep(.el-table tr:hover) {
  background-color: var(--bg-secondary) !important;
}

:deep(.el-table td) {
  border-bottom: 1px solid var(--border-light) !important;
  transition: all var(--transition-fast);
}

:deep(.el-table td:hover) {
  background-color: var(--primary-light) !important;
}

/* 硬盘类型 */
.disk-type {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.disk-icon {
  width: 28px;
  height: 28px;
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.disk-type:hover .disk-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

/* 标签页内容 */
.tab-content {
  padding: var(--spacing-lg);
  min-height: 400px;
  background-color: var(--bg-secondary);
  border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
}

/* CPU详情 */
.cpu-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.cpu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-primary);
  margin-bottom: var(--spacing-lg);
}

.cpu-header h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.cpu-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background-color: var(--primary-color);
  border-radius: var(--border-radius-full);
}

.cpu-info {
  display: flex;
  gap: var(--spacing-lg);
  font-size: var(--font-size-sm);
  color: var(--text-regular);
  background-color: var(--bg-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.cpu-chart {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  background-color: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.cpu-chart::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--info-color));
}

.cpu-chart:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.chart-container {
  height: 250px;
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.chart-container:hover {
  background-color: var(--primary-light);
}

.chart {
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, var(--primary-light), var(--bg-secondary));
  position: relative;
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
}

.chart::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background-color: rgba(51, 112, 255, 0.3);
  transform: translateY(-50%);
}

.chart-container:hover .chart {
  background: linear-gradient(to bottom, var(--primary-color), var(--primary-light));
}

.cpu-stats {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.stat-item {
  flex: 1;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
  border: 1px solid var(--border-light);
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: var(--primary-color);
  transform: scaleY(0);
  transition: transform var(--transition-normal);
}

.stat-item::after {
  content: '';
  position: absolute;
  bottom: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(51, 112, 255, 0.1) 0%, transparent 70%);
  transform: scale(0);
  transition: transform var(--transition-slow);
  border-radius: 50%;
}

.stat-item:hover {
  background-color: var(--bg-primary);
  transform: translateY(-4px) scale(1.02);
  box-shadow: var(--shadow-card);
  border-color: var(--primary-color);
}

.stat-item:hover::before {
  transform: scaleY(1);
}

.stat-item:hover::after {
  transform: scale(1);
}

.stat-item:active {
  transform: translateY(-2px) scale(0.98);
  transition: transform var(--transition-fast);
}

.stat-label {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: var(--font-weight-normal);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all var(--transition-fast);
}

.stat-item:hover .stat-label {
  color: var(--primary-color);
  transform: translateX(4px);
}

.stat-value {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  transition: all var(--transition-normal);
}

.stat-item:hover .stat-value {
  transform: translateY(-2px);
}

.stat-value.usage {
  color: var(--warning-color);
}

.stat-value.temperature {
  color: var(--primary-color);
}

.stat-value.received {
  color: var(--success-color);
}

.stat-value.sent {
  color: var(--primary-color);
}

.sub-stats {
  display: flex;
  flex-direction: column;
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: var(--font-weight-normal);
  gap: 4px;
  transition: all var(--transition-fast);
}

.stat-item:hover .sub-stats {
  color: var(--text-regular);
  transform: translateX(4px);
}

/* 内存详情 */
.memory-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.memory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-primary);
  margin-bottom: var(--spacing-lg);
}

.memory-header h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.memory-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background-color: var(--success-color);
  border-radius: var(--border-radius-full);
}

.memory-type {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  color: var(--text-regular);
  background-color: var(--bg-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

:deep(.el-dropdown-link) {
  color: var(--primary-color);
  transition: all var(--transition-fast);
}

:deep(.el-dropdown-link:hover) {
  color: var(--primary-active);
  transform: scale(1.1);
}

.memory-chart {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  background-color: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.memory-chart::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--success-color), var(--warning-color));
}

.memory-chart:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.memory-bar {
  display: flex;
  height: 24px;
  border-radius: var(--border-radius-full);
  overflow: hidden;
  background-color: var(--border-light);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all var(--transition-normal);
}

.memory-chart:hover .memory-bar {
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.15);
}

.bar-item {
  height: 100%;
  transition: all var(--transition-slow);
  position: relative;
  overflow: hidden;
}

.bar-item::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left var(--transition-slow);
}

.bar-item:hover::after {
  left: 100%;
}

.bar-item.system-reserved {
  background-color: var(--info-color);
}

.bar-item.used {
  background-color: var(--primary-color);
}

.bar-item.buffer {
  background-color: var(--success-color);
}

.bar-item.cache {
  background-color: var(--warning-color);
}

.bar-item.free {
  background-color: var(--error-color);
}

.memory-legend {
  display: flex;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
  padding: var(--spacing-md);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
}

.memory-chart:hover .memory-legend {
  background-color: var(--bg-tertiary);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-sm);
  color: var(--text-regular);
  transition: all var(--transition-normal);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
}

.legend-item:hover {
  color: var(--text-primary);
  background-color: var(--bg-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.legend-item .color {
  width: 16px;
  height: 16px;
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-sm);
}

.legend-item:hover .color {
  transform: scale(1.2);
  box-shadow: var(--shadow-md);
}

.color.system-reserved {
  background-color: var(--info-color);
}

.color.used {
  background-color: var(--primary-color);
}

.color.buffer {
  background-color: var(--success-color);
}

.color.cache {
  background-color: var(--warning-color);
}

.color.free {
  background-color: var(--error-color);
}

.memory-stats {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

/* 网络详情 */
.network-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.network-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-primary);
  margin-bottom: var(--spacing-lg);
}

.network-header h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.network-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background-color: var(--info-color);
  border-radius: var(--border-radius-full);
}

.network-settings {
  font-size: var(--font-size-sm);
  color: var(--primary-color);
  cursor: pointer;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-focus);
  background-color: var(--primary-light);
}

.network-settings:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.network-chart {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  background-color: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.network-chart::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--info-color), var(--primary-color));
}

.network-chart:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.network-stats {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.network-interfaces {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

.interface {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  transition: all var(--transition-normal);
  border: 1px solid var(--border-light);
  position: relative;
  overflow: hidden;
}

.interface::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary-color), var(--success-color));
  transform: scaleX(0);
  transition: transform var(--transition-normal);
}

.interface:hover {
  background-color: var(--bg-primary);
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
  border-color: var(--primary-color);
}

.interface:hover::before {
  transform: scaleX(1);
}

.interface h4 {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  transition: all var(--transition-normal);
}

.interface:hover h4 {
  color: var(--primary-color);
  transform: translateX(4px);
}

.interface-chart {
  height: 120px;
  background-color: var(--bg-tertiary);
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.interface:hover .interface-chart {
  background-color: var(--primary-light);
}

.interface-chart .chart {
  background: linear-gradient(to bottom, var(--info-light), var(--bg-tertiary));
}

.interface:hover .interface-chart .chart {
  background: linear-gradient(to bottom, var(--primary-light), var(--info-light));
}

/* GPU详情 */
.gpu-details {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.gpu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-primary);
  margin-bottom: var(--spacing-lg);
}

.gpu-header h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.gpu-header h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background-color: var(--warning-color);
  border-radius: var(--border-radius-full);
}

.gpu-info {
  font-size: var(--font-size-sm);
  color: var(--text-regular);
  background-color: var(--bg-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.gpu-chart {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  background-color: var(--bg-primary);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.gpu-chart::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--warning-color), var(--error-color));
}

.gpu-chart:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.gpu-memory {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-normal);
}

.gpu-chart:hover .gpu-memory {
  background-color: var(--bg-tertiary);
}

.gpu-stats {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: var(--spacing-md);
  }
  
  .cpu-stats,
  .memory-stats,
  .network-stats,
  .gpu-stats {
    flex-wrap: wrap;
  }
  
  .network-interfaces {
    grid-template-columns: 1fr;
  }
  
  .stat-item {
    min-width: 150px;
  }
  
  .disk-table {
    padding: var(--spacing-md);
  }
  
  .tab-content {
    padding: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .status-tabs {
    margin: 0;
    border-radius: var(--border-radius-md);
  }
  
  .overview-cards {
    grid-template-columns: 1fr;
    padding: var(--spacing-md);
    gap: var(--spacing-md);
  }
  
  .disk-table-card {
    margin: var(--spacing-md) 0;
    border-radius: var(--border-radius-md) !important;
  }
  
  .disk-table {
    padding: var(--spacing-md);
  }
  
  .tab-content {
    padding: var(--spacing-md);
  }
  
  :deep(.el-tabs__item) {
    padding: 0 var(--spacing-md);
    font-size: var(--font-size-xs);
    height: 48px;
    line-height: 48px;
  }
  
  .cpu-header,
  .memory-header,
  .network-header,
  .gpu-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }
  
  .cpu-info,
  .memory-type,
  .gpu-info {
    width: 100%;
    flex-direction: column;
    gap: var(--spacing-xs);
    align-items: flex-start;
  }
  
  .cpu-stats,
  .memory-stats,
  .network-stats,
  .gpu-stats {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .network-interfaces {
    grid-template-columns: 1fr;
  }
  
  .stat-item {
    min-width: 100%;
  }
  
  .chart-container {
    height: 200px;
  }
  
  .interface-chart {
    height: 100px;
  }
  
  .memory-legend {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
  
  .legend-item {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .status-tabs {
    margin: 0;
    border-radius: var(--border-radius-sm);
  }
  
  .overview-cards {
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
  }
  
  .disk-table-card {
    margin: var(--spacing-sm) 0;
    border-radius: var(--border-radius-sm) !important;
  }
  
  .disk-table {
    padding: var(--spacing-sm);
  }
  
  .tab-content {
    padding: var(--spacing-sm);
  }
  
  :deep(.el-tabs__item) {
    padding: 0 var(--spacing-sm);
    font-size: 12px;
    height: 44px;
    line-height: 44px;
  }
  
  .card-title {
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
  }
  
  .card-title i {
    font-size: 16px;
  }
  
  .gauge {
    width: 70px;
    height: 70px;
  }
  
  .gauge::before {
    width: 70px;
    height: 70px;
  }
  
  .gauge-value {
    font-size: var(--font-size-md);
  }
  
  .chart-container {
    height: 160px;
  }
  
  .interface-chart {
    height: 80px;
  }
  
  .stat-item {
    padding: var(--spacing-md);
  }
  
  .stat-value {
    font-size: var(--font-size-lg);
  }
  
  .info-item .value {
    font-size: var(--font-size-sm);
  }
  
  .disk-type {
    gap: var(--spacing-sm);
  }
  
  .disk-icon {
    width: 24px;
    height: 24px;
  }
  
  :deep(.el-table th),
  :deep(.el-table td) {
    padding: var(--spacing-sm) !important;
    font-size: var(--font-size-xs);
  }
}

/* 可访问性增强 */
.overview-card:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.stat-item:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.network-settings:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

.interface:focus-visible {
  outline: var(--focus-outline);
  outline-offset: var(--focus-outline-offset);
}

/* 键盘导航增强 */
.overview-card:focus {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}

.stat-item:focus {
  background-color: var(--bg-primary);
  border-color: var(--primary-color);
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

.network-settings:focus {
  background-color: var(--primary-color);
  color: white;
  box-shadow: var(--shadow-md);
}

.interface:focus {
  background-color: var(--bg-primary);
  border-color: var(--primary-color);
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

/* 屏幕阅读器支持 */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .overview-card {
    border: 2px solid var(--border-primary-high-contrast) !important;
  }
  
  .stat-item {
    border: 2px solid var(--border-primary-high-contrast);
  }
  
  .interface {
    border: 2px solid var(--border-primary-high-contrast);
  }
  
  .network-settings {
    border: 2px solid var(--primary-color-high-contrast);
  }
  
  .disk-table-card {
    border: 2px solid var(--border-primary-high-contrast) !important;
  }
  
  :deep(.el-table th),
  :deep(.el-table td) {
    border-bottom: 2px solid var(--border-primary-high-contrast) !important;
  }
  
  :deep(.el-tabs__active-bar) {
    height: 4px;
  }
  
  :deep(.el-tabs__item) {
    border: 1px solid var(--border-primary-high-contrast);
    margin: 0 4px;
    border-radius: var(--border-radius-md) !important;
  }
  
  :deep(.el-tabs__item.is-active) {
    border-color: var(--primary-color-high-contrast);
  }
}

/* 减少动画模式支持 */
@media (prefers-reduced-motion: reduce) {
  .overview-card,
  .stat-item,
  .interface,
  .chart-container,
  .memory-bar,
  .bar-item,
  .legend-item {
    transition: none;
  }
  
  .overview-card:hover,
  .stat-item:hover,
  .interface:hover,
  .chart-container:hover,
  .legend-item:hover {
    transform: none;
  }
}
</style>
