import React, { useMemo } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, TooltipProps } from 'recharts'

interface ChartDataItem {
  name: string
  [key: string]: number | string
}

interface BarChartComponentProps {
  data: ChartDataItem[]
  dataKey: string | string[]
  title: string
  gradientId: string | string[]
  gradientColor: string | string[]
  domain?: [number, number]
  formatter?: (value: any) => [string, string]
  showLegend?: boolean
}

// 自定义工具提示组件
const CustomTooltip: React.FC<TooltipProps<number, string>> = ({ active, payload, label, coordinate }) => {
  if (active && payload && payload.length && coordinate) {
    return (
      <div style={{
        backgroundColor: 'rgba(255, 255, 255, 0.98)',
        backdropFilter: 'blur(12px)',
        borderRadius: '12px',
        boxShadow: '0 8px 25px rgba(0, 0, 0, 0.15)',
        border: '1px solid rgba(200, 200, 200, 0.3)',
        color: '#333',
        padding: '12px 16px',
        fontFamily: 'inherit',
        overflow: 'visible',
        zIndex: 10000,
        pointerEvents: 'none',
        outline: 'none',
        boxSizing: 'border-box',
        position: 'absolute',
        left: `${coordinate.x}px`,
        top: `${coordinate.y}px`,
        transform: 'translate(-50%, -100%)',
        marginLeft: '0px',
        marginTop: '-10px'
      }}>
        <div style={{
          fontWeight: '600',
          color: '#333',
          marginBottom: '8px',
          fontSize: '1rem',
          background: 'linear-gradient(135deg, #0066cc 0%, #00aaff 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          textAlign: 'center',
          display: 'block',
          width: '100%'
        }}>{label}</div>
        {payload.map((entry, index) => (
          <div key={`item-${index}`} style={{
            color: '#666',
            fontSize: '0.95rem',
            padding: '4px 0',
            background: 'transparent',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            width: '100%'
          }}>
            <span>{entry.name}:</span>
            <span style={{
              fontWeight: '700',
              color: '#333',
              marginLeft: '12px',
              background: 'linear-gradient(135deg, #0066cc 0%, #00aaff 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              display: 'inline-block'
            }}>{entry.value}%</span>
          </div>
        ))}
      </div>
    )
  }
  return null
}

// 通用的柱状图组件，使用React.memo优化，只在数据变化时更新
const BarChartComponent: React.FC<BarChartComponentProps> = React.memo(({
  data,
  dataKey,
  title,
  gradientId,
  gradientColor,
  domain = [0, 100],
  formatter = (value) => [`${value}`, ''],
  showLegend = false
}) => {
  // 使用useMemo缓存图表配置，只有在依赖变化时才重新计算
  const chartConfig = useMemo(() => ({
    data,
    margin: { top: 5, right: 30, left: 20, bottom: 5 },
    domain
  }), [data, domain])

  // 将单个值转换为数组，方便统一处理
  const dataKeys = Array.isArray(dataKey) ? dataKey : [dataKey]
  const gradientIds = Array.isArray(gradientId) ? gradientId : [gradientId]
  const gradientColors = Array.isArray(gradientColor) ? gradientColor : [gradientColor]

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart 
          data={chartConfig.data} 
          margin={chartConfig.margin}
          barGap={8}
          barCategoryGap={20}
          style={{ border: 'none' }}
          animationDuration={0}
        >
          <defs>
            {/* 为每个数据系列创建渐变 */}
            {gradientIds.map((id, index) => (
              <linearGradient key={id} id={id} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={gradientColors[index]} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={gradientColors[index]} stopOpacity={0.2}/>
              </linearGradient>
            ))}
          </defs>
          <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="rgba(220, 220, 220, 0.4)" />
          <XAxis 
            dataKey="name" 
            tick={{ fontSize: 12, fill: '#888' }} 
            axisLine={false} 
            tickLine={false}
          />
          <YAxis 
            domain={chartConfig.domain} 
            tick={{ fontSize: 12, fill: '#888' }} 
            axisLine={false} 
            tickLine={false}
            label={{ 
              value: title, 
              angle: -90, 
              position: 'insideLeft',
              style: { textAnchor: 'middle', fontSize: 12, fill: '#888' }
            }}
          />
          {/* 使用自定义工具提示组件，完全控制样式 */}
          <Tooltip 
            content={<CustomTooltip />} 
            formatter={formatter} 
            cursor={{ fill: 'transparent' }} 
            wrapperStyle={{
              border: 'none',
              outline: 'none',
              background: 'transparent',
              overflow: 'visible',
              zIndex: 10000,
              display: 'inline-block'
            }}
            contentWrapperStyle={{
              background: 'transparent',
              border: 'none',
              boxShadow: 'none',
              overflow: 'visible'
            }}
          />
          {showLegend && (
            <Legend 
              wrapperStyle={{ paddingTop: 10 }} 
              iconType="circle"
              iconSize={10}
              formatter={(value) => <span style={{ fontSize: 12, color: '#888' }}>{value}</span>}
              style={{ border: 'none', outline: 'none' }}
            />
          )}
          {/* 为每个数据系列创建柱状图 */}
          {dataKeys.map((key, index) => (
            <Bar 
              key={key} 
              dataKey={key} 
              fill={`url(#${gradientIds[index % gradientIds.length]})`} 
              radius={[4, 4, 0, 0]} 
              barSize={20}
              style={{ stroke: 'none', outline: 'none' }}
              animationDuration={0}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
})

export default BarChartComponent
