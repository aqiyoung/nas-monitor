import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface CPUUsage {
  total_usage: number
  per_core_usage: number[]
  cpu_count: {
    physical: number
    logical: number
  }
}

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

interface DiskUsage {
  device: string
  mountpoint: string
  fstype: string
  total: number
  used: number
  free: number
  percent: number
}

const System: React.FC = () => {
  const [cpuUsage, setCpuUsage] = useState<CPUUsage | null>(null)
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsage | null>(null)
  const [diskUsage, setDiskUsage] = useState<DiskUsage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // 数据比较函数，用于判断数据是否真正变化
  const dataChanged = (oldData: any, newData: any): boolean => {
    if (oldData === null || newData === null) {
      return oldData !== newData
    }
    
    // 对于数组，比较其长度和JSON字符串
    if (Array.isArray(oldData) && Array.isArray(newData)) {
      if (oldData.length !== newData.length) {
        return true
      }
      return JSON.stringify(oldData) !== JSON.stringify(newData)
    }
    
    // 对于对象，比较其JSON字符串
    return JSON.stringify(oldData) !== JSON.stringify(newData)
  }

  const fetchData = async () => {
    try {
      // 只有在初始加载且没有任何数据时才显示loading
      if (!cpuUsage && !memoryUsage && diskUsage.length === 0) {
        setLoading(true)
      }
      
      const [cpuRes, memoryRes, diskRes] = await Promise.all([
        api.get('/api/system/cpu'),
        api.get('/api/system/memory'),
        api.get('/api/system/disk')
      ])
      
      // 只有当数据真正变化时才更新状态，避免不必要的重新渲染
      if (dataChanged(cpuUsage, cpuRes.data)) {
        setCpuUsage(cpuRes.data)
      }
      if (dataChanged(memoryUsage, memoryRes.data)) {
        setMemoryUsage(memoryRes.data)
      }
      if (dataChanged(diskUsage, diskRes.data)) {
        setDiskUsage(diskRes.data)
      }
      
      // 只有在有错误时才设置error，否则保持null
      if (error) {
        setError(null)
      }
    } catch (err) {
      setError('获取系统数据失败')
      console.error(err)
    } finally {
      // 只有在初始加载时才设置loading为false
      if (loading) {
        setLoading(false)
      }
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  const cpuChartData = cpuUsage?.per_core_usage?.map((usage, index) => ({
    name: `核心 ${index + 1}`,
    使用率: usage
  })) || []

  const diskChartData = diskUsage.map(disk => ({
    name: disk.mountpoint,
    使用率: disk.percent
  }))

  return (
    <div>
      {loading && <div className="loading-overlay">加载中...</div>}
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <div className="card">
          <h2>CPU 详细信息</h2>
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
                animationDuration={1500} 
                animationEasing="ease-in-out"
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
                  animationDuration={1500}
                  animationEasing="ease-in-out"
                  hoverFill="#2980b9"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <h2>内存详细信息</h2>
          <div className="metric">
            <span className="metric-label">内存总量</span>
            <span className="metric-value">{((memoryUsage?.memory.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
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
            <span className="metric-label">内存使用率</span>
            <span className="metric-value">{memoryUsage?.memory.percent || 0}%</span>
          </div>
          <div className="metric">
            <span className="metric-label">Swap 总量</span>
            <span className="metric-value">{((memoryUsage?.swap.total || 0) / (1024 * 1024 * 1024)).toFixed(2)} GB</span>
          </div>
          <div className="metric">
            <span className="metric-label">Swap 使用率</span>
            <span className="metric-value">{memoryUsage?.swap.percent || 0}%</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>磁盘使用情况</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart 
              data={diskChartData} 
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }} 
              animationDuration={1500} 
              animationEasing="ease-in-out"
            >
              <defs>
                <linearGradient id="diskGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2ecc71" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#2ecc71" stopOpacity={0.2}/>
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
                formatter={(value) => [`${value}%`, '磁盘使用率']}
                labelStyle={{ fontWeight: 'bold', color: '#333' }}
              />
              <Bar 
                dataKey="使用率" 
                fill="url(#diskGradient)" 
                radius={[4, 4, 0, 0]} 
                barSize={30}
                animationDuration={1500}
                animationEasing="ease-in-out"
                hoverFill="#27ae60"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        <div style={{ marginTop: '20px' }}>
          {diskUsage.map((disk) => (
            <div key={disk.mountpoint} className="metric">
              <div>
                <div className="metric-label">{disk.mountpoint}</div>
                <div style={{ fontSize: '0.8rem', color: '#999' }}>{disk.device} ({disk.fstype})</div>
              </div>
              <div>
                <div className="metric-value">{disk.percent}%</div>
                <div style={{ fontSize: '0.8rem', color: '#999' }}>
                  {(disk.used / (1024 * 1024 * 1024)).toFixed(2)} GB / {(disk.total / (1024 * 1024 * 1024)).toFixed(2)} GB
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default System;