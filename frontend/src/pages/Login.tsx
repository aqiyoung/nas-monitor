import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../utils/api'

const Login: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      console.log('=== 开始登录 ===')
      console.log('用户名:', username)
      console.log('密码:', password)
      
      const params = new URLSearchParams()
      params.append('username', username)
      params.append('password', password)
      
      console.log('请求参数:', params.toString())
      console.log('请求URL:', '/api/auth/login')
      
      const response = await api.post('/api/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      console.log('登录成功，响应数据:', response.data)
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('username', username)
        console.log('Token已保存，准备跳转到首页')
        navigate('/')
      }
    } catch (err: any) {
      console.error('登录失败，完整错误信息:', err)
      console.error('错误响应:', err.response)
      console.error('错误状态码:', err.response?.status)
      console.error('错误详情:', err.response?.data)
      
      setError(err.response?.data?.detail || '登录失败，请检查用户名和密码')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: '#f8f9fa',
      padding: '20px',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif'
    }}>
      <div style={{
        zIndex: 1,
        display: 'flex',
        justifyContent: 'space-around',
        alignItems: 'center',
        width: '100%',
        maxWidth: '1200px',
        gap: '20px'
      }}>
        {/* 左侧功能介绍 */}
        <div style={{
          flex: 1,
          minWidth: '200px',
          maxWidth: '250px',
          textAlign: 'left',
          padding: '0 10px'
        }}>
          <div style={{
            marginBottom: '30px'
          }}>
            <h3 style={{
              color: '#667eea',
              fontSize: '1.3rem',
              fontWeight: '700',
              marginBottom: '12px'
            }}>实时监控</h3>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px'
            }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: '#667eea',
                fontSize: '1.1rem',
                flexShrink: 0
              }}>📊</div>
              <div>
                <p style={{
                  color: '#6c757d',
                  fontSize: '0.85rem',
                  lineHeight: '1.4',
                  margin: 0
                }}>实时获取系统状态、CPU使用率、内存使用情况等关键指标</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 style={{
              color: '#667eea',
              fontSize: '1.3rem',
              fontWeight: '700',
              marginBottom: '12px'
            }}>网络监控</h3>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px'
            }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: '#667eea',
                fontSize: '1.1rem',
                flexShrink: 0
              }}>🔌</div>
              <div>
                <p style={{
                  color: '#6c757d',
                  fontSize: '0.85rem',
                  lineHeight: '1.4',
                  margin: 0
                }}>监控网络流量、接口状态和连接信息</p>
              </div>
            </div>
          </div>
        </div>
        
        {/* 中间登录框 */}
        <div style={{
          backgroundColor: 'white',
          padding: '40px',
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          textAlign: 'center',
          border: '1px solid #e9ecef',
          width: '350px',
          flex: '0 0 auto'
        }}>
          <div style={{ marginBottom: '20px' }}>
            <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style={{ 
              width: '60px', 
              height: '60px',
              margin: '0 auto',
              display: 'block'
            }}>
              <circle cx="50" cy="50" r="45" fill="#667eea"/>
              <rect x="30" y="30" width="40" height="40" rx="3" fill="white"/>
              <rect x="35" y="35" width="30" height="5" rx="2" fill="#667eea"/>
              <rect x="35" y="45" width="30" height="3" rx="1" fill="#667eea"/>
              <rect x="35" y="52" width="30" height="3" rx="1" fill="#667eea"/>
              <rect x="35" y="59" width="30" height="3" rx="1" fill="#667eea"/>
            </svg>
          </div>
          <h2 style={{
            textAlign: 'center',
            marginBottom: '12px',
            color: '#667eea',
            fontSize: '1.5rem',
            fontWeight: '600'
          }}>NAS 监控平台</h2>
          <p style={{
            textAlign: 'center',
            marginBottom: '24px',
            color: '#6c757d',
            fontSize: '0.95rem'
          }}>实时监控和管理您的NAS设备状态</p>
        
        {error && (
          <div style={{
            backgroundColor: '#fff1f0',
            color: '#ff4d4f',
            padding: '12px',
            borderRadius: '8px',
            marginBottom: '20px',
            fontSize: '0.9rem',
            border: '1px solid #ffccc7'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '20px' }}>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ 
                width: '100%',
                padding: '12px 16px',
                border: '1px solid #d9d9d9',
                borderRadius: '8px',
                fontSize: '14px',
                boxSizing: 'border-box',
                outline: 'none',
                transition: 'border-color 0.3s'
              }}
              placeholder="用户名"
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ 
                width: '100%',
                padding: '12px 16px',
                border: '1px solid #d9d9d9',
                borderRadius: '8px',
                fontSize: '14px',
                boxSizing: 'border-box',
                outline: 'none',
                transition: 'border-color 0.3s'
              }}
              placeholder="密码"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{ 
              width: '100%',
              padding: '12px',
              backgroundColor: '#667eea',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '16px',
              fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'all 0.3s ease',
              boxSizing: 'border-box'
            }}
          >
            {loading ? '登录中...' : '登录'}
          </button>
        </form>
        </div>
        
        {/* 右侧功能介绍 */}
        <div style={{
          flex: 1,
          minWidth: '200px',
          maxWidth: '250px',
          textAlign: 'left',
          padding: '0 10px'
        }}>
          <div style={{
            marginBottom: '30px'
          }}>
            <h3 style={{
              color: '#667eea',
              fontSize: '1.3rem',
              fontWeight: '700',
              marginBottom: '12px'
            }}>存储监控</h3>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px'
            }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: '#667eea',
                fontSize: '1.1rem',
                flexShrink: 0
              }}>💾</div>
              <div>
                <p style={{
                  color: '#6c757d',
                  fontSize: '0.85rem',
                  lineHeight: '1.4',
                  margin: 0
                }}>监控磁盘使用情况、IO状态，及时发现存储问题</p>
              </div>
            </div>
          </div>
          
          <div>
            <h3 style={{
              color: '#667eea',
              fontSize: '1.3rem',
              fontWeight: '700',
              marginBottom: '12px'
            }}>Docker监控</h3>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '10px'
            }}>
              <div style={{
                width: '36px',
                height: '36px',
                borderRadius: '50%',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                color: '#667eea',
                fontSize: '1.1rem',
                flexShrink: 0
              }}>🐳</div>
              <div>
                <p style={{
                  color: '#6c757d',
                  fontSize: '0.85rem',
                  lineHeight: '1.4',
                  margin: 0
                }}>监控Docker容器状态、资源使用情况</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login