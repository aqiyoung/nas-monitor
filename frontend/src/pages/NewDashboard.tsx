import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import SystemStatusData from '../components/SystemStatusData'
import BarChartComponent from '../components/Charts/BarChartComponent'

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
  wifi_name?: string | null
}

// 数据展示组件，只负责显示数据，使用React.memo优化
const CPUUsageData: React.FC<{ cpuUsage: CPUUsage | null }> = React.memo(({ cpuUsage }) => {
  return (
    <>
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
    </>
  )
})



const MemoryUsageData: React.FC<{ memoryUsage: MemoryUsage | null }> = React.memo(({ memoryUsage }) => {
  return (
    <>
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
    </>
  )
})

const NetworkTrafficData: React.FC<{ networkTraffic: NetworkTraffic | null }> = React.memo(({ networkTraffic }) => {
  return (
    <>
      {/* 添加WiFi名称显示 */}
      {networkTraffic?.wifi_name && (
        <div className="metric">
          <span className="metric-label">当前WiFi</span>
          <span className="metric-value">{networkTraffic.wifi_name}</span>
        </div>
      )}
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
    </>
  )
})



// 主Dashboard组件，负责数据获取和状态管理
const NewDashboard: React.FC = () => {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null)
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [networkTraffic, setNetworkTraffic] = useState<NetworkTraffic | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 使用useMemo缓存CPU图表数据，只有当cpuUsage变化时才重新计算
  const cpuChartData = useMemo(() => {
    return cpuUsage?.per_core_usage?.map((usage, index) => ({
      name: `核心 ${index + 1}`,
      使用率: usage
    })) || []
  }, [cpuUsage])

  const fetchData = async () => {
    try {
      const [systemRes, cpuRes, memoryRes, networkRes] = await Promise.all([
        api.get('/api/system/status'),
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/network/traffic')
      ])
      
      // 只更新数据状态，不影响容器渲染
      setSystemStatus(prev => systemRes.data)
      setCpuUsage(prev => cpuRes.data)
      setMemoryUsage(prev => memoryRes.data)
      setNetworkTraffic(prev => networkRes.data)
      setError(null)
    } catch (err) {
      setError('获取数据失败，请检查后端服务是否正常运行')
      console.error(err)
    } finally {
      // 初始加载完成后关闭loading，后续刷新不再显示
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
      {error && <div className="error">{error}</div>}
      
      {/* 动态数据展示，直接挂载到容器中 */}
      <div className="grid">
        <div className="card">
          <h2>系统状态</h2>
          <SystemStatusData systemStatus={systemStatus} />
        </div>

        <div className="card">
          <h2>CPU 使用情况</h2>
          <CPUUsageData cpuUsage={cpuUsage} />
          {/* 添加CPU核心使用率图表，使用通用的BarChartComponent */}
          <BarChartComponent
            data={cpuChartData}
            dataKey="使用率"
            title="使用率 (%)"
            gradientId="cpuGradient"
            gradientColor="#3498db"
            domain={[0, 100]}
            formatter={(value) => [`${value}%`, 'CPU使用率']}
          />
        </div>

        <div className="card">
          <h2>内存使用情况</h2>
          <MemoryUsageData memoryUsage={memoryUsage} />
        </div>

        <div className="card">
          <h2>网络流量</h2>
          <NetworkTrafficData networkTraffic={networkTraffic} />
        </div>
      </div>
    </div>
  )
}

export default NewDashboard