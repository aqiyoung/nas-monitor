import React, { useEffect, useState } from 'react'
import api from '../utils/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface DiskIO {
  disk_name: string
  read_bytes: number
  write_bytes: number
  read_count: number
  write_count: number
  read_time: number
  write_time: number
}

interface SystemIO {
  total_read_bytes: number
  total_write_bytes: number
  total_read_count: number
  total_write_count: number
  total_read_time: number
  total_write_time: number
}

const IO: React.FC = () => {
  const [diskIO, setDiskIO] = useState<DiskIO[]>([])
  const [systemIO, setSystemIO] = useState<SystemIO | null>(null)
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
      if (diskIO.length === 0 && !systemIO) {
        setLoading(true)
      }
      
      const [diskRes, systemRes] = await Promise.all([
        api.get('/io/disk'),
        api.get('/io/system')
      ])
      
      // 只有当数据真正变化时才更新状态，避免不必要的重新渲染
      if (dataChanged(diskIO, diskRes.data)) {
        setDiskIO(diskRes.data)
      }
      if (dataChanged(systemIO, systemRes.data)) {
        setSystemIO(systemRes.data)
      }
      
      // 只有在有错误时才设置error，否则保持null
      if (error) {
        setError(null)
      }
    } catch (err) {
      setError('获取 IO 数据失败')
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

  // 准备磁盘 IO 图表数据
  const diskIOChartData = diskIO.map(disk => ({
    name: disk.disk_name,
    读取字节: disk.read_bytes / (1024 * 1024), // MB
    写入字节: disk.write_bytes / (1024 * 1024) // MB
  }))

  return (
    <div>
      {error && <div className="error-overlay">{error}</div>}
      
      <div className="grid">
        <div className="card">
          <h2>系统 IO 统计</h2>
          <div className="metric">
            <span className="metric-label">总读取字节</span>
            <span className="metric-value">{((systemIO?.total_read_bytes || 0) / (1024 * 1024)).toFixed(2)} MB</span>
          </div>
          <div className="metric">
            <span className="metric-label">总写入字节</span>
            <span className="metric-value">{((systemIO?.total_write_bytes || 0) / (1024 * 1024)).toFixed(2)} MB</span>
          </div>
          <div className="metric">
            <span className="metric-label">总读取次数</span>
            <span className="metric-value">{systemIO?.total_read_count || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">总写入次数</span>
            <span className="metric-value">{systemIO?.total_write_count || 0}</span>
          </div>
          <div className="metric">
            <span className="metric-label">总读取时间</span>
            <span className="metric-value">{systemIO?.total_read_time || 0} ms</span>
          </div>
          <div className="metric">
            <span className="metric-label">总写入时间</span>
            <span className="metric-value">{systemIO?.total_write_time || 0} ms</span>
          </div>
        </div>

        <div className="card">
          <h2>磁盘 IO 概览</h2>
          <div className="chart-container">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart 
                    data={diskIOChartData} 
                    margin={{ top: 5, right: 30, left: 20, bottom: 5 }} 
                    animationDuration={1500} 
                    animationEasing="ease-in-out"
                    barGap={8}
                    barCategoryGap={20}
                  >
                    <defs>
                      <linearGradient id="readGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3498db" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3498db" stopOpacity={0.2}/>
                      </linearGradient>
                      <linearGradient id="writeGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#e74c3c" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#e74c3c" stopOpacity={0.2}/>
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
                        value: '数据量 (MB)', 
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
                      formatter={(value) => [(typeof value === 'number' ? value.toFixed(2) : value) + ' MB', '']}
                      labelStyle={{ fontWeight: 'bold', color: '#333' }}
                    />
                    <Legend 
                      wrapperStyle={{ paddingTop: 10 }} 
                      iconType="circle"
                      iconSize={10}
                      formatter={(value) => <span style={{ fontSize: 12, color: '#666' }}>{value}</span>}
                    />
                    <Bar 
                      dataKey="读取字节" 
                      fill="url(#readGradient)" 
                      radius={[4, 4, 0, 0]} 
                      barSize={30}
                      animationDuration={1500}
                      animationEasing="ease-in-out"
                      hoverFill="#2980b9"
                    />
                    <Bar 
                      dataKey="写入字节" 
                      fill="url(#writeGradient)" 
                      radius={[4, 4, 0, 0]} 
                      barSize={30}
                      animationDuration={1500}
                      animationEasing="ease-in-out"
                      hoverFill="#c0392b"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
        </div>
      </div>

      <div className="card">
        <h2>磁盘 IO 详细信息</h2>
        {diskIO.map((disk) => (
          <div key={disk.disk_name} style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
            <div className="metric">
              <span className="metric-label">磁盘名称</span>
              <span className="metric-value">{disk.disk_name}</span>
            </div>
            <div className="grid" style={{ gridTemplateColumns: '1fr 1fr', gap: '10px', marginTop: '10px' }}>
              <div>
                <div className="metric">
                  <span className="metric-label">读取字节</span>
                  <span className="metric-value">{(disk.read_bytes / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
                <div className="metric">
                  <span className="metric-label">写入字节</span>
                  <span className="metric-value">{(disk.write_bytes / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
                <div className="metric">
                  <span className="metric-label">读取次数</span>
                  <span className="metric-value">{disk.read_count}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">写入次数</span>
                  <span className="metric-value">{disk.write_count}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">读取时间</span>
                  <span className="metric-value">{disk.read_time} ms</span>
                </div>
                <div className="metric">
                  <span className="metric-label">写入时间</span>
                  <span className="metric-value">{disk.write_time} ms</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default IO;