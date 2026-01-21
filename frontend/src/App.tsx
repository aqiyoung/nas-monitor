
import { BrowserRouter as Router, Routes, Route, NavLink, Outlet, useNavigate } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import System from './pages/System'
import Network from './pages/Network'
import IO from './pages/IO'
import Docker from './pages/Docker'
import Login from './pages/Login'
import Alarm from './pages/Alarm'
import UserManagement from './pages/UserManagement'
import { useEffect } from 'react'

// 受保护的路由组件
const ProtectedRoute = () => {
  const token = localStorage.getItem('token')
  const navigate = useNavigate()

  useEffect(() => {
    if (!token) {
      navigate('/login')
    }
  }, [token, navigate])

  return token ? <Outlet /> : null
}

function App() {

  return (
    <Router>
      <Routes>
        {/* 登录路由 */}
        <Route path="/login" element={<Login />} />
        
        {/* 受保护的路由 */}
        <Route element={<ProtectedRoute />}>
          <Route path="/*" element={(
            <div className="container-fluid">
              <header className="header">
                <h1>NAS 监控平台</h1>
                <nav className="nav">
                  <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>仪表盘</NavLink>
                  <NavLink to="/system" className={({ isActive }) => isActive ? 'active' : ''}>系统状态</NavLink>
                  <NavLink to="/network" className={({ isActive }) => isActive ? 'active' : ''}>网络流量</NavLink>
                  <NavLink to="/io" className={({ isActive }) => isActive ? 'active' : ''}>IO 状态</NavLink>
                  <NavLink to="/docker" className={({ isActive }) => isActive ? 'active' : ''}>Docker 监控</NavLink>
                  <NavLink to="/alarm" className={({ isActive }) => isActive ? 'active' : ''}>告警管理</NavLink>
                  <NavLink to="/user" className={({ isActive }) => isActive ? 'active' : ''}>用户管理</NavLink>
                </nav>
              </header>
              
              <main className="container">
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/system" element={<System />} />
                    <Route path="/network" element={<Network />} />
                    <Route path="/io" element={<IO />} />
                    <Route path="/docker" element={<Docker />} />
                    <Route path="/alarm" element={<Alarm />} />
                    <Route path="/user" element={<UserManagement />} />
                  </Routes>
              </main>
            </div>
          )} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App