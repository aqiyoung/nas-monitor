import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 认证相关API
export const authApi = {
  login: (data: { username: string; password: string }) => {
    return api.post('/auth/login', data)
  },
  refreshToken: (token: string) => {
    return api.post('/auth/refresh', { token })
  }
}

// 系统相关API
export const systemApi = {
  getStatus: () => {
    return api.get('/system/status')
  },
  getCpuUsage: () => {
    return api.get('/system/cpu')
  },
  getMemoryUsage: () => {
    return api.get('/system/memory')
  },
  getDiskUsage: () => {
    return api.get('/system/disk')
  },
  getDiskSmartInfo: () => {
    return api.get('/system/disk/smart')
  }
}

// 网络相关API
export const networkApi = {
  getTraffic: () => {
    return api.get('/network/traffic')
  },
  getInterfaces: () => {
    return api.get('/network/interfaces')
  },
  capturePackets: (data: { interface?: string; duration?: number; output_file?: string }) => {
    return api.post('/network/capture', data)
  },
  getLogs: (params: { log_file?: string; lines?: number }) => {
    return api.get('/network/logs', { params })
  }
}

// IO相关API
export const ioApi = {
  getIoStats: () => {
    return api.get('/io/stats')
  }
}

// Docker相关API
export const dockerApi = {
  getContainers: () => {
    return api.get('/docker/containers')
  },
  getStats: () => {
    return api.get('/docker/stats')
  },
  getImages: () => {
    return api.get('/docker/images')
  },
  pullImage: (image_name: string) => {
    return api.post('/docker/images/pull', { image_name })
  },
  deleteImage: (image_id: string) => {
    return api.delete(`/docker/images/${image_id}`)
  },
  startContainer: (container_id: string) => {
    return api.post(`/docker/containers/${container_id}/start`)
  },
  stopContainer: (container_id: string) => {
    return api.post(`/docker/containers/${container_id}/stop`)
  },
  restartContainer: (container_id: string) => {
    return api.post(`/docker/containers/${container_id}/restart`)
  },
  getContainerLogs: (container_id: string, tail?: number) => {
    return api.get(`/docker/containers/${container_id}/logs`, { params: { tail } })
  }
}

// 告警相关API
export const alarmApi = {
  getAlarms: () => {
    return api.get('/alarm/configs')
  },
  getConfig: (config_id: string) => {
    return api.get(`/alarm/configs/${config_id}`)
  },
  updateConfig: (config_id: string, data: any) => {
    return api.put(`/alarm/configs/${config_id}`, data)
  }
}

export default api
