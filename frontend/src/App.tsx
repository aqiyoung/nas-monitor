
import { BrowserRouter as Router, Routes, Route, NavLink, Outlet, useNavigate } from 'react-router-dom'
import Dashboard from './pages/NewDashboard'
import System from './pages/NewSystem'
import Network from './pages/NewNetwork'
import IO from './pages/NewIO'
import Docker from './pages/NewDocker'
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
                  <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}><span>仪表盘</span></NavLink>
                  <NavLink to="/system" className={({ isActive }) => isActive ? 'active' : ''}><span>系统状态</span></NavLink>
                  <NavLink to="/network" className={({ isActive }) => isActive ? 'active' : ''}><span>网络流量</span></NavLink>
                  <NavLink to="/io" className={({ isActive }) => isActive ? 'active' : ''}><span>IO 状态</span></NavLink>
                  <NavLink to="/docker" className={({ isActive }) => isActive ? 'active' : ''}><span>Docker 监控</span></NavLink>
                  <NavLink to="/alarm" className={({ isActive }) => isActive ? 'active' : ''}><span>告警管理</span></NavLink>
                  <NavLink to="/user" className={({ isActive }) => isActive ? 'active' : ''}><span>用户管理</span></NavLink>
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