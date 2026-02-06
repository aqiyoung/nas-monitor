<template>
  <div class="monitoring-container">
    <el-page-header
      @back="goBack"
      content="监控中心"
      class="page-header"
    />

    <el-card class="monitoring-card">
      <template #header>
        <div class="card-header">
          <span>监控容器状态</span>
        </div>
      </template>

      <div class="monitoring-tabs">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane label="Prometheus" name="prometheus">
            <div class="prometheus-content">
              <el-button type="primary" @click="fetchPrometheusMetrics" :loading="loading.prometheus">
                刷新数据
              </el-button>
              
              <el-divider />
              
              <div v-if="prometheusData.success" class="metrics-container">
                <el-table :data="formatPrometheusData(prometheusData.data)" style="width: 100%">
                  <el-table-column prop="metric" label="指标" width="180" />
                  <el-table-column prop="value" label="值" />
                  <el-table-column prop="labels" label="标签" />
                </el-table>
              </div>
              <div v-else class="error-message">
                <el-alert
                  :title="prometheusData.error"
                  type="error"
                  show-icon
                  :closable="false"
                />
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="InfluxDB" name="influxdb">
            <div class="influxdb-content">
              <el-button type="primary" @click="fetchInfluxDBData" :loading="loading.influxdb">
                刷新数据
              </el-button>
              
              <el-divider />
              
              <div v-if="influxdbData.success" class="buckets-container">
                <el-table :data="formatInfluxDBData(influxdbData.data)" style="width: 100%">
                  <el-table-column prop="name" label="桶名称" width="180" />
                  <el-table-column prop="id" label="ID" />
                  <el-table-column prop="retention" label="保留期" />
                </el-table>
              </div>
              <div v-else class="error-message">
                <el-alert
                  :title="influxdbData.error"
                  type="error"
                  show-icon
                  :closable="false"
                />
              </div>
            </div>
          </el-tab-pane>

          <el-tab-pane label="监控状态" name="status">
            <div class="status-content">
              <el-descriptions :column="2" border>
                <el-descriptions-item label="Prometheus状态">
                  <el-tag :type="prometheusStatus.type">{{ prometheusStatus.text }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="InfluxDB状态">
                  <el-tag :type="influxdbStatus.type">{{ influxdbStatus.text }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="Node Exporter状态">
                  <el-tag :type="nodeExporterStatus.type">{{ nodeExporterStatus.text }}</el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="cAdvisor状态">
                  <el-tag :type="cadvisorStatus.type">{{ cadvisorStatus.text }}</el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { prometheusApi, influxdbApi } from '../services/api'

const router = useRouter()
const activeTab = ref('prometheus')
const loading = ref({
  prometheus: false,
  influxdb: false
})

const prometheusData = ref({
  success: false,
  data: null,
  error: ''
})

const influxdbData = ref({
  success: false,
  data: null,
  error: ''
})

const prometheusStatus = ref({
  type: 'info',
  text: '检查中'
})

const influxdbStatus = ref({
  type: 'info',
  text: '检查中'
})

const nodeExporterStatus = ref({
  type: 'info',
  text: '检查中'
})

const cadvisorStatus = ref({
  type: 'info',
  text: '检查中'
})

const goBack = () => {
  router.back()
}

const fetchPrometheusMetrics = async () => {
  loading.value.prometheus = true
  try {
    const data = await prometheusApi.getMetrics()
    prometheusData.value = data
    
    // 更新状态
    if (data.success) {
      prometheusStatus.value = {
        type: 'success',
        text: '正常'
      }
    } else {
      prometheusStatus.value = {
        type: 'danger',
        text: '异常'
      }
    }
  } catch (error) {
    prometheusData.value = {
      success: false,
      data: null,
      error: '获取Prometheus指标失败'
    }
    prometheusStatus.value = {
      type: 'danger',
      text: '异常'
    }
  } finally {
    loading.value.prometheus = false
  }
}

const fetchInfluxDBData = async () => {
  loading.value.influxdb = true
  try {
    const data = await influxdbApi.getData()
    influxdbData.value = data
    
    // 更新状态
    if (data.success) {
      influxdbStatus.value = {
        type: 'success',
        text: '正常'
      }
    } else {
      influxdbStatus.value = {
        type: 'danger',
        text: '异常'
      }
    }
  } catch (error) {
    influxdbData.value = {
      success: false,
      data: null,
      error: '获取InfluxDB数据失败'
    }
    influxdbStatus.value = {
      type: 'danger',
      text: '异常'
    }
  } finally {
    loading.value.influxdb = false
  }
}

const formatPrometheusData = (data: any) => {
  if (!data || !data.data || !data.data.result) {
    return []
  }
  
  return data.data.result.map((item: any) => {
    return {
      metric: item.metric?.__name__ || 'unknown',
      value: item.value?.[1] || 'N/A',
      labels: JSON.stringify(item.metric || {})
    }
  })
}

const formatInfluxDBData = (data: any) => {
  if (!data || !data.buckets) {
    return []
  }
  
  return data.buckets.map((bucket: any) => {
    return {
      name: bucket.name || 'unknown',
      id: bucket.id || 'N/A',
      retention: bucket.retentionRules?.[0]?.everySeconds || 'N/A'
    }
  })
}

// 检查监控容器状态
const checkServiceStatus = async () => {
  // 这里可以添加对其他监控容器的状态检查
  // 暂时使用默认状态
  nodeExporterStatus.value = {
    type: 'success',
    text: '正常'
  }
  
  cadvisorStatus.value = {
    type: 'success',
    text: '正常'
  }
}

onMounted(() => {
  fetchPrometheusMetrics()
  fetchInfluxDBData()
  checkServiceStatus()
})
</script>

<style scoped>
.monitoring-container {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
}

.monitoring-card {
  margin-bottom: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitoring-tabs {
  margin-top: 16px;
}

.prometheus-content,
.influxdb-content {
  padding: 16px;
}

.error-message {
  margin-top: 16px;
}

.metrics-container,
.buckets-container {
  margin-top: 16px;
}

.status-content {
  padding: 16px;
}

.el-table {
  margin-top: 16px;
}
</style>