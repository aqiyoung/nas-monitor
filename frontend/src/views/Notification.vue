<template>
  <div class="notification-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>通知管理</span>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="通知渠道" name="channels">
          <div class="channel-management">
            <el-button type="primary" @click="showAddChannelDialog">添加通知渠道</el-button>
            <el-table :data="channels" style="width: 100%" class="mt-4">
              <el-table-column prop="name" label="名称" width="180"></el-table-column>
              <el-table-column prop="type" label="类型" width="120">
                <template #default="scope">
                  <el-tag :type="scope.row.type === 'telegram' ? 'info' : 'success'">
                    {{ scope.row.type === 'telegram' ? 'Telegram' : '飞书' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="enabled" label="状态" width="100">
                <template #default="scope">
                  <el-switch v-model="scope.row.enabled" @change="updateChannelStatus(scope.row)"></el-switch>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template #default="scope">
                  <el-button size="small" type="primary" @click="showEditChannelDialog(scope.row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteChannel(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="通知偏好" name="preferences">
          <div class="preference-management">
            <el-form :model="preference" label-width="120px">
              <el-form-item label="启用的渠道">
                <el-select
                  v-model="preference.channels"
                  multiple
                  placeholder="选择通知渠道"
                  style="width: 100%"
                >
                  <el-option
                    v-for="channel in channels"
                    :key="channel.id"
                    :label="channel.name"
                    :value="channel.id"
                  ></el-option>
                </el-select>
              </el-form-item>
              
              <el-form-item label="消息类型偏好">
                <el-table :data="messageTypePreferences" style="width: 100%">
                  <el-table-column prop="type" label="消息类型" width="180"></el-table-column>
                  <el-table-column label="通知渠道">
                    <template #default="scope">
                      <el-select
                        v-model="scope.row.channels"
                        multiple
                        placeholder="选择通知渠道"
                        style="width: 100%"
                      >
                        <el-option
                          v-for="channel in channels"
                          :key="channel.id"
                          :label="channel.name"
                          :value="channel.id"
                        ></el-option>
                      </el-select>
                    </template>
                  </el-table-column>
                </el-table>
              </el-form-item>
              
              <el-form-item label="严重程度偏好">
                <el-table :data="severityPreferences" style="width: 100%">
                  <el-table-column prop="level" label="严重程度" width="180"></el-table-column>
                  <el-table-column label="通知渠道">
                    <template #default="scope">
                      <el-select
                        v-model="scope.row.channels"
                        multiple
                        placeholder="选择通知渠道"
                        style="width: 100%"
                      >
                        <el-option
                          v-for="channel in channels"
                          :key="channel.id"
                          :label="channel.name"
                          :value="channel.id"
                        ></el-option>
                      </el-select>
                    </template>
                  </el-table-column>
                </el-table>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="savePreferences">保存偏好设置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- 添加/编辑通知渠道对话框 -->
    <el-dialog
      :title="isEditing ? '编辑通知渠道' : '添加通知渠道'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="渠道名称">
          <el-input v-model="form.name" placeholder="请输入渠道名称"></el-input>
        </el-form-item>
        
        <el-form-item label="渠道类型">
          <el-radio-group v-model="form.type">
            <el-radio label="telegram">Telegram</el-radio>
            <el-radio label="feishu">飞书</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="是否启用">
          <el-switch v-model="form.enabled"></el-switch>
        </el-form-item>
        
        <el-form-item label="配置信息" v-if="form.type === 'telegram'">
          <el-input v-model="form.config.token" placeholder="Telegram Bot Token" class="mb-2"></el-input>
          <el-input v-model="form.config.chat_id" placeholder="Chat ID" class="mb-2"></el-input>
        </el-form-item>
        
        <el-form-item label="配置信息" v-else-if="form.type === 'feishu'">
          <el-input v-model="form.config.webhook_url" placeholder="飞书机器人Webhook URL" class="mb-2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveChannel">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, reactive, computed } from 'vue'
import { notificationApi } from '../services/api'

export default defineComponent({
  name: 'Notification',
  setup() {
    const activeTab = ref('channels')
    const channels = ref<any[]>([])
    const preference = reactive({
      user_id: 'default',
      channels: [],
      message_types: {
        'system': [],
        'network': [],
        'docker': []
      },
      severity_levels: {
        'info': [],
        'warning': [],
        'critical': []
      }
    })
    
    const dialogVisible = ref(false)
    const isEditing = ref(false)
    const form = reactive({
      id: '',
      name: '',
      type: 'telegram',
      enabled: true,
      config: {
        token: '',
        chat_id: '',
        webhook_url: ''
      }
    })
    
    const messageTypePreferences = computed(() => {
      return [
        { type: 'system', channels: preference.message_types.system || [] },
        { type: 'network', channels: preference.message_types.network || [] },
        { type: 'docker', channels: preference.message_types.docker || [] }
      ]
    })
    
    const severityPreferences = computed(() => {
      return [
        { level: 'info', channels: preference.severity_levels.info || [] },
        { level: 'warning', channels: preference.severity_levels.warning || [] },
        { level: 'critical', channels: preference.severity_levels.critical || [] }
      ]
    })
    
    // 加载通知渠道
    const loadChannels = async () => {
      try {
        const response = await notificationApi.getChannels()
        channels.value = response
      } catch (error) {
        console.error('加载通知渠道失败:', error)
      }
    }
    
    // 加载通知偏好设置
    const loadPreferences = async () => {
      try {
        const response = await notificationApi.getPreference('default')
        if (response) {
          Object.assign(preference, response)
        }
      } catch (error) {
        console.error('加载通知偏好设置失败:', error)
      }
    }
    
    // 显示添加渠道对话框
    const showAddChannelDialog = () => {
      isEditing.value = false
      form.id = ''
      form.name = ''
      form.type = 'telegram'
      form.enabled = true
      form.config = {
        token: '',
        chat_id: '',
        webhook_url: ''
      }
      dialogVisible.value = true
    }
    
    // 显示编辑渠道对话框
    const showEditChannelDialog = (channel: any) => {
      isEditing.value = true
      form.id = channel.id
      form.name = channel.name
      form.type = channel.type
      form.enabled = channel.enabled
      form.config = { ...channel.config }
      dialogVisible.value = true
    }
    
    // 保存渠道
    const saveChannel = async () => {
      try {
        if (isEditing.value) {
          await notificationApi.updateChannel(form.id, form)
        } else {
          await notificationApi.createChannel(form)
        }
        dialogVisible.value = false
        loadChannels()
      } catch (error) {
        console.error('保存通知渠道失败:', error)
      }
    }
    
    // 更新渠道状态
    const updateChannelStatus = async (channel: any) => {
      try {
        await notificationApi.updateChannel(channel.id, { enabled: channel.enabled })
      } catch (error) {
        console.error('更新渠道状态失败:', error)
        channel.enabled = !channel.enabled // 恢复原来的状态
      }
    }
    
    // 删除渠道
    const deleteChannel = async (channelId: string) => {
      try {
        await notificationApi.deleteChannel(channelId)
        loadChannels()
      } catch (error) {
        console.error('删除渠道失败:', error)
      }
    }
    
    // 保存偏好设置
    const savePreferences = async () => {
      try {
        // 更新message_types和severity_levels
        preference.message_types = {
          'system': messageTypePreferences.value[0].channels,
          'network': messageTypePreferences.value[1].channels,
          'docker': messageTypePreferences.value[2].channels
        }
        
        preference.severity_levels = {
          'info': severityPreferences.value[0].channels,
          'warning': severityPreferences.value[1].channels,
          'critical': severityPreferences.value[2].channels
        }
        
        await notificationApi.updatePreference('default', preference)
        alert('偏好设置已保存')
      } catch (error) {
        console.error('保存偏好设置失败:', error)
      }
    }
    
    // 组件挂载时加载数据
    onMounted(() => {
      loadChannels()
      loadPreferences()
    })
    
    return {
      activeTab,
      channels,
      preference,
      dialogVisible,
      isEditing,
      form,
      messageTypePreferences,
      severityPreferences,
      showAddChannelDialog,
      showEditChannelDialog,
      saveChannel,
      updateChannelStatus,
      deleteChannel,
      savePreferences
    }
  }
})
</script>

<style scoped>
.notification-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.channel-management {
  margin-top: 20px;
}

.preference-management {
  margin-top: 20px;
}

.mt-4 {
  margin-top: 16px;
}

.mb-2 {
  margin-bottom: 8px;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}
</style>
