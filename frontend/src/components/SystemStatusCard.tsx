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
<<<<<<< HEAD
  data: SystemStatus | null
}

const SystemStatusCard: React.FC<SystemStatusCardProps> = React.memo(({ data }) => {
=======
  systemStatus: SystemStatus | null
}

const SystemStatusCard: React.FC<SystemStatusCardProps> = React.memo(({ systemStatus }) => {
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
  return (
    <div className="card">
      <h2>系统状态</h2>
      <div className="metric">
        <span className="metric-label">主机名</span>
<<<<<<< HEAD
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
=======
        <span className="metric-value">{systemStatus?.hostname || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">操作系统</span>
        <span className="metric-value">{systemStatus?.os || '-'} {systemStatus?.os_version || ''}</span>
      </div>
      <div className="metric">
        <span className="metric-label">架构</span>
        <span className="metric-value">{systemStatus?.architecture || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">启动时间</span>
        <span className="metric-value">{systemStatus?.boot_time || '-'}</span>
      </div>
      <div className="metric">
        <span className="metric-label">运行时间</span>
        <span className="metric-value">{systemStatus?.uptime || '-'}</span>
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
      </div>
    </div>
  )
})

<<<<<<< HEAD
export default SystemStatusCard
=======
export default SystemStatusCard
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
