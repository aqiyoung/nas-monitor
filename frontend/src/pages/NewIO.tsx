import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import BarChartComponent from '../components/Charts/BarChartComponent'

interface DiskIO {
  disk_name: string
  read_bytes: number
  write_bytes: number
  read_count: number
  write_count: number
  read_time: number
  write_time: number
}

interface SystemIO {
  total_read_bytes: number
  total_write_bytes: number
  total_read_count: number
  total_write_count: number
  total_read_time: number
  total_write_time: number
}

// 静态容器组件，只渲染一次，不依赖数据状态
const IOStaticContainer: React.FC = React.memo(() => {
  return (
    <div>
      <div className="grid">
        {/* 系统 IO 统计卡片容器 */}
        <div className="card">
          <h2>系统 IO 统计</h2>
          {/* 系统 IO 数据将通过动态组件传入 */}
          <div id="system-io-metrics"></div>
        </div>

        {/* 磁盘 IO 概览卡片容器 */}
        <div className="card">
          <h2>磁盘 IO 概览</h2>
          {/* 磁盘 IO 图表将通过动态组件传入 */}
          <div id="disk-io-chart"></div>
        </div>
      </div>

      {/* 磁盘 IO 详细信息卡片容器 */}
      <div className="card">
        <h2>磁盘 IO 详细信息</h2>
        {/* 磁盘 IO 详细数据将通过动态组件传入 */}
        <div id="disk-io-details"></div>
      </div>
    </div>
  )
})

// 系统 IO 指标展示组件，使用React.memo优化
const SystemIOMetrics: React.FC<{ systemIO: SystemIO | null }> = React.memo(({ systemIO }) => {
  return (
    <>
      <div className="metric">
        <span className="metric-label">总读取字节</span>
        <span className="metric-value">{((systemIO?.total_read_bytes || 0) / (1024 * 1024)).toFixed(2)} MB</span>
      </div>
      <div className="metric">
        <span className="metric-label">总写入字节</span>
        <span className="metric-value">{((systemIO?.total_write_bytes || 0) / (1024 * 1024)).toFixed(2)} MB</span>
      </div>
      <div className="metric">
        <span className="metric-label">总读取次数</span>
        <span className="metric-value">{systemIO?.total_read_count || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">总写入次数</span>
        <span className="metric-value">{systemIO?.total_write_count || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">总读取时间</span>
        <span className="metric-value">{systemIO?.total_read_time || 0} ms</span>
      </div>
      <div className="metric">
        <span className="metric-label">总写入时间</span>
        <span className="metric-value">{systemIO?.total_write_time || 0} ms</span>
      </div>
    </>
  )
})

// 磁盘 IO 详细信息展示组件，使用React.memo优化
const DiskIODetails: React.FC<{ diskIO: DiskIO[] }> = React.memo(({ diskIO }) => {
  return (
    <div>
      {diskIO.map((disk) => (
        <div key={disk.disk_name} style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
          <div className="metric">
            <span className="metric-label">磁盘名称</span>
            <span className="metric-value">{disk.disk_name}</span>
          </div>
          <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '10px' }}>
            <div>
              <div className="metric">
                <span className="metric-label">读取字节</span>
                <span className="metric-value">{(disk.read_bytes / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">写入字节</span>
                <span className="metric-value">{(disk.write_bytes / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">读取次数</span>
                <span className="metric-value">{disk.read_count}</span>
              </div>
              <div className="metric">
                <span className="metric-label">写入次数</span>
                <span className="metric-value">{disk.write_count}</span>
              </div>
              <div className="metric">
                <span className="metric-label">读取时间</span>
                <span className="metric-value">{disk.read_time} ms</span>
              </div>
              <div className="metric">
                <span className="metric-label">写入时间</span>
                <span className="metric-value">{disk.write_time} ms</span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
})

// 主IO组件，负责数据获取和状态管理
const NewIO: React.FC = () => {
  const [diskIO, setDiskIO] = useState<DiskIO[]>([])
  const [systemIO, setSystemIO] = useState<SystemIO | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 使用useMemo缓存图表数据，只有当diskIO变化时才重新计算
  const diskIOChartData = useMemo(() => {
    return diskIO.map(disk => ({
      name: disk.disk_name,
      读取字节: disk.read_bytes / (1024 * 1024), // MB
      写入字节: disk.write_bytes / (1024 * 1024) // MB
    }))
  }, [diskIO])

  const fetchData = async () => {
    try {
      const [diskRes, systemRes] = await Promise.all([
        api.get('/io/disk'),
        api.get('/io/system')
      ])
      
      // 只更新数据状态，不影响容器渲染
      setDiskIO(prev => diskRes.data)
      setSystemIO(prev => systemRes.data)
      setError(null)
    } catch (err) {
      setError('获取 IO 数据失败')
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
          <h2>系统 IO 统计</h2>
          <SystemIOMetrics systemIO={systemIO} />
        </div>

        <div className="card">
          <h2>磁盘 IO 概览</h2>
          <BarChartComponent
            data={diskIOChartData}
            dataKey={['读取字节', '写入字节']}
            title="数据量 (MB)"
            gradientId={['readGradient', 'writeGradient']}
            gradientColor={['#3498db', '#e74c3c']}
            formatter={(value) => [(typeof value === 'number' ? value.toFixed(2) : value) + ' MB', '']}
            showLegend={true}
          />
        </div>
      </div>

      <div className="card">
        <h2>磁盘 IO 详细信息</h2>
        <DiskIODetails diskIO={diskIO} />
      </div>
    </div>
  )
}

export default NewIO
