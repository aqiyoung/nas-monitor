import React, { useEffect, useState } from 'react'
import axios from 'axios'
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

  const fetchData = async () => {
    try {
      setLoading(true)
      const [diskRes, systemRes] = await Promise.all([
        axios.get('/api/io/disk'),
        axios.get('/api/io/system')
      ])
      
      setDiskIO(diskRes.data)
      setSystemIO(systemRes.data)
      setError(null)
    } catch (err) {
      setError('获取 IO 数据失败')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 5000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="loading">加载中...</div>
  }

  if (error) {
    return <div className="error">{error}</div>
  }

  // 准备磁盘 IO 图表数据
  const diskIOChartData = diskIO.map(disk => ({
    name: disk.disk_name,
    读取字节: disk.read_bytes / (1024 * 1024), // MB
    写入字节: disk.write_bytes / (1024 * 1024) // MB
  }))

  return (
    <div>
      <div className="grid">
        <div className="card">
          <h2>系统 IO 统计</h2>
          {systemIO && (
            <>
              <div className="metric">
                <span className="metric-label">总读取字节</span>
                <span className="metric-value">{(systemIO.total_read_bytes / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">总写入字节</span>
                <span className="metric-value">{(systemIO.total_write_bytes / (1024 * 1024)).toFixed(2)} MB</span>
              </div>
              <div className="metric">
                <span className="metric-label">总读取次数</span>
                <span className="metric-value">{systemIO.total_read_count}</span>
              </div>
              <div className="metric">
                <span className="metric-label">总写入次数</span>
                <span className="metric-value">{systemIO.total_write_count}</span>
              </div>
              <div className="metric">
                <span className="metric-label">总读取时间</span>
                <span className="metric-value">{systemIO.total_read_time} ms</span>
              </div>
              <div className="metric">
                <span className="metric-label">总写入时间</span>
                <span className="metric-value">{systemIO.total_write_time} ms</span>
              </div>
            </>
          )}
        </div>

        <div className="card">
          <h2>磁盘 IO 概览</h2>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={diskIOChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => [(typeof value === 'number' ? value.toFixed(2) : value) + ' MB', '']} />
                <Legend />
                <Bar dataKey="读取字节" fill="#3498db" />
                <Bar dataKey="写入字节" fill="#e74c3c" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>磁盘 IO 详细信息</h2>
        {diskIO.map((disk, index) => (
          <div key={index} style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
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
  )
}

export default IO