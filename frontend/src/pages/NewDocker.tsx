import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import BarChartComponent from '../components/Charts/BarChartComponent'

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

// 静态容器组件，只渲染一次，不依赖数据状态
const DockerStaticContainer: React.FC = React.memo(() => {
  return (
    <div>
      <div className="grid">
        {/* 容器概览卡片容器 */}
        <div className="card">
          <h2>容器概览</h2>
          {/* 容器概览数据将通过动态组件传入 */}
          <div id="container-overview"></div>
        </div>

        {/* 容器 CPU 使用率卡片容器 */}
        <div className="card">
          <h2>容器 CPU 使用率</h2>
          {/* CPU 使用率图表将通过动态组件传入 */}
          <div id="cpu-chart"></div>
        </div>

        {/* 容器内存使用率卡片容器 */}
        <div className="card">
          <h2>容器内存使用率</h2>
          {/* 内存使用率图表将通过动态组件传入 */}
          <div id="memory-chart"></div>
        </div>
      </div>

      {/* 容器列表卡片容器 */}
      <div className="card">
        <h2>容器列表</h2>
        {/* 容器列表数据将通过动态组件传入 */}
        <div id="container-list"></div>
      </div>

      {/* 镜像列表卡片容器 */}
      <div className="card">
        <h2>镜像列表</h2>
        {/* 镜像列表数据将通过动态组件传入 */}
        <div id="image-list"></div>
      </div>

      {/* 拉取镜像卡片容器 */}
      <div className="card">
        <h2>拉取最新镜像</h2>
        {/* 拉取镜像表单将通过动态组件传入 */}
        <div id="pull-image-form"></div>
      </div>
    </div>
  )
})

// 容器概览数据展示组件，使用React.memo优化
const ContainerOverview: React.FC<{ containers: DockerContainer[], images: DockerImage[] }> = React.memo(({ containers, images }) => {
  return (
    <>
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
    </>
  )
})

// 容器列表展示组件，使用React.memo优化
const ContainerList: React.FC<{ containers: DockerContainer[] }> = React.memo(({ containers }) => {
  return (
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
  )
})

// 镜像列表展示组件，使用React.memo优化
const ImageList: React.FC<{ images: DockerImage[] }> = React.memo(({ images }) => {
  return (
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
  )
})

// 拉取镜像表单组件，使用React.memo优化
const PullImageForm: React.FC<{
  newImageName: string
  setNewImageName: (value: string) => void
  handlePullImage: () => void
  isPulling: boolean
  pullSuccess: boolean
  pullError: string | null
}> = React.memo(({ 
  newImageName, 
  setNewImageName, 
  handlePullImage, 
  isPulling, 
  pullSuccess, 
  pullError 
}) => {
  return (
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
  )
})

// 主Docker组件，负责数据获取和状态管理
const NewDocker: React.FC = () => {
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

  // 使用useMemo缓存图表数据
  const cpuChartData = useMemo(() => {
    return stats.map(container => ({
      name: container.name,
      CPU使用率: (container.cpu_usage / 10000000).toFixed(2) // 转换为百分比
    }))
  }, [stats])

  const memoryChartData = useMemo(() => {
    return stats.map(container => ({
      name: container.name,
      内存使用率: ((container.memory_usage / container.memory_limit) * 100).toFixed(2) // 转换为百分比
    }))
  }, [stats])

  const fetchData = async () => {
    try {
      const [containersRes, statsRes, imagesRes] = await Promise.all([
        api.get('/api/docker/containers'),
        api.get('/api/docker/stats'),
        api.get('/api/docker/images')
      ])
      
      // 只更新数据状态，不影响容器渲染
      setContainers(prev => containersRes.data || [])
      setStats(prev => statsRes.data || [])
      setImages(prev => imagesRes.data || [])
      setError(null)
    } catch (err) {
      setError('获取 Docker 数据失败：Docker 服务可能未运行或未安装')
      console.error('Docker API Error:', err)
      // 发生错误时，将数据重置为空数组，确保页面能正常显示
      setContainers([])
      setStats([])
      setImages([])
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

  return (
    <div>
      {loading && <div className="loading-overlay">加载中...</div>}
      {error && <div className="error">{error}</div>}
      
      {/* 动态数据展示，使用React.memo优化，只在数据变化时更新 */}
      <div className="grid">
        <div className="card">
          <h2>容器概览</h2>
          <ContainerOverview containers={containers} images={images} />
        </div>

        <div className="card">
          <h2>容器 CPU 使用率</h2>
          <BarChartComponent
            data={cpuChartData}
            dataKey="CPU使用率"
            title="使用率 (%)"
            gradientId="cpuGradient"
            gradientColor="#3498db"
            domain={[0, 100]}
            formatter={(value) => [`${value}%`, 'CPU使用率']}
          />
        </div>

        <div className="card">
          <h2>容器内存使用率</h2>
          <BarChartComponent
            data={memoryChartData}
            dataKey="内存使用率"
            title="使用率 (%)"
            gradientId="memoryGradient"
            gradientColor="#2ecc71"
            domain={[0, 100]}
            formatter={(value) => [`${value}%`, '内存使用率']}
          />
        </div>
      </div>

      <div className="card">
        <h2>容器列表</h2>
        <ContainerList containers={containers} />
      </div>

      <div className="card">
        <h2>镜像列表</h2>
        <ImageList images={images} />
      </div>

      <div className="card">
        <h2>拉取最新镜像</h2>
        <PullImageForm
          newImageName={newImageName}
          setNewImageName={setNewImageName}
          handlePullImage={handlePullImage}
          isPulling={isPulling}
          pullSuccess={pullSuccess}
          pullError={pullError}
        />
      </div>
    </div>
  )
}

export default NewDocker
