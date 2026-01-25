import React, { useEffect, useState } from 'react'
import api from '../utils/api'

interface SystemStatus {
  hostname: string
  os: string
  os_version: string
  architecture: string
  boot_time: string
  uptime: string
}

interface CPUUsage {
  total_usage: number
  per_core_usage: number[]
  cpu_count: {
    physical: number
    logical: number
  }
}

interface MemoryUsage {
  memory: {
    total: number
    available: number
    used: number
    percent: number
  }
  swap: {
    total: number
    used: number
    free: number
    percent: number
  }
}

interface NetworkTraffic {
  bytes_sent: number
  bytes_recv: number
  packets_sent: number
  packets_recv: number
  errin: number
  errout: number
  dropin: number
  dropout: number
}

const Dashboard: React.FC = React.memo(() => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [networkTraffic, setNetworkTraffic] = useState<NetworkTraffic | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 数据比较函数，用于判断数据是否真正变化
  const dataChanged = (oldData: any, newData: any): boolean => {
    if (oldData === null || newData === null) {
      return oldData !== newData
    }
    
    // 对于对象，比较其JSON字符串
    return JSON.stringify(oldData) !== JSON.stringify(newData)
  }

  const fetchData = async () => {
    try {
      // 只有在初始加载且没有任何数据时才显示loading
      if (!systemStatus && !cpuUsage && !memoryUsage && !networkTraffic) {
        setLoading(true)
      }
      
      const [systemRes, cpuRes, memoryRes, networkRes] = await Promise.all([
        api.get('/api/system/status'),
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/network/traffic')
      ])
      
      // 只有当数据真正变化时才更新状态，避免不必要的重新渲染
      if (dataChanged(systemStatus, systemRes.data)) {
        setSystemStatus(systemRes.data)
      }
      if (dataChanged(cpuUsage, cpuRes.data)) {
        setCpuUsage(cpuRes.data)
      }
      if (dataChanged(memoryUsage, memoryRes.data)) {
        setMemoryUsage(memoryRes.data)
      }
      if (dataChanged(networkTraffic, networkRes.data)) {
        setNetworkTraffic(networkRes.data)
      }
      
      // 只有在有错误时才设置error，否则保持null
      if (error) {
        setError(null)
      }
    } catch (err) {
      setError('获取数据失败，请检查后端服务是否正常运行')
      console.error(err)
    } finally {
      // 只有在初始加载时才设置loading为false
      if (loading) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000) // 每5秒刷新一次数据
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      {loading && <div className="loading-overlay">加载中...</div>}
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <div className="card">
          <h2>系统状态</h2>
          <div className="metric">
            <span className="metric-label">主机名</span>
            <span className="metric-value">{systemStatus?.hostname || '-'}</span>
          </div>
          <div className="metric">
            <span className="metric-label">操作系统</span>
            <span className="metric-value">{systemStatus?.os || '-'} {systemStatus?.os_version || ''}</span>
          </div>
          <div className="metric">
            <span className="metric-label">架构</span>
            <span className="metric-value">{systemStatus?.architecture || '-'}</span>
          </div>
          <div className="metric">
            <span className="metric-label">启动时间</span>
            <span className="metric-value">{systemStatus?.boot_time || '-'}</span>
          </div>
          <div className="metric">
            <span className="metric-label">运行时间</span>
            <span className="metric-value">{systemStatus?.uptime || '-'}</span>
          </div>
        </div>

        <div className="card">
          <h2>CPU 使用情况</h2>
          <div className="metric">
            <span className="metric-label">总使用率</span>
            <span className="metric-value">{cpuUsage?.total_usage || 0}%</span>
          </div>
          <div className="metric">
            <span className="metric-label">物理核心</span>
            <span className="metric-value">{cpuUsage?.cpu_count.physical || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">逻辑核心</span>
            <span className="metric-value">{cpuUsage?.cpu_count.logical || 0}</span>
          </div>
        </div>

        <div className="card">
          <h2>内存使用情况</h2>
          <div className="metric">
            <span className="metric-label">内存使用率</span>
            <span className="metric-value">{memoryUsage?.memory.percent || 0}%</span>
          </div>
          <div className="metric">
            <span className="metric-label">已用内存</span>
            <span className="metric-value">{((memoryUsage?.memory.used || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">可用内存</span>
            <span className="metric-value">{((memoryUsage?.memory.available || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">内存总量</span>
            <span className="metric-value">{((memoryUsage?.memory.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">Swap 使用率</span>
            <span className="metric-value">{memoryUsage?.swap.percent || 0}%</span>
          </div>
        </div>

        <div className="card">
          <h2>网络流量</h2>
          <div className="metric">
            <span className="metric-label">发送字节数</span>
            <span className="metric-value">{((networkTraffic?.bytes_sent || 0) / (1024 * 1024)).toFixed(2)} MB</span>
          </div>
          <div className="metric">
            <span className="metric-label">接收字节数</span>
            <span className="metric-value">{((networkTraffic?.bytes_recv || 0) / (1024 * 1024)).toFixed(2)} MB</span>
          </div>
          <div className="metric">
            <span className="metric-label">发送数据包</span>
            <span className="metric-value">{networkTraffic?.packets_sent || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">接收数据包</span>
            <span className="metric-value">{networkTraffic?.packets_recv || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">错误输入</span>
            <span className="metric-value">{networkTraffic?.errin || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">错误输出</span>
            <span className="metric-value">{networkTraffic?.errout || 0}</span>
          </div>
        </div>
      </div>
    </div>
  )
})

export default Dashboard