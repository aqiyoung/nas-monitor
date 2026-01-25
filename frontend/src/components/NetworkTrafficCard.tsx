import React from 'react'

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

interface NetworkTrafficCardProps {
  data: NetworkTraffic | null
}

const NetworkTrafficCard: React.FC<NetworkTrafficCardProps> = React.memo(({ data }) => {
  return (
    <div className="card">
      <h2>网络流量</h2>
      <div className="metric">
        <span className="metric-label">发送字节数</span>
        <span className="metric-value">{((data?.bytes_sent || 0) / (1024 * 1024)).toFixed(2)} MB</span>
      </div>
      <div className="metric">
        <span className="metric-label">接收字节数</span>
        <span className="metric-value">{((data?.bytes_recv || 0) / (1024 * 1024)).toFixed(2)} MB</span>
      </div>
      <div className="metric">
        <span className="metric-label">发送数据包</span>
        <span className="metric-value">{data?.packets_sent || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">接收数据包</span>
        <span className="metric-value">{data?.packets_recv || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">错误输入</span>
        <span className="metric-value">{data?.errin || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">错误输出</span>
        <span className="metric-value">{data?.errout || 0}</span>
      </div>
    </div>
  )
})

export default NetworkTrafficCard
