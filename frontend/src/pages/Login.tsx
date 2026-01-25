import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../utils/api'

const Login: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  
  // 为每个背景圆生成随机动画类
  const getRandomAnimationClass = () => {
    // 随机选择1-5之间的数字
    const randomAnimation = Math.floor(Math.random() * 5) + 1
    return `animate-random-${randomAnimation}`
  }
  
  // 生成所有背景圆的随机动画类
  const circle1Animation = getRandomAnimationClass()
  const circle2Animation = getRandomAnimationClass()
  const circle3Animation = getRandomAnimationClass()
  const circle4Animation = getRandomAnimationClass()
  const circle5Animation = getRandomAnimationClass()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // 使用application/x-www-form-urlencoded格式发送登录请求
      const params = new URLSearchParams()
      params.append('username', username)
      params.append('password', password)
      
      const response = await api.post('/api/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      // 存储token和用户名到localStorage
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('username', username)
        navigate('/')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || '登录失败，请检查用户名和密码')
      console.error('Login error:', err)
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
      background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
      backgroundAttachment: 'fixed',
      padding: '40px',
      position: 'relative',
      overflow: 'hidden',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif'
    }}>
      {/* 背景装饰元素 - 带动画 */}
      <div className={`background-circle background-circle-1 ${circle1Animation}`}></div>
      <div className={`background-circle background-circle-2 ${circle2Animation}`}></div>
      <div className={`background-circle background-circle-3 ${circle3Animation}`}></div>
      <div className={`background-circle background-circle-4 ${circle4Animation}`}></div>
      <div className={`background-circle background-circle-5 ${circle5Animation}`}></div>
      
      {/* 主要内容 */}
      <div style={{
        zIndex: 1,
        display: 'grid',
        gridTemplateColumns: '1fr 420px 1fr',
        gap: '150px',
        width: '100%',
        maxWidth: '1800px',
        alignItems: 'center'
      }}>
        {/* 左侧描述 - 参差布局 */}
        <div style={{
          textAlign: 'right',
          color: '#666',
          paddingRight: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '60px',
          maxWidth: '400px'
        }}>
          <div style={{
            fontSize: '2.5rem',
            fontWeight: '800',
            color: '#333',
            letterSpacing: '-1px',
            margin: '0',
            marginRight: '-30px',
            lineHeight: '1.1'
          }}>实时监控</div>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '30px',
            animation: 'fadeInUp 0.8s ease-out 0.2s both'
          }}>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginRight: '10px',
              fontSize: '1.2rem',
              fontWeight: '600',
              color: '#444'
            }}>您的NAS设备状态</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginRight: '60px',
              fontSize: '1.1rem',
              fontWeight: '500',
              color: '#555'
            }}>系统资源使用情况</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginRight: '20px',
              fontSize: '1.15rem',
              fontWeight: '500',
              color: '#666'
            }}>网络流量实时监测</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginRight: '40px',
              fontSize: '1rem',
              fontWeight: '500',
              color: '#777'
            }}>CPU内存使用率</p>
          </div>
        </div>
        
        {/* 登录框 */}
        <div style={{
          backgroundColor: 'white',
          padding: '60px 50px',
          borderRadius: '20px',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.15)',
          textAlign: 'center',
          border: '1px solid #e0e0e0',
          transform: 'translateY(-10px)',
          position: 'relative',
          zIndex: 2,
          animation: 'fadeInUp 0.8s ease-out both'
        }}>
          {/* Logo */}
          <div style={{ marginBottom: '30px' }}>
            <svg width="120" height="120" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style={{ 
          width: '120px', 
          height: '120px',
          margin: '0 auto',
          display: 'block',
          animation: 'fadeInUp 0.6s ease-out 0.2s both'
        }}>
          <circle cx="50" cy="50" r="45" fill="url(#bgGradient)"/>
          <defs>
            <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0066cc" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#4facfe" stop-opacity="0.9"/>
            </linearGradient>
            <linearGradient id="serverGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
              <stop offset="100%" stop-color="#f0f0f0" stop-opacity="0.9"/>
            </linearGradient>
            <linearGradient id="monitorGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#4facfe"/>
              <stop offset="50%" stop-color="#00f2fe"/>
              <stop offset="100%" stop-color="#4facfe"/>
            </linearGradient>
          </defs>
          <rect x="30" y="25" width="40" height="50" rx="3" fill="url(#serverGradient)"/>
          <rect x="33" y="28" width="34" height="8" rx="2" fill="#4facfe" opacity="0.6"/>
          <rect x="33" y="40" width="34" height="2" rx="1" fill="#4facfe" opacity="0.6"/>
          <rect x="33" y="45" width="34" height="2" rx="1" fill="#4facfe" opacity="0.6"/>
          <rect x="33" y="50" width="34" height="2" rx="1" fill="#4facfe" opacity="0.6"/>
          <rect x="33" y="55" width="34" height="2" rx="1" fill="#4facfe" opacity="0.6"/>
          <rect x="33" y="60" width="34" height="8" rx="2" fill="#4facfe" opacity="0.6"/>
          <circle cx="38" cy="32" r="1.5" fill="#00ff99"/>
          <circle cx="43" cy="32" r="1.5" fill="#ff6b6b"/>
          <circle cx="48" cy="32" r="1.5" fill="#ffd93d"/>
          <rect x="25" y="15" width="50" height="8" rx="2" fill="#ffffff" opacity="0.8"/>
          <rect x="28" y="17" width="44" height="4" rx="1" fill="url(#monitorGradient)"/>
        </svg>
          </div>
          <h2 style={{
            textAlign: 'center',
            marginBottom: '40px',
            color: '#333',
            fontSize: '2.2rem',
            fontWeight: '800',
            letterSpacing: '-0.5px',
            animation: 'fadeInUp 0.6s ease-out 0.3s both'
          }}>NAS 监控平台</h2>
        
        {error && (
          <div style={{
            backgroundColor: '#fee',
            color: '#c33',
            padding: '15px',
            borderRadius: '10px',
            marginBottom: '30px',
            fontSize: '1rem',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
            border: '1px solid #f8d7da'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div style={{ marginBottom: '30px', textAlign: 'left' }}>
            <label style={{ 
              display: 'block',
              marginBottom: '10px',
              color: '#555',
              fontWeight: '600',
              fontSize: '1rem'
            }}>用户名</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ 
                width: '100%',
                padding: '15px',
                border: '2px solid #e0e0e0',
                borderRadius: '12px',
                fontSize: '16px',
                transition: 'all 0.3s ease',
                backgroundColor: '#fafafa',
                boxSizing: 'border-box'
              }}
              placeholder="请输入用户名"
            />
          </div>

          <div style={{ marginBottom: '40px', textAlign: 'left' }}>
            <label style={{ 
              display: 'block',
              marginBottom: '10px',
              color: '#555',
              fontWeight: '600',
              fontSize: '1rem'
            }}>密码</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ 
                width: '100%',
                padding: '15px',
                border: '2px solid #e0e0e0',
                borderRadius: '12px',
                fontSize: '16px',
                transition: 'all 0.3s ease',
                backgroundColor: '#fafafa',
                boxSizing: 'border-box'
              }}
              placeholder="请输入密码"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{ 
              width: '100%',
              padding: '16px',
              backgroundColor: '#0066cc',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontSize: '18px',
              fontWeight: '700',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.7 : 1,
              transition: 'all 0.3s ease',
              boxShadow: '0 6px 20px rgba(0, 102, 204, 0.4)',
              boxSizing: 'border-box'
            }}
          >
            {loading ? '登录中...' : '登录'}
          </button>
        </form>
        </div>
        
        {/* 右侧描述 - 参差布局 */}
        <div style={{
          textAlign: 'left',
          color: '#666',
          paddingLeft: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '60px',
          maxWidth: '400px'
        }}>
          <div style={{
            fontSize: '2.5rem',
            fontWeight: '800',
            color: '#333',
            letterSpacing: '-1px',
            margin: '0',
            marginLeft: '-30px',
            lineHeight: '1.1'
          }}>全面管理</div>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '30px',
            animation: 'fadeInUp 0.8s ease-out 0.4s both'
          }}>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginLeft: '50px',
              fontSize: '1.1rem',
              fontWeight: '500',
              color: '#555'
            }}>磁盘IO性能分析</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginLeft: '10px',
              fontSize: '1.2rem',
              fontWeight: '600',
              color: '#444'
            }}>Docker容器监控</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginLeft: '70px',
              fontSize: '1rem',
              fontWeight: '500',
              color: '#666'
            }}>告警通知系统</p>
            <p style={{ 
              margin: '0', 
              lineHeight: '1.5', 
              marginLeft: '30px',
              fontSize: '1.15rem',
              fontWeight: '500',
              color: '#555'
            }}>服务状态管理</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login