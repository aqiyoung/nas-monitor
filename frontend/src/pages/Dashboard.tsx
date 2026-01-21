import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

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
      // 初始加载时显示loading，后续刷新只更新数据，不显示loading
      const showLoading = !systemStatus && !cpuUsage && !memoryUsage && !networkTraffic
      if (showLoading) {
        setLoading(true)
      }
      
      const [systemRes, cpuRes, memoryRes, networkRes] = await Promise.all([
        axios.get('/api/system/status'),
        axios.get('/api/system/cpu'),
        axios.get('/api/system/memory'),
        axios.get('/api/network/traffic')
      ])
      
      setSystemStatus(systemRes.data)
      setCpuUsage(cpuRes.data)
      setMemoryUsage(memoryRes.data)
      setNetworkTraffic(networkRes.data)
      setError(null)
    } catch (err) {
      setError('获取数据失败，请检查后端服务是否正常运行')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000) // 每5秒刷新一次数据
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

  return (
    <div>
      <div className="grid">
        <div className="card">
          <h2>系统状态</h2>
          {systemStatus && (
            <>
              <div className="metric">
                <span className="metric-label">主机名</span>
                <span className="metric-value">{systemStatus.hostname}</span>
              </div>
              <div className="metric">
                <span className="metric-label">操作系统</span>
                <span className="metric-value">{systemStatus.os} {systemStatus.os_version}</span>
              </div>
              <div className="metric">
                <span className="metric-label">架构</span>
                <span className="metric-value">{systemStatus.architecture}</span>
              </div>
              <div className="metric">
                <span className="metric-label">启动时间</span>
                <span className="metric-value">{systemStatus.boot_time}</span>
              </div>
              <div className="metric">
                <span className="metric-label">运行时间</span>
                <span className="metric-value">{systemStatus.uptime}</span>
              </div>
            </>
          )}
        </div>

        <div className="card">
          <h2>CPU 使用情况</h2>
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
          <h2>内存使用情况</h2>
          {memoryUsage && (
            <>
              <div className="metric">
                <span className="metric-label">内存使用率</span>
                <span className="metric-value">{memoryUsage.memory.percent}%</span>
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
                <span className="metric-label">内存总量</span>
                <span className="metric-value">{(memoryUsage.memory.total / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
              </div>
              <div className="metric">
                <span className="metric-label">Swap 使用率</span>
                <span className="metric-value">{memoryUsage.swap.percent}%</span>
              </div>
            </>
          )}
        </div>

        <div className="card">
          <h2>网络流量</h2>
          {networkTraffic && (
            <>
              <div className="metric">
                <span className="metric-label">发送字节数</span>
                <span className="metric-value">{(networkTraffic.bytes_sent / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">接收字节数</span>
                <span className="metric-value">{(networkTraffic.bytes_recv / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">发送数据包</span>
                <span className="metric-value">{networkTraffic.packets_sent}</span>
              </div>
              <div className="metric">
                <span className="metric-label">接收数据包</span>
                <span className="metric-value">{networkTraffic.packets_recv}</span>
              </div>
              <div className="metric">
                <span className="metric-label">错误输入</span>
                <span className="metric-value">{networkTraffic.errin}</span>
              </div>
              <div className="metric">
                <span className="metric-label">错误输出</span>
                <span className="metric-value">{networkTraffic.errout}</span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard