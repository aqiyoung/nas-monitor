import React from 'react'

interface SystemStatus {
  hostname: string
  os: string
  os_version: string
  architecture: string
  boot_time: string
  uptime: string
}

interface SystemStatusDataProps {
  systemStatus: SystemStatus | null
}

// 系统状态数据展示组件，只负责显示数据，使用React.memo优化
const SystemStatusData: React.FC<SystemStatusDataProps> = React.memo(({ systemStatus }) => {
  return (
    <>
      <div className="metric">
        <span className="metric-label">主机名</span>
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
      </div>
    </>
  )
})

export default SystemStatusData