import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

// 自定义Tooltip组件，用于显示更详细的信息
const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        backgroundColor: 'white',
        border: '1px solid #ccc',
        borderRadius: '8px',
        padding: '10px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
        fontSize: '12px',
        fontWeight: '500'
      }}>
        <p style={{ margin: '0 0 5px 0', color: '#333', fontWeight: '600' }}>{label}</p>
        <p style={{ margin: 0, color: '#667eea' }}>
          {payload[0].name}: {payload[0].value}%
        </p>
      </div>
    )
  }
  return null
}

interface BarChartComponentProps {
  data: any[]
  width?: number
  height?: number
  title?: string
}

const BarChartComponent: React.FC<BarChartComponentProps> = ({ 
  data, 
  width = 400, 
  height = 300,
  title = ''
}) => {
  return (
    <div>
      {title && <h3 style={{ marginBottom: '10px', fontSize: '16px', color: '#333' }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <BarChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 12 }}
            stroke="#666"
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            stroke="#666"
            domain={[0, 100]}
            tickFormatter={(value) => `${value}%`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="value" 
            fill="#667eea"
            radius={[4, 4, 0, 0]}
            animationDuration={1500}
            barSize={20}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default BarChartComponent