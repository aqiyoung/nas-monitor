<template>
  <div class="alarm-page">
    <h2>告警管理</h2>
    
    <!-- 告警列表 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>告警列表</span>
        </div>
      </template>
      <div class="alarms-info">
        <el-table :data="alarms" style="width: 100%">
          <el-table-column prop="id" label="告警ID" width="100" />
          <el-table-column prop="level" label="告警级别">
            <template #default="scope">
              <el-tag :type="getAlarmLevelType(scope.row.level)">
                {{ scope.row.level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="type" label="告警类型" />
          <el-table-column prop="message" label="告警消息" />
          <el-table-column prop="time" label="告警时间" />
          <el-table-column prop="status" label="告警状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === 'resolved' ? 'success' : 'danger'">
                {{ scope.row.status === 'resolved' ? '已解决' : '未解决' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 告警配置 -->
    <el-card class="metric-card">
      <template #header>
        <div class="card-header">
          <span>告警配置</span>
        </div>
      </template>
      <div class="alarm-config">
        <el-form :model="alarmConfig" ref="alarmConfigRef" label-width="120px">
          <el-form-item label="CPU阈值">
            <el-input-number v-model="alarmConfig.cpu_threshold" :min="1" :max="100" :step="1" placeholder="CPU使用率阈值（%）" />
          </el-form-item>
          
          <el-form-item label="内存阈值">
            <el-input-number v-model="alarmConfig.memory_threshold" :min="1" :max="100" :step="1" placeholder="内存使用率阈值（%）" />
          </el-form-item>
          
          <el-form-item label="磁盘阈值">
            <el-input-number v-model="alarmConfig.disk_threshold" :min="1" :max="100" :step="1" placeholder="磁盘使用率阈值（%）" />
          </el-form-item>
          
          <el-form-item label="告警检查间隔">
            <el-input-number v-model="alarmConfig.check_interval" :min="10" :max="3600" :step="10" placeholder="告警检查间隔（秒）" />
          </el-form-item>
          
          <el-form-item label="邮件告警">
            <el-switch v-model="alarmConfig.email_alarm" />
          </el-form-item>
          
          <el-form-item label="邮件地址" v-if="alarmConfig.email_alarm">
            <el-input v-model="alarmConfig.email_address" placeholder="告警邮件接收地址" />
          </el-form-item>
          
          <el-form-item label="钉钉告警">
            <el-switch v-model="alarmConfig.dingtalk_alarm" />
          </el-form-item>
          
          <el-form-item label="钉钉Webhook" v-if="alarmConfig.dingtalk_alarm">
            <el-input v-model="alarmConfig.dingtalk_webhook" placeholder="钉钉机器人Webhook地址" />
          </el-form-item>
          
          <el-form-item label="企业微信告警">
            <el-switch v-model="alarmConfig.wework_alarm" />
          </el-form-item>
          
          <el-form-item label="企业微信配置" v-if="alarmConfig.wework_alarm">
            <el-input v-model="alarmConfig.wework_corp_id" placeholder="企业微信CorpID" style="margin-bottom: 10px" />
            <el-input v-model="alarmConfig.wework_agent_id" placeholder="企业微信AgentID" style="margin-bottom: 10px" />
            <el-input v-model="alarmConfig.wework_app_secret" placeholder="企业微信AppSecret" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="handleUpdateConfig" :loading="configLoading">
              更新配置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { alarmApi } from '../services/api'

// 告警列表
const alarms = ref([])

// 告警配置
const alarmConfigRef = ref()
const configLoading = ref(false)
const alarmConfig = ref({
  cpu_threshold: 80,
  memory_threshold: 80,
  disk_threshold: 80,
  check_interval: 60,
  email_alarm: false,
  email_address: '',
  dingtalk_alarm: false,
  dingtalk_webhook: '',
  wework_alarm: false,
  wework_corp_id: '',
  wework_agent_id: '',
  wework_app_secret: ''
})

// 定时器
let updateTimer: number | undefined

// 加载告警列表
const loadAlarms = async () => {
  try {
    const data = await alarmApi.getAlarms()
    alarms.value = data
  } catch (error) {
    console.error('加载告警列表失败:', error)
  }
}

// 加载告警配置
const loadAlarmConfig = async () => {
  try {
    const data = await alarmApi.getConfig()
    if (data) {
      alarmConfig.value = { ...alarmConfig.value, ...data }
    }
  } catch (error) {
    console.error('加载告警配置失败:', error)
  }
}

// 加载所有数据
const loadAllData = () => {
  loadAlarms()
  loadAlarmConfig()
}

// 更新告警配置
const handleUpdateConfig = async () => {
  configLoading.value = true
  
  try {
    const response = await alarmApi.updateConfig(alarmConfig.value)
    if (response.success) {
      // 配置更新成功
      console.log('告警配置更新成功')
    }
  } catch (error) {
    console.error('更新告警配置失败:', error)
  } finally {
    configLoading.value = false
  }
}

// 获取告警级别类型
const getAlarmLevelType = (level: string): string => {
  switch (level) {
    case 'critical':
      return 'danger'
    case 'warning':
      return 'warning'
    case 'info':
      return 'info'
    default:
      return 'success'
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadAllData()
  // 每30秒更新一次数据
  updateTimer = window.setInterval(loadAllData, 30000)
})

// 组件卸载时清除定时器
onUnmounted(() => {
  if (updateTimer) {
    clearInterval(updateTimer)
  }
})
</script>

<style scoped>
.alarm-page {
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

.alarms-info {
  padding: 10px 0;
}

.alarm-config {
  padding: 10px 0;
}
</style>
