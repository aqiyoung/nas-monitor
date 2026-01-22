import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import BarChartComponent from '../components/Charts/BarChartComponent'

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

// 静态容器组件，只渲染一次，不依赖数据状态
const SystemStaticContainer: React.FC = React.memo(() => {
  return (
    <div>
      <div className="grid">
        {/* CPU 使用情况卡片容器 */}
        <div className="card">
          <h2>CPU 详细信息</h2>
          {/* CPU数据将通过动态组件传入 */}
          <div id="cpu-metrics"></div>
          {/* CPU图表将通过动态组件传入 */}
          <div id="cpu-chart"></div>
        </div>

        {/* 内存使用情况卡片容器 */}
        <div className="card">
          <h2>内存详细信息</h2>
          {/* 内存数据将通过动态组件传入 */}
          <div id="memory-metrics"></div>
        </div>
      </div>

      {/* 磁盘使用情况卡片容器 */}
      <div className="card">
        <h2>磁盘使用情况</h2>
        {/* 磁盘图表将通过动态组件传入 */}
        <div id="disk-chart"></div>
        {/* 磁盘详细数据将通过动态组件传入 */}
        <div id="disk-details"></div>
      </div>
    </div>
  )
})

// CPU指标展示组件，使用React.memo优化
const CPUMetrics: React.FC<{ cpuUsage: CPUUsage | null }> = React.memo(({ cpuUsage }) => {
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

// 内存指标展示组件，使用React.memo优化
const MemoryMetrics: React.FC<{ memoryUsage: MemoryUsage | null }> = React.memo(({ memoryUsage }) => {
  return (
    <>
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
      <div className="metric">
        <span className="metric-label">内存使用率</span>
        <span className="metric-value">{memoryUsage?.memory.percent || 0}%</span>
      </div>
      <div className="metric">
        <span className="metric-label">Swap 总量</span>
        <span className="metric-value">{((memoryUsage?.swap.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">Swap 使用率</span>
        <span className="metric-value">{memoryUsage?.swap.percent || 0}%</span>
      </div>
    </>
  )
})

// 磁盘详细信息展示组件，使用React.memo优化
const DiskDetails: React.FC<{ diskUsage: DiskUsage[] }> = React.memo(({ diskUsage }) => {
  return (
    <div style={{ marginTop: '20px' }}>
      {diskUsage.map((disk) => (
        <div key={disk.mountpoint} className="metric">
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
  )
})

// 主System组件，负责数据获取和状态管理
const NewSystem: React.FC = () => {
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [diskUsage, setDiskUsage] = useState<DiskUsage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 使用useMemo缓存图表数据，只有当相关数据变化时才重新计算
  const cpuChartData = useMemo(() => {
    return cpuUsage?.per_core_usage?.map((usage, index) => ({
      name: `核心 ${index + 1}`,
      使用率: usage
    })) || []
  }, [cpuUsage])

  const diskChartData = useMemo(() => {
    return diskUsage.map(disk => ({
      name: disk.mountpoint,
      使用率: disk.percent
    }))
  }, [diskUsage])

  const fetchData = async () => {
    try {
      const [cpuRes, memoryRes, diskRes] = await Promise.all([
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/system/disk')
      ])
      
      // 只更新数据状态，不影响容器渲染
      setCpuUsage(prev => cpuRes.data)
      setMemoryUsage(prev => memoryRes.data)
      setDiskUsage(prev => diskRes.data)
      setError(null)
    } catch (err) {
      setError('获取系统数据失败')
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
      
      {/* 动态数据展示，使用React.memo优化，只在数据变化时更新 */}
      <div className="grid">
        <div className="card">
          <h2>CPU 详细信息</h2>
          <CPUMetrics cpuUsage={cpuUsage} />
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
          <h2>内存详细信息</h2>
          <MemoryMetrics memoryUsage={memoryUsage} />
        </div>
      </div>

      <div className="card">
        <h2>磁盘使用情况</h2>
        <BarChartComponent
          data={diskChartData}
          dataKey="使用率"
          title="使用率 (%)"
          gradientId="diskGradient"
          gradientColor="#2ecc71"
          domain={[0, 100]}
          formatter={(value) => [`${value}%`, '磁盘使用率']}
        />
        <DiskDetails diskUsage={diskUsage} />
      </div>
    </div>
  )
}

export default NewSystem