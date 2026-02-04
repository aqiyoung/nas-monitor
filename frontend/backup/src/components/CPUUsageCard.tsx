import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface CPUUsage {
  total_usage: number
  cpu_count: {
    physical: number
    logical: number
  }
}

interface CPUChartData {
  name: string
  使用率: number
}

interface CPUUsageCardProps {
  data: CPUUsage | null
  cpuChartData: CPUChartData[]
}

const CPUUsageCard: React.FC<CPUUsageCardProps> = React.memo(({ data, cpuChartData }) => {
  return (
    <div className="card">
      <h2>CPU 使用情况</h2>
      <div className="metric">
        <span className="metric-label">总使用率</span>
        <span className="metric-value">{data?.total_usage || 0}%</span>
      </div>
      <div className="metric">
        <span className="metric-label">物理核心</span>
        <span className="metric-value">{data?.cpu_count.physical || 0}</span>
      </div>
      <div className="metric">
        <span className="metric-label">逻辑核心</span>
        <span className="metric-value">{data?.cpu_count.logical || 0}</span>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart 
            data={cpuChartData} 
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }} 
            animationDuration={0}
          >
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
              fill="#3498db" 
              radius={[4, 4, 0, 0]} 
              barSize={30}
              animationDuration={0}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
})

export default CPUUsageCard
