import React, { useEffect, useState, useMemo } from 'react'
import api from '../utils/api'
import AreaChartComponent from '../components/Charts/AreaChartComponent'

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

interface NetworkInterface {
  name: string
  mac_address: string | null
  ip_addresses: {
    ip: string
    netmask: string
    broadcast?: string
  }[]
  is_up: boolean
  speed: number
  mtu: number
}

// 静态容器组件，只渲染一次，不依赖数据状态
const NetworkStaticContainer: React.FC = React.memo(() => {
  return (
    <div>
      <div className="grid">
        {/* 网络流量统计卡片容器 */}
        <div className="card">
          <h2>网络流量统计</h2>
          {/* 网络流量数据将通过动态组件传入 */}
          <div id="network-traffic-metrics"></div>
        </div>

        {/* 网络流量图表卡片容器 */}
        <div className="card">
          <h2>网络流量图表</h2>
          {/* 网络流量图表将通过动态组件传入 */}
          <div id="network-traffic-chart"></div>
        </div>
      </div>

      {/* 网络接口信息卡片容器 */}
      <div className="card">
        <h2>网络接口信息</h2>
        {/* 网络接口数据将通过动态组件传入 */}
        <div id="network-interfaces"></div>
      </div>
    </div>
  )
})

// 网络流量指标展示组件，使用React.memo优化
const NetworkTrafficMetrics: React.FC<{ networkTraffic: NetworkTraffic | null }> = React.memo(({ networkTraffic }) => {
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
      <div className="metric">
        <span className="metric-label">错误输入</span>
        <span className="metric-value">{networkTraffic?.errin || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">错误输出</span>
        <span className="metric-value">{networkTraffic?.errout || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">丢弃输入</span>
        <span className="metric-value">{networkTraffic?.dropin || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">丢弃输出</span>
        <span className="metric-value">{networkTraffic?.dropout || 0}</span>
      </div>
    </>
  )
})

// 网络接口信息展示组件，使用React.memo优化
const NetworkInterfaces: React.FC<{ networkInterfaces: NetworkInterface[] }> = React.memo(({ networkInterfaces }) => {
  return (
    <>
      {networkInterfaces.map((iface) => (
        <div key={iface.name} style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
          <div className="metric">
            <span className="metric-label">接口名称</span>
            <span className="metric-value">{iface.name}</span>
          </div>
          <div className="metric">
            <span className="metric-label">MAC 地址</span>
            <span className="metric-value">{iface.mac_address || 'N/A'}</span>
          </div>
          <div className="metric">
            <span className="metric-label">状态</span>
            <span className="metric-value" style={{ color: iface.is_up ? '#2ecc71' : '#e74c3c' }}>
              {iface.is_up ? '已启动' : '已关闭'}
            </span>
          </div>
          <div className="metric">
            <span className="metric-label">速度</span>
            <span className="metric-value">{iface.speed} Mbps</span>
          </div>
          <div className="metric">
            <span className="metric-label">MTU</span>
            <span className="metric-value">{iface.mtu}</span>
          </div>
          <div style={{ marginTop: '10px' }}>
            <div className="metric-label" style={{ marginBottom: '5px' }}>IP 地址</div>
            {iface.ip_addresses && iface.ip_addresses.length > 0 ? (
              iface.ip_addresses.map((ip) => (
                <div key={ip.ip} style={{ marginLeft: '20px', fontSize: '0.9rem', color: '#666' }}>
                  {ip.ip} {ip.netmask && `(${ip.netmask})`}
                </div>
              ))
            ) : (
              <div style={{ marginLeft: '20px', fontSize: '0.9rem', color: '#999' }}>无 IP 地址</div>
            )}
          </div>
        </div>
      ))}
    </>
  )
})

// 主Network组件，负责数据获取和状态管理
const NewNetwork: React.FC = () => {
  const [networkTraffic, setNetworkTraffic] = useState<NetworkTraffic | null>(null)
  const [networkInterfaces, setNetworkInterfaces] = useState<NetworkInterface[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 使用useMemo缓存图表数据，只有当networkTraffic变化时才重新计算
  // 将字节数转换为MB，数据包保持不变
  const chartData = useMemo(() => {
    return [
      { name: '发送字节', 数值: (networkTraffic?.bytes_sent || 0) / (1024 * 1024), 单位: 'MB' },
      { name: '接收字节', 数值: (networkTraffic?.bytes_recv || 0) / (1024 * 1024), 单位: 'MB' }
    ]
  }, [networkTraffic])

  const fetchData = async () => {
    try {
      // 分别处理每个请求，确保一个请求失败不会影响另一个
      const trafficPromise = api.get('/network/traffic')
        .then(res => {
          setNetworkTraffic(prev => res.data)
          return res.data
        })
        .catch(err => {
          console.error('获取网络流量失败:', err)
          return null
        })
      
      const interfacesPromise = api.get('/network/interfaces')
        .then(res => {
          const newInterfaces = res.data || []
          setNetworkInterfaces(prev => newInterfaces)
          return res.data
        })
        .catch(err => {
          console.error('获取网络接口失败:', err)
          setNetworkInterfaces(prev => [])
          return []
        })
      
      await Promise.all([trafficPromise, interfacesPromise])
      setError(null)
    } catch (err) {
      setError('获取网络数据失败')
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
          <h2>网络流量统计</h2>
          <NetworkTrafficMetrics networkTraffic={networkTraffic} />
        </div>

        <div className="card">
          <h2>网络流量图表</h2>
          <AreaChartComponent
            data={chartData}
            dataKey="数值"
            title="数据量 (MB)"
            gradientId="networkGradient"
            gradientColor="#3498db"
            formatter={(value, name) => {
              const numValue = typeof value === 'number' ? value : parseFloat(value as string);
              return [numValue.toFixed(2) + ' MB', name]
            }}
          />
        </div>
      </div>

      <div className="card">
        <h2>网络接口信息</h2>
        <NetworkInterfaces networkInterfaces={networkInterfaces} />
      </div>
    </div>
  )
}

export default NewNetwork