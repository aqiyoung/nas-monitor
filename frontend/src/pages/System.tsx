import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

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
      // 初始加载时显示loading，后续刷新只更新数据，不显示loading
      const showLoading = !cpuUsage && !memoryUsage && diskUsage.length === 0
      if (showLoading) {
        setLoading(true)
      }
      
      const [cpuRes, memoryRes, diskRes] = await Promise.all([
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/system/disk')
      ])
      
      setCpuUsage(cpuRes.data)
      setMemoryUsage(memoryRes.data)
      setDiskUsage(diskRes.data)
      setError(null)
    } catch (err) {
      setError('获取系统数据失败')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="loading">加载中...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  const cpuChartData = cpuUsage?.per_core_usage.map((usage, index) => ({
    name: `核心 ${index + 1}`,
    使用率: usage
  })) || []

  const diskChartData = diskUsage.map(disk => ({
    name: disk.mountpoint,
    使用率: disk.percent
  }))

  return (
    <div>
      <div className="grid">
        <div className="card">
          <h2>CPU 详细信息</h2>
          {cpuUsage && (
            <>
              <div className="metric">
                <span className="metric-label">总使用率</span>
                <span className="metric-value">{cpuUsage.total_usage}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">物理核心</span>
                <span className="metric-value">{cpuUsage.cpu_count.physical}</span>
              </div>
              <div className="metric">
                <span className="metric-label">逻辑核心</span>
                <span className="metric-value">{cpuUsage.cpu_count.logical}</span>
              </div>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={cpuChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="使用率" fill="#3498db" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </>
          )}
        </div>

        <div className="card">
          <h2>内存详细信息</h2>
          {memoryUsage && (
            <>
              <div className="metric">
                <span className="metric-label">内存总量</span>
                <span className="metric-value">{(memoryUsage.memory.total / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
              </div>
              <div className="metric">
                <span className="metric-label">已用内存</span>
                <span className="metric-value">{(memoryUsage.memory.used / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
              </div>
              <div className="metric">
                <span className="metric-label">可用内存</span>
                <span className="metric-value">{(memoryUsage.memory.available / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
              </div>
              <div className="metric">
                <span className="metric-label">内存使用率</span>
                <span className="metric-value">{memoryUsage.memory.percent}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Swap 总量</span>
                <span className="metric-value">{(memoryUsage.swap.total / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
              </div>
              <div className="metric">
                <span className="metric-label">Swap 使用率</span>
                <span className="metric-value">{memoryUsage.swap.percent}%</span>
              </div>
            </>
          )}
        </div>
      </div>

      <div className="card">
        <h2>磁盘使用情况</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={diskChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="使用率" fill="#2ecc71" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div style={{ marginTop: '20px' }}>
          {diskUsage.map((disk, index) => (
            <div key={index} className="metric">
              <div>
                <div className="metric-label">{disk.mountpoint}</div>
                <div style={{ fontSize: '0.8rem', color: '#999' }}>{disk.device} ({disk.fstype})</div>
              </div>
              <div>
                <div className="metric-value">{disk.percent}%</div>
                <div style={{ fontSize: '0.8rem', color: '#999' }}>
                  {(disk.used / (1024 * 1024 * 1024)).toFixed(2)} GB / {(disk.total / (1024 * 1024 * 1024)).toFixed(2)} GB
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default System