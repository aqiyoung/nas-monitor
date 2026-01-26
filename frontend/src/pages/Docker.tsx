import React, { useEffect, useState } from 'react'
import api from '../utils/api'
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
  // 拉取镜像相关状态
  const [newImageName, setNewImageName] = useState<string>('')
  const [isPulling, setIsPulling] = useState<boolean>(false)
  const [pullSuccess, setPullSuccess] = useState<boolean>(false)
  const [pullError, setPullError] = useState<string | null>(null)

  // 数据比较函数，用于判断数据是否真正变化
  const dataChanged = (oldData: any, newData: any): boolean => {
    if (oldData === null || newData === null) {
      return oldData !== newData
    }
    
    // 对于数组，比较其长度和JSON字符串
    if (Array.isArray(oldData) && Array.isArray(newData)) {
      if (oldData.length !== newData.length) {
        return true
      }
      return JSON.stringify(oldData) !== JSON.stringify(newData)
    }
    
    // 对于对象，比较其JSON字符串
    return JSON.stringify(oldData) !== JSON.stringify(newData)
  }

  const fetchData = async () => {
    try {
      // 只有在初始加载且没有任何数据时才显示loading
      if (containers.length === 0 && stats.length === 0 && images.length === 0) {
        setLoading(true)
      }
      
      const [containersRes, statsRes, imagesRes] = await Promise.all([
        api.get('/api/docker/containers'),
        api.get('/api/docker/stats'),
        api.get('/api/docker/images')
      ])
      
      // 只有当数据真正变化时才更新状态，避免不必要的重新渲染
      const newContainers = containersRes.data || []
      const newStats = statsRes.data || []
      const newImages = imagesRes.data || []
      
      if (dataChanged(containers, newContainers)) {
        setContainers(newContainers)
      }
      if (dataChanged(stats, newStats)) {
        setStats(newStats)
      }
      if (dataChanged(images, newImages)) {
        setImages(newImages)
      }
      
      // 只有在有错误时才设置error，否则保持null
      if (error) {
        setError(null)
      }
    } catch (err) {
      // 发生错误时，仅更新error状态，不重置数据，避免页面闪烁
      setError('获取 Docker 数据失败：Docker 服务可能未运行或未安装')
      console.error('Docker API Error:', err)
    } finally {
      // 始终在请求完成后设置loading为false，确保页面正常显示
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  // 处理拉取镜像
  const handlePullImage = async () => {
    if (!newImageName.trim()) return
    
    setPullSuccess(false)
    setPullError(null)
    setIsPulling(true)
    
    try {
      await api.post('/api/docker/images/pull', {
        image_name: newImageName
      })
      
      // 拉取成功，刷新镜像列表
      fetchData()
      setPullSuccess(true)
      setNewImageName('')
    } catch (err: any) {
      console.error('Pull image error:', err)
      setPullError(err.response?.data?.detail || '拉取镜像失败，请检查镜像名称是否正确')
    } finally {
      setIsPulling(false)
    }
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
      {error && <div className="error-overlay">{error}</div>}
      
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
              <BarChart 
                data={cpuChartData} 
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }} 
                animationDuration={0} 
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  tick={{ fontSize: 12, fill: '#666' }} 
                  axisLine={{ stroke: '#ddd' }} 
                  tickLine={{ stroke: '#ddd' }}
                />
                <YAxis 
                  domain={[0, 100]} 
                  tick={{ fontSize: 12, fill: '#666' }} 
                  axisLine={{ stroke: '#ddd' }} 
                  tickLine={{ stroke: '#ddd' }}
                  label={{ 
                    value: '使用率 (%)', 
                    angle: -90, 
                    position: 'insideLeft',
                    style: { textAnchor: 'middle', fontSize: 12, fill: '#666' }
                  }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    border: '1px solid #e0e0e0'
                  }} 
                  formatter={(value) => [`${value}%`, 'CPU使用率']}
                  labelStyle={{ fontWeight: 'bold', color: '#333' }}
                />
                <Bar 
                  dataKey="CPU使用率" 
                  fill="#3498db" 
                  radius={[4, 4, 0, 0]} 
                  barSize={30}
                  animationDuration={0}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <h2>容器内存使用率</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart 
                data={memoryChartData} 
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }} 
                animationDuration={0} 
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" vertical={false} />
                <XAxis 
                  dataKey="name" 
                  tick={{ fontSize: 12, fill: '#666' }} 
                  axisLine={{ stroke: '#ddd' }} 
                  tickLine={{ stroke: '#ddd' }}
                />
                <YAxis 
                  domain={[0, 100]} 
                  tick={{ fontSize: 12, fill: '#666' }} 
                  axisLine={{ stroke: '#ddd' }} 
                  tickLine={{ stroke: '#ddd' }}
                  label={{ 
                    value: '使用率 (%)', 
                    angle: -90, 
                    position: 'insideLeft',
                    style: { textAnchor: 'middle', fontSize: 12, fill: '#666' }
                  }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    borderRadius: '8px', 
                    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                    border: '1px solid #e0e0e0'
                  }} 
                  formatter={(value) => [`${value}%`, '内存使用率']}
                  labelStyle={{ fontWeight: 'bold', color: '#333' }}
                />
                <Bar 
                  dataKey="内存使用率" 
                  fill="#2ecc71" 
                  radius={[4, 4, 0, 0]} 
                  barSize={30}
                  animationDuration={0}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>容器列表</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
          {containers.map((container) => (
            <div key={container.id} style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
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
          {images.map((image) => (
            <div key={image.id} style={{ padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
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

      <div className="card">
        <h2>拉取最新镜像</h2>
        <div style={{ marginBottom: '20px' }}>
          <div className="metric">
            <span className="metric-label">镜像名称</span>
            <input
              type="text"
              placeholder="例如: nginx, docker.io/library/nginx, nginx:latest"
              value={newImageName}
              onChange={(e) => setNewImageName(e.target.value)}
              style={{
                width: '100%',
                padding: '10px',
                borderRadius: '4px',
                border: '1px solid #ddd',
                fontSize: '16px',
                marginTop: '5px'
              }}
              disabled={isPulling}
            />
          </div>
          <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
            <button
              className="btn btn-primary"
              onClick={handlePullImage}
              disabled={isPulling || !newImageName.trim()}
              style={{
                padding: '10px 20px',
                backgroundColor: '#3498db',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                fontSize: '16px',
                cursor: isPulling || !newImageName.trim() ? 'not-allowed' : 'pointer',
                opacity: isPulling || !newImageName.trim() ? 0.7 : 1
              }}
            >
              {isPulling ? '拉取中...' : '拉取镜像'}
            </button>
          </div>
          {pullError && (
            <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#fee', color: '#c33', borderRadius: '4px' }}>
              {pullError}
            </div>
          )}
          {pullSuccess && (
            <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#efe', color: '#3c3', borderRadius: '4px' }}>
              镜像拉取成功！
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Docker;