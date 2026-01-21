import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface DockerContainer {
  id: string
  name: string
  status: string
  image: string
  created: string
  ports: any
  command: string[]
}

interface DockerStats {
  name: string
  cpu_usage: number
  memory_usage: number
  memory_limit: number
  network: any
  blkio: any
}

interface DockerImage {
  id: string
  tags: string[]
  created: string
  size: number
  virtual_size: number
}

const Docker: React.FC = () => {
  const [containers, setContainers] = useState<DockerContainer[]>([])
  const [stats, setStats] = useState<DockerStats[]>([])
  const [images, setImages] = useState<DockerImage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    try {
      // 初始加载时显示loading，后续刷新只更新数据，不显示loading
      const showLoading = containers.length === 0 && stats.length === 0 && images.length === 0
      if (showLoading) {
        setLoading(true)
      }
      
      const [containersRes, statsRes, imagesRes] = await Promise.all([
        axios.get('/api/docker/containers'),
        axios.get('/api/docker/stats'),
        axios.get('/api/docker/images')
      ])
      
      setContainers(containersRes.data)
      setStats(statsRes.data)
      setImages(imagesRes.data)
      setError(null)
    } catch (err) {
      setError('获取 Docker 数据失败')
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

  // 准备图表数据
  const cpuChartData = stats.map(container => ({
    name: container.name,
    CPU使用率: (container.cpu_usage / 10000000).toFixed(2) // 转换为百分比
  }))

  const memoryChartData = stats.map(container => ({
    name: container.name,
    内存使用率: ((container.memory_usage / container.memory_limit) * 100).toFixed(2) // 转换为百分比
  }))

  return (
    <div>
      <div className="grid">
        <div className="card">
          <h2>容器概览</h2>
          <div className="metric">
            <span className="metric-label">总容器数</span>
            <span className="metric-value">{containers.length}</span>
          </div>
          <div className="metric">
            <span className="metric-label">运行中容器</span>
            <span className="metric-value">{containers.filter(c => c.status === 'running').length}</span>
          </div>
          <div className="metric">
            <span className="metric-label">停止容器</span>
            <span className="metric-value">{containers.filter(c => c.status !== 'running').length}</span>
          </div>
          <div className="metric">
            <span className="metric-label">镜像数量</span>
            <span className="metric-value">{images.length}</span>
          </div>
        </div>

        <div className="card">
          <h2>容器 CPU 使用率</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cpuChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip formatter={(value) => [value + ' %', 'CPU使用率']} />
                <Bar dataKey="CPU使用率" fill="#3498db" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <h2>容器内存使用率</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={memoryChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip formatter={(value) => [value + ' %', '内存使用率']} />
                <Bar dataKey="内存使用率" fill="#2ecc71" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>容器列表</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
          {containers.map((container, index) => (
            <div key={index} style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
              <div className="metric">
                <span className="metric-label">容器名称</span>
                <span className="metric-value">{container.name}</span>
              </div>
              <div className="metric">
                <span className="metric-label">状态</span>
                <span className="metric-value" style={{ color: container.status === 'running' ? '#2ecc71' : '#e74c3c' }}>
                  {container.status}
                </span>
              </div>
              <div className="metric">
                <span className="metric-label">镜像</span>
                <span className="metric-value" style={{ fontSize: '0.8rem' }}>{container.image}</span>
              </div>
              <div className="metric">
                <span className="metric-label">创建时间</span>
                <span className="metric-value" style={{ fontSize: '0.8rem' }}>
                  {new Date(container.created).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2>镜像列表</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
          {images.map((image, index) => (
            <div key={index} style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
              <div className="metric">
                <span className="metric-label">镜像 ID</span>
                <span className="metric-value" style={{ fontSize: '0.8rem' }}>{image.id.substring(0, 12)}</span>
              </div>
              <div className="metric">
                <span className="metric-label">标签</span>
                <span className="metric-value" style={{ fontSize: '0.8rem' }}>
                  {image.tags.length > 0 ? image.tags.join(', ') : 'none'}
                </span>
              </div>
              <div className="metric">
                <span className="metric-label">大小</span>
                <span className="metric-value">{(image.size / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">虚拟大小</span>
                <span className="metric-value">{(image.virtual_size / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">创建时间</span>
                <span className="metric-value" style={{ fontSize: '0.8rem' }}>
                  {new Date(image.created).toLocaleString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Docker