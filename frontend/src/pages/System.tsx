import React, { useEffect, useState } from 'react'
import api from '../utils/api'

interface CPUUsage {
  total_usage: number
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

interface DiskUsage {
  device: string
  mountpoint: string
  fstype: string
  total: number
  used: number
  free: number
  percent: number
}

const System: React.FC = () => {
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [diskUsage, setDiskUsage] = useState<DiskUsage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      // 只有在首次加载且没有任何数据时才显示loading
      if (!cpuUsage && !memoryUsage && diskUsage.length === 0) {
        setLoading(true)
      }
      const [cpuRes, memoryRes, diskRes] = await Promise.all([
        api.get('/system/cpu'),
        api.get('/system/memory'),
        api.get('/system/disk')
      ])
      setCpuUsage(cpuRes.data)
      setMemoryUsage(memoryRes.data)
      setDiskUsage(diskRes.data)
      setError(null)
    } catch (err) {
      setError('获取系统数据失败')
      console.error(err)
    } finally {
      // 始终在请求完成后设置loading为false
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <div className="card">
          <h2>CPU 详细信息</h2>
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
          <h2>内存详细信息</h2>
          <div className="metric">
            <span className="metric-label">内存总量</span>
            <span className="metric-value">{((memoryUsage?.memory.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">已用内存</span>
            <span className="metric-value">{((memoryUsage?.memory.used || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">可用内存</span>
            <span className="metric-value">{((memoryUsage?.memory.available || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default System