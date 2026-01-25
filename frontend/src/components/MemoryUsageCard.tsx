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
<<<<<<< HEAD
  data: MemoryUsage | null
}

const MemoryUsageCard: React.FC<MemoryUsageCardProps> = React.memo(({ data }) => {
=======
  memoryUsage: MemoryUsage | null
}

const MemoryUsageCard: React.FC<MemoryUsageCardProps> = React.memo(({ memoryUsage }) => {
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
  return (
    <div className="card">
      <h2>内存使用情况</h2>
      <div className="metric">
        <span className="metric-label">内存使用率</span>
<<<<<<< HEAD
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
=======
        <span className="metric-value">{memoryUsage?.memory.percent || 0}%</span>
      </div>
      <div className="metric">
        <span className="metric-label">已用内存</span>
        <span className="metric-value">{((memoryUsage?.memory.used || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">可用内存</span>
        <span className="metric-value">{((memoryUsage?.memory.available || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">内存总量</span>
        <span className="metric-value">{((memoryUsage?.memory.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
      </div>
      <div className="metric">
        <span className="metric-label">Swap 使用率</span>
        <span className="metric-value">{memoryUsage?.swap.percent || 0}%</span>
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
      </div>
    </div>
  )
})

<<<<<<< HEAD
export default MemoryUsageCard
=======
export default MemoryUsageCard
>>>>>>> 8dc063b0ff58679f36031866f642f62d32ea8e90
