import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

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

const Network: React.FC = () => {
  const [networkTraffic, setNetworkTraffic] = useState<NetworkTraffic | null>(null)
  const [networkInterfaces, setNetworkInterfaces] = useState<NetworkInterface[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

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
      if (!networkTraffic && networkInterfaces.length === 0) {
        setLoading(true)
      }
      
      // 分别处理每个请求，确保一个请求失败不会影响另一个
      const trafficPromise = api.get('/api/network/traffic')
        .then(res => {
          // 只有当数据真正变化时才更新状态
          if (dataChanged(networkTraffic, res.data)) {
            setNetworkTraffic(res.data)
          }
          return res.data
        })
        .catch(err => {
          console.error('获取网络流量失败:', err)
          return null
        })
      
      const interfacesPromise = api.get('/api/network/interfaces')
        .then(res => {
          const newInterfaces = res.data || []
          // 只有当数据真正变化时才更新状态
          if (dataChanged(networkInterfaces, newInterfaces)) {
            setNetworkInterfaces(newInterfaces)
          }
          return res.data
        })
        .catch(err => {
          console.error('获取网络接口失败:', err)
          setNetworkInterfaces([])
          return []
        })
      
      await Promise.all([trafficPromise, interfacesPromise])
      
      // 只有在有错误时才设置error，否则保持null
      if (error) {
        setError(null)
      }
    } catch (err) {
      setError('获取网络数据失败')
      console.error(err)
    } finally {
      // 只有在初始加载时才设置loading为false
      if (loading) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  // 准备图表数据
  const chartData = [
    {
      name: '发送字节',
      数值: networkTraffic?.bytes_sent || 0,
      单位: 'MB'
    },
    {
      name: '接收字节',
      数值: networkTraffic?.bytes_recv || 0,
      单位: 'MB'
    },
    {
      name: '发送数据包',
      数值: networkTraffic?.packets_sent || 0,
      单位: '个'
    },
    {
      name: '接收数据包',
      数值: networkTraffic?.packets_recv || 0,
      单位: '个'
    }
  ]

  return (
    <div>
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <div className="card">
          <h2>网络流量统计</h2>
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
        </div>

        <div className="card">
          <h2>网络流量图表</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value, name, props) => {
                  if (props.payload.name === '发送字节' || props.payload.name === '接收字节') {
                    const numValue = typeof value === 'number' ? value : parseFloat(value as string);
                    return [(numValue / (1024 * 1024)).toFixed(2) + ' MB', name]
                  }
                  return [value + ' 个', name]
                }} />
                <Area type="monotone" dataKey="数值" stroke="#3498db" fill="#3498db" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>网络接口信息</h2>
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
              {iface.ip_addresses.map((ip) => (
                <div key={ip.ip} style={{ marginLeft: '20px', fontSize: '0.9rem', color: '#666' }}>
                  {ip.ip} {ip.netmask && `(${ip.netmask})`}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Network;