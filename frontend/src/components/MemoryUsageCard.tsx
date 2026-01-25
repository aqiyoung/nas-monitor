import React from 'react'

interface MemoryUsage {
  memory: {
    total: number
    available: number
    used: number
    percent: number
  }
  swap: {
    total: number
    used: number
    free: number
    percent: number
  }
}

interface MemoryUsageCardProps {
  data: MemoryUsage | null
}

const MemoryUsageCard: React.FC<MemoryUsageCardProps> = React.memo(({ data }) => {
  return (
    <div className="card">
      <h2>内存使用情况</h2>
      <div className="metric">
        <span className="metric-label">内存使用率</span>
        <span className="metric-value">{data?.memory.percent || 0}%</span>
      </div>
      <div className="metric">
        <span className="metric-label">已用内存</span>
        <span className="metric-value">{((data?.memory.used || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">可用内存</span>
        <span className="metric-value">{((data?.memory.available || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">内存总量</span>
        <span className="metric-value">{((data?.memory.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">Swap 使用率</span>
        <span className="metric-value">{data?.swap.percent || 0}%</span>
      </div>
    </div>
  )
})

export default MemoryUsageCard
