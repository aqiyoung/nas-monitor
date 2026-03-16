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

    <!-- 主要内容区域 -->
    <div class="main-content-container">
      <!-- 左侧区域：CPU使用率 -->
      <div class="content-area left-area">
        <!-- CPU使用率 -->
        <el-card class="metric-card">
          <template #header>
            <div class="card-header">
              <span>CPU</span>
              <div class="cpu-header-info">
                <span class="cpu-usage">{{ cpuUsage.total_usage.toFixed(1) }}%</span>
                <span class="cpu-speed">{{ cpuSpeed }} GHz</span>
              </div>
            </div>
          </template>
          <div class="cpu-info">
            <!-- CPU使用率波形图 -->
            <div class="cpu-chart-container">
              <div ref="cpuChartRef" class="cpu-chart"></div>
            </div>
            <!-- CPU详细信息 -->
            <div class="cpu-details" v-if="cpuUsage.cpu_count">
              <div class="cpu-details-row">
                <div class="cpu-detail-item">
                  <span class="detail-label">利用率</span>
                  <span class="detail-value">{{ cpuUsage.total_usage.toFixed(1) }}%</span>
                </div>
                <div class="cpu-detail-item">
                  <span class="detail-label">速度</span>
                  <span class="detail-value">{{ cpuSpeed }} GHz</span>
                </div>
              </div>
              <div class="cpu-details-row">
                <div class="cpu-detail-item">
                  <span class="detail-label">核心</span>
                  <span class="detail-value">{{ cpuUsage.cpu_count.physical }}</span>
                </div>
                <div class="cpu-detail-item">
                  <span class="detail-label">线程</span>
                  <span class="detail-value">{{ cpuUsage.cpu_count.logical }}</span>
                </div>
              </div>
            </div>
            <!-- CPU核心使用率垂直柱状图 -->
            <div class="cpu-cores" v-if="cpuUsage.per_core_usage.length > 0">
              <div ref="cpuCoreChartRef" class="cpu-core-chart"></div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 右侧区域：内存、磁盘使用率和S.M.A.R.T信息 -->
      <div class="content-area right-area">
        <!-- 内存使用率 -->
        <el-card class="metric-card">
          <template #header>
            <div class="card-header">
              <span>内存</span>
              <div class="memory-header-info">
                <span class="memory-usage">{{ memoryUsage.memory.percent.toFixed(1) }}%</span>
                <span class="memory-total">{{ formatBytes(memoryUsage.memory.total) }}</span>
              </div>
            </div>
          </template>
          <div class="memory-info">
            <!-- 内存使用率波形图 -->
            <div class="memory-chart-container">
              <div ref="memoryChartRef" class="memory-chart"></div>
            </div>
            <!-- 内存详细信息 -->
            <div class="memory-details" v-if="memoryUsage.memory">
              <div class="memory-details-row">
                <div class="memory-detail-item">
                  <span class="detail-label">已用</span>
                  <span class="detail-value">{{ formatBytes(memoryUsage.memory.used) }}</span>
                </div>
                <div class="memory-detail-item">
                  <span class="detail-label">可用</span>
                  <span class="detail-value">{{ formatBytes(memoryUsage.memory.available) }}</span>
                </div>
              </div>
              <div class="memory-details-row">
                <div class="memory-detail-item">
                  <span class="detail-label">总量</span>
                  <span class="detail-value">{{ formatBytes(memoryUsage.memory.total) }}</span>
                </div>
                <div class="memory-detail-item">
                  <span class="detail-label">使用率</span>
                  <span class="detail-value">{{ memoryUsage.memory.percent.toFixed(1) }}%</span>
                </div>
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
    </div>

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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { systemApi, networkApi, dockerApi } from '../services/api'
import * as echarts from 'echarts'

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

// 磁盘S.M.A.R.T信息
const diskSmartInfo = ref([])

// Docker容器状态
const dockerStats = ref([])

// CPU波形图相关
const cpuChartRef = ref<HTMLElement | null>(null)
let cpuChart: echarts.ECharts | null = null
const cpuUsageHistory = ref<number[]>([])
const cpuLabels = ref<string[]>([])

// CPU核心柱状图相关
const cpuCoreChartRef = ref<HTMLElement | null>(null)
let cpuCoreChart: echarts.ECharts | null = null

// 内存图表相关
const memoryChartRef = ref<HTMLElement | null>(null)
let memoryChart: echarts.ECharts | null = null
const memoryUsageHistory = ref<number[]>([])
const memoryLabels = ref<string[]>([])

// CPU速度
const cpuSpeed = ref(3.60)

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
    
    // 更新CPU使用率历史数据
    const now = new Date()
    const timeLabel = `${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    
    // 添加新数据
    cpuUsageHistory.value.push(data.total_usage)
    cpuLabels.value.push(timeLabel)
    
    // 保持历史数据长度为20
    if (cpuUsageHistory.value.length > 20) {
      cpuUsageHistory.value.shift()
      cpuLabels.value.shift()
    }
    
    // 更新波形图
    updateCpuChart()
    
    // 更新CPU核心柱状图
    updateCpuCoreChart()
  } catch (error) {
    console.error('加载CPU使用率失败:', error)
  }
}

// 加载内存使用率
const loadMemoryUsage = async () => {
  try {
    const data = await systemApi.getMemoryUsage()
    memoryUsage.value = data
    
    // 更新内存使用率历史数据
    const now = new Date()
    const timeLabel = `${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    
    // 添加新数据
    memoryUsageHistory.value.push(data.memory.percent)
    memoryLabels.value.push(timeLabel)
    
    // 保持历史数据长度为20
    if (memoryUsageHistory.value.length > 20) {
      memoryUsageHistory.value.shift()
      memoryLabels.value.shift()
    }
    
    // 更新内存图表
    updateMemoryChart()
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
  loadDiskSmartInfo()
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

// 初始化CPU波形图
const initCpuChart = () => {
  if (cpuChartRef.value) {
    cpuChart = echarts.init(cpuChartRef.value)
    
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}%'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: cpuLabels.value,
        axisLabel: {
          interval: 5,
          fontSize: 12,
          color: '#606266'
        },
        axisLine: {
          lineStyle: {
            color: '#e0e0e0'
          }
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f0f0f0',
            type: 'dashed'
          }
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        axisLabel: {
          formatter: '{value}%',
          fontSize: 12,
          color: '#606266'
        },
        axisLine: {
          lineStyle: {
            color: '#e0e0e0'
          }
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f0f0f0',
            type: 'dashed'
          }
        }
      },
      series: [
        {
          name: 'CPU使用率',
          type: 'line',
          smooth: true,
          symbol: 'none',
          sampling: 'lttb',
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgba(64, 158, 255, 0.6)'
              },
              {
                offset: 1,
                color: 'rgba(64, 158, 255, 0.1)'
              }
            ])
          },
          lineStyle: {
            width: 2
          },
          data: cpuUsageHistory.value
        }
      ]
    }
    
    cpuChart.setOption(option)
  }
}

// 更新CPU波形图
const updateCpuChart = () => {
  if (cpuChart) {
    cpuChart.setOption({
      xAxis: {
        data: cpuLabels.value
      },
      series: [
        {
          data: cpuUsageHistory.value
        }
      ]
    })
  }
}

// 初始化CPU核心柱状图
const initCpuCoreChart = () => {
  if (cpuCoreChartRef.value) {
    cpuCoreChart = echarts.init(cpuCoreChartRef.value)
    updateCpuCoreChart()
  }
}

// 更新CPU核心柱状图
const updateCpuCoreChart = () => {
  if (cpuCoreChart) {
    const coreData = cpuUsage.value.per_core_usage
    const coreLabels = coreData.map((_, index) => `核心 ${index + 1}`)
    
    const option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: '{b}: {c}%'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: coreLabels,
        axisLabel: {
          interval: 0,
          rotate: 0
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        axisLabel: {
          formatter: '{value}%'
        }
      },
      series: [
        {
          name: 'CPU核心使用率',
          type: 'bar',
          data: coreData,
          itemStyle: {
            color: function(params) {
              const value = params.value
              if (value > 80) return '#F56C6C'
              if (value > 50) return '#E6A23C'
              return '#67C23A'
            }
          },
          barWidth: '60%'
        }
      ]
    }
    
    cpuCoreChart.setOption(option)
  }
}

// 初始化内存图表
const initMemoryChart = () => {
  if (memoryChartRef.value) {
    memoryChart = echarts.init(memoryChartRef.value)
    
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}%'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: memoryLabels.value,
        axisLabel: {
          interval: 5,
          fontSize: 12,
          color: '#606266'
        },
        axisLine: {
          lineStyle: {
            color: '#e0e0e0'
          }
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f0f0f0',
            type: 'dashed'
          }
        }
      },
      yAxis: {
        type: 'value',
        min: 0,
        max: 100,
        axisLabel: {
          formatter: '{value}%',
          fontSize: 12,
          color: '#606266'
        },
        axisLine: {
          lineStyle: {
            color: '#e0e0e0'
          }
        },
        axisTick: {
          show: false
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: '#f0f0f0',
            type: 'dashed'
          }
        }
      },
      series: [
        {
          name: '内存使用率',
          type: 'line',
          smooth: true,
          symbol: 'none',
          sampling: 'lttb',
          itemStyle: {
            color: '#67C23A'
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: 'rgba(103, 194, 58, 0.6)'
              },
              {
                offset: 1,
                color: 'rgba(103, 194, 58, 0.1)'
              }
            ])
          },
          lineStyle: {
            width: 2
          },
          data: memoryUsageHistory.value
        }
      ]
    }
    
    memoryChart.setOption(option)
  }
}

// 更新内存图表
const updateMemoryChart = () => {
  if (memoryChart) {
    memoryChart.setOption({
      xAxis: {
        data: memoryLabels.value
      },
      series: [
        {
          data: memoryUsageHistory.value
        }
      ]
    })
  }
}

// 组件挂载时加载数据
onMounted(async () => {
  // 先加载初始数据
  await loadAllData()
  
  // 初始化图表
  nextTick(() => {
    initCpuChart()
    initCpuCoreChart()
    initMemoryChart()
  })
  
  // 每5秒更新一次数据
  updateTimer = window.setInterval(loadAllData, 5000)
  
  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    if (cpuChart) {
      cpuChart.resize()
    }
    if (cpuCoreChart) {
      cpuCoreChart.resize()
    }
    if (memoryChart) {
      memoryChart.resize()
    }
  })
})

// 组件卸载时清除定时器和销毁图表
onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
  if (cpuChart) {
    cpuChart.dispose()
    cpuChart = null
  }
  if (cpuCoreChart) {
    cpuCoreChart.dispose()
    cpuCoreChart = null
  }
  if (memoryChart) {
    memoryChart.dispose()
    memoryChart = null
  }
  window.removeEventListener('resize', () => {
    if (cpuChart) {
      cpuChart.resize()
    }
    if (cpuCoreChart) {
      cpuCoreChart.resize()
    }
    if (memoryChart) {
      memoryChart.resize()
    }
  })
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

/* 主要内容容器 */
.main-content-container {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

/* 内容区域 */
.content-area {
  flex: 1;
  min-width: 0; /* 防止flex子元素溢出 */
}

.left-area {
  flex: 1;
}

.right-area {
  flex: 1;
}

/* 系统信息卡片 */
.system-info-card {
  margin-bottom: 16px;
  border-radius: 10px !important;
  overflow: hidden;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

.system-info-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 12px;
  height: 40px;
}

.card-header span {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

/* 系统信息网格 */
.system-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  padding: 12px 0;
}

/* 信息项 */
.info-item {
  display: flex;
  flex-direction: column;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.info-item:hover {
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  border-color: #409EFF;
}

/* 标签和值 */
.label {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
  font-weight: 400;
}

.value {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  line-height: 1.3;
}

/* 指标卡片 */
.metric-card {
  min-height: 180px;
  border-radius: 10px !important;
  overflow: hidden;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
  margin-bottom: 16px;
}

.metric-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

/* CPU信息 */
.cpu-info {
  padding: 12px 0;
}

.cpu-total {
  margin-bottom: 12px;
}

.cpu-cores {
  margin-top: 12px;
}

.core-item {
  margin-bottom: 8px;
}

.core-label {
  font-size: 12px;
  color: #606266;
  margin-bottom: 4px;
  display: block;
  font-weight: 500;
}

/* 内存信息 */
.memory-info {
  padding: 12px 0;
}

.memory-total {
  margin-bottom: 12px;
}

.memory-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.memory-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.memory-item .value {
  font-size: 14px;
  font-weight: 500;
  color: #409EFF;
}

/* 网络信息 */
.network-info {
  padding: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.network-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.network-item:hover {
  background-color: white;
  border-color: #409EFF;
}

.network-item .value {
  font-size: 14px;
  font-weight: 500;
  color: #67C23A;
}

/* 磁盘信息 */
.disk-info {
  padding: 12px 0;
}

.disk-item {
  margin-bottom: 12px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.disk-item:hover {
  background-color: white;
  border-color: #409EFF;
}

.disk-label {
  font-size: 12px;
  color: #606266;
  margin-bottom: 8px;
  font-weight: 500;
}

.disk-details {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
  text-align: right;
}

/* Docker卡片 */
.docker-card {
  margin-top: 16px;
  border-radius: 10px !important;
  overflow: hidden;
  box-shadow: 0 2px 8px 0 rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none !important;
}

.docker-card:hover {
  box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.docker-info {
  padding: 12px 0;
}

/* Docker容器状态 */
.docker-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
}

.container-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 16px;
  background-color: white;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.container-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
  transform: translateY(-1px);
}

.container-header {
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.container-name {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.container-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric .label {
  font-size: 12px;
  color: #606266;
  margin-bottom: 0;
}

.metric .value {
  font-size: 13px;
  font-weight: 500;
  color: #409EFF;
}

/* 无数据状态 */
.no-data {
  text-align: center;
  padding: 24px 16px;
  color: #909399;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 2px dashed #e9ecef;
  margin: 16px 0;
}

.no-data::before {
  content: '';
  display: block;
  width: 48px;
  height: 48px;
  margin: 0 auto 12px;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23c0c4cc"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14h-2v-4H8v-2h2V9h2v2h2v2h-2v4z"/></svg>') no-repeat center;
  background-size: contain;
}

/* 进度条样式 */
:deep(.el-progress__text) {
  font-size: 12px !important;
  font-weight: 500 !important;
  color: #303133 !important;
}

:deep(.el-progress-bar__outer) {
  border-radius: 8px !important;
  overflow: hidden !important;
  background-color: #f0f2f5 !important;
}

:deep(.el-progress-bar__inner) {
  border-radius: 8px !important;
  transition: width 1s ease-in-out !important;
}

/* CPU头部信息 */
.cpu-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cpu-usage {
  font-size: 14px;
  font-weight: 600;
  color: #409EFF;
}

.cpu-speed {
  font-size: 12px;
  color: #606266;
}

/* CPU详细信息 */
.cpu-details {
  margin: 12px 0;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.cpu-details-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.cpu-details-row:last-child {
  margin-bottom: 0;
}

.cpu-detail-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.detail-label {
  font-size: 11px;
  color: #909399;
}

.detail-value {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
}

/* 内存头部信息 */
.memory-header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.memory-usage {
  font-size: 14px;
  font-weight: 600;
  color: #67C23A;
}

.memory-total {
  font-size: 12px;
  color: #606266;
}

/* 内存图表 */
.memory-chart-container {
  margin: 12px 0;
}

.memory-chart {
  width: 100%;
  height: 160px;
}

/* 内存详细信息 */
.memory-details {
  margin: 12px 0;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.memory-details-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.memory-details-row:last-child {
  margin-bottom: 0;
}

.memory-detail-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* CPU图表 */
.cpu-chart-container {
  margin: 12px 0;
}

.cpu-chart {
  width: 100%;
  height: 160px;
}

.cpu-cores {
  margin-top: 12px;
}

.cpu-core-chart {
  width: 100%;
  height: 240px;
}

/* 磁盘S.M.A.R.T信息 */
.smart-info {
  padding: 12px;
}

.disk-smart-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.smart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.smart-item:last-child {
  border-bottom: none;
}

.smart-item .label {
  margin-bottom: 0;
  font-weight: 500;
}

.smart-item .value {
  font-size: 14px;
  font-weight: 600;
}

.smart-attributes {
  margin-top: 16px;
}

.smart-attributes h4 {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.status-ok {
  color: #67C23A;
  font-weight: 600;
}

.status-warning {
  color: #E6A23C;
  font-weight: 600;
}

.status-error {
  color: #F56C6C;
  font-weight: 600;
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
  
  /* 响应式布局：在小屏幕上改为垂直排列 */
  .main-content-container {
    flex-direction: column;
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
