import React, { useMemo } from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface ChartDataItem {
  name: string
  [key: string]: number | string
}

interface AreaChartComponentProps {
  data: ChartDataItem[]
  dataKey: string
  title: string
  gradientId: string
  gradientColor: string
  formatter?: (value: any, name: string, props: any) => [string, string]
}

// 通用的面积图组件，使用React.memo优化，只在数据变化时更新
const AreaChartComponent: React.FC<AreaChartComponentProps> = React.memo(({
  data,
  dataKey,
  title,
  gradientId,
  gradientColor,
  formatter = (value) => [`${value}`, '']
}) => {
  // 使用useMemo缓存图表配置，只有在依赖变化时才重新计算
  const chartConfig = useMemo(() => ({
    data,
    margin: { top: 5, right: 30, left: 20, bottom: 5 }
  }), [data])

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart 
          data={chartConfig.data}
          margin={chartConfig.margin}
        >
          <defs>
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={gradientColor} stopOpacity={0.8}/>
              <stop offset="95%" stopColor={gradientColor} stopOpacity={0.2}/>
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
            tick={{ fontSize: 12, fill: '#666' }} 
            axisLine={{ stroke: '#ddd' }} 
            tickLine={{ stroke: '#ddd' }}
            label={{ 
              value: title, 
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
            formatter={formatter}
            labelStyle={{ fontWeight: 'bold', color: '#333' }}
          />
          <Area 
            type="monotone" 
            dataKey={dataKey} 
            stroke={gradientColor} 
            fill={`url(#${gradientId})`} 
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
})

export default AreaChartComponent