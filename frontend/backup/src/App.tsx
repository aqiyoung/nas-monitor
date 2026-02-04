import React, { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, NavLink, Outlet, useNavigate } from 'react-router-dom'
import Dashboard from './pages/NewDashboard'
import System from './pages/NewSystem'
import Network from './pages/NewNetwork'
import IO from './pages/NewIO'
import Docker from './pages/NewDocker'
import Login from './pages/Login'
import Alarm from './pages/Alarm'
import UserManagement from './pages/UserManagement'

// 自定义Header组件，包含退出功能
const Header = React.memo(() => {
  const navigate = useNavigate()
  
  // 退出登录功能
  const handleLogout = () => {
    // 清除localStorage中的token和username
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    // 跳转到登录页面
    navigate('/login')
  }
  
  const username = localStorage.getItem('username')
  
  return (
    <header className="header">
      <div className="header-content">
        <svg width="60" height="60" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style={{ width: '60px', height: '60px' }}>
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
        <div>
          <h1>NAS 监控平台</h1>
          <p className="platform-description">实时监控您的NAS设备状态，包括系统资源、网络流量、磁盘IO和Docker容器</p>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <nav className="nav">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>仪表盘</NavLink>
          <NavLink to="/system" className={({ isActive }) => isActive ? 'active' : ''}>系统状态</NavLink>
          <NavLink to="/network" className={({ isActive }) => isActive ? 'active' : ''}>网络流量</NavLink>
          <NavLink to="/io" className={({ isActive }) => isActive ? 'active' : ''}>IO 状态</NavLink>
          <NavLink to="/docker" className={({ isActive }) => isActive ? 'active' : ''}>Docker 监控</NavLink>
          <NavLink to="/alarm" className={({ isActive }) => isActive ? 'active' : ''}>告警管理</NavLink>
          <NavLink to="/user" className={({ isActive }) => isActive ? 'active' : ''}>用户管理</NavLink>
        </nav>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', color: 'white', display: 'flex', justifyContent: 'center', alignItems: 'center', fontSize: '0.9rem', fontWeight: '700' }}>
              {username?.charAt(0).toUpperCase() || 'U'}
            </span>
            <span style={{ fontSize: '0.95rem', fontWeight: '600', color: '#333' }}>
              {username || '未知用户'}
            </span>
          </div>
          
          <button
            onClick={handleLogout}
            style={{ 
              backgroundColor: '#0066cc', 
              color: 'white', 
              border: 'none', 
              borderRadius: '20px', 
              padding: '8px 16px', 
              fontSize: '0.85rem', 
              fontWeight: '600', 
              cursor: 'pointer' 
            }}
          >
            退出
          </button>
        </div>
      </div>
    </header>
  )
})

// 受保护的路由组件
const ProtectedRoute = React.memo(() => {
  const token = localStorage.getItem('token')
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      navigate('/login')
    }
  }, [token, navigate])

  return token ? (
    <>
      <Header />
      <Outlet />
    </>
  ) : null
})

function App() {
  return (
    <Router>
      <Routes>
        {/* 登录路由 */}
        <Route path="/login" element={<Login />} />
        
        {/* 受保护的路由 */}
        <Route element={<ProtectedRoute />}>
          <Route path="/" element={
            <div className="container-fluid">
              <main className="container">
                <Dashboard />
              </main>
            </div>
          } />
          <Route path="/system" element={
            <div className="container-fluid">
              <main className="container">
                <System />
              </main>
            </div>
          } />
          <Route path="/network" element={
            <div className="container-fluid">
              <main className="container">
                <Network />
              </main>
            </div>
          } />
          <Route path="/io" element={
            <div className="container-fluid">
              <main className="container">
                <IO />
              </main>
            </div>
          } />
          <Route path="/docker" element={
            <div className="container-fluid">
              <main className="container">
                <Docker />
              </main>
            </div>
          } />
          <Route path="/alarm" element={
            <div className="container-fluid">
              <main className="container">
                <Alarm />
              </main>
            </div>
          } />
          <Route path="/user" element={
            <div className="container-fluid">
              <main className="container">
                <UserManagement />
              </main>
            </div>
          } />
        </Route>
      </Routes>
    </Router>
  )
}

export default App