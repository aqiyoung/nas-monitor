import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import SystemStatusCard from '../components/SystemStatusCard'
import CPUUsageCard from '../components/CPUUsageCard'
import MemoryUsageCard from '../components/MemoryUsageCard'
import NetworkTrafficCard from '../components/NetworkTrafficCard'

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

const Dashboard: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [networkTraffic, setNetworkTraffic] = useState<NetworkTraffic | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      // 只有在初始加载且没有任何数据时才显示loading
      const isInitialLoad = !systemStatus && !cpuUsage && !memoryUsage && !networkTraffic
      if (isInitialLoad) {
        setLoading(true)
      }
      const [systemRes, cpuRes, memoryRes, networkRes] = await Promise.all([
        api.get('/api/system/status'),
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/network/traffic')
      ])
      
      // 使用函数式更新，避免直接依赖外部状态
      setSystemStatus(prev => systemRes.data)
      setCpuUsage(prev => cpuRes.data)
      setMemoryUsage(prev => memoryRes.data)
      setNetworkTraffic(prev => networkRes.data)
      setError(null)
    } catch (err) {
      setError('获取数据失败，请检查后端服务是否正常运行')
      console.error(err)
    } finally {
      // 无论如何，初始加载完成后都要关闭loading
      // 不依赖闭包中的loading值，确保后续刷新不会显示loading
      setLoading(false)
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
        <SystemStatusCard systemStatus={systemStatus} />
        <CPUUsageCard cpuUsage={cpuUsage} />
        <MemoryUsageCard memoryUsage={memoryUsage} />
        <NetworkTrafficCard networkTraffic={networkTraffic} />
      </div>
    </div>
  )
}

// 使用React.memo包装Dashboard组件，避免不必要的重新渲染
export default React.memo(Dashboard)
