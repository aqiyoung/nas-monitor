import React, { useMemo } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface CPUUsage {
  total_usage: number
  per_core_usage: number[]
  cpu_count: {
    physical: number
    logical: number
  }
}

interface CPUUsageCardProps {
  cpuUsage: CPUUsage | null
}

const CPUUsageCard: React.FC<CPUUsageCardProps> = React.memo(({ cpuUsage }) => {
  // 使用useMemo缓存图表数据，只有当cpuUsage变化时才重新计算
  const cpuChartData = useMemo(() => {
    return cpuUsage?.per_core_usage?.map((usage, index) => ({
      name: `核心 ${index + 1}`,
      使用率: usage
    })) || []
  }, [cpuUsage])

  return (
    <div className="card">
      <h2>CPU 使用情况</h2>
      <div className="metric">
        <span className="metric-label">总使用率</span>
        <span className="metric-value">{cpuUsage?.total_usage || 0}%</span>
      </div>
      <div className="metric">
        <span className="metric-label">物理核心</span>
        <span className="metric-value">{cpuUsage?.cpu_count.physical || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">逻辑核心</span>
        <span className="metric-value">{cpuUsage?.cpu_count.logical || 0}</span>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={cpuChartData} 
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <defs>
              <linearGradient id="cpuGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3498db" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#3498db" stopOpacity={0.2}/>
              </linearGradient>
            </defs>
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
              dataKey="使用率" 
              fill="url(#cpuGradient)" 
              radius={[4, 4, 0, 0]} 
              barSize={30}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
})

export default CPUUsageCard