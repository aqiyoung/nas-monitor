import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import SystemStatusCard from '../components/SystemStatusCard'
import CPUUsageCard from '../components/CPUUsageCard'
import MemoryUsageCard from '../components/MemoryUsageCard'
import NetworkTrafficCard from '../components/NetworkTrafficCard'
import { withRenderDebug } from '../utils/debug-render'

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
  // 使用更高效的深度比较，避免不必要的JSON.stringify
  const dataChanged = useMemo(() => {
    const deepCompare = (a: any, b: any): boolean => {
      if (a === b) return false
      
      if (typeof a !== typeof b) return true
      
      if (typeof a !== 'object' || a === null || b === null) return a !== b
      
      if (Array.isArray(a) && Array.isArray(b)) {
        if (a.length !== b.length) return true
        for (let i = 0; i < a.length; i++) {
          if (deepCompare(a[i], b[i])) return true
        }
        return false
      }
      
      const keysA = Object.keys(a)
      const keysB = Object.keys(b)
      if (keysA.length !== keysB.length) return true
      
      for (const key of keysA) {
        if (!keysB.includes(key)) return true
        if (deepCompare(a[key], b[key])) return true
      }
      
      return false
    }
    
    return deepCompare
  }, [])

  const fetchData = async () => {
    try {
      // 只有在初始加载且没有任何数据时才显示loading
      if (!systemStatus && !cpuUsage && !memoryUsage && !networkTraffic) {
        setLoading(true)
      }
      
      const [systemRes, cpuRes, memoryRes, networkRes] = await Promise.all([
        api.get('/system/status'),
        api.get('/system/cpu'),
        api.get('/system/memory'),
        api.get('/network/traffic')
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

  // 准备CPU图表数据
  const cpuChartData = cpuUsage?.per_core_usage ? cpuUsage.per_core_usage.map((usage, index) => ({
    name: `核心 ${index + 1}`,
    使用率: usage
  })) : []

  return (
    <div>
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <SystemStatusCard data={systemStatus} />
        <CPUUsageCard data={cpuUsage} cpuChartData={cpuChartData} />
        <MemoryUsageCard data={memoryUsage} />
        <NetworkTrafficCard data={networkTraffic} />
      </div>
    </div>
  )
})

export default Dashboard