import React from 'react'

interface SystemStatus {
  hostname: string
  os: string
  os_version: string
  architecture: string
  boot_time: string
  uptime: string
}

interface SystemStatusCardProps {
  data: SystemStatus | null
}

const SystemStatusCard: React.FC<SystemStatusCardProps> = React.memo(({ data }) => {
  return (
    <div className="card">
      <h2>系统状态</h2>
      <div className="metric">
        <span className="metric-label">主机名</span>
        <span className="metric-value">{data?.hostname || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">操作系统</span>
        <span className="metric-value">{data?.os || '-'} {data?.os_version || ''}</span>
      </div>
      <div className="metric">
        <span className="metric-label">架构</span>
        <span className="metric-value">{data?.architecture || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">启动时间</span>
        <span className="metric-value">{data?.boot_time || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">运行时间</span>
        <span className="metric-value">{data?.uptime || '-'}</span>
      </div>
    </div>
  )
})

export default SystemStatusCard
