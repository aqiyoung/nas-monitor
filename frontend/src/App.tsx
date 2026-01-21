
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import System from './pages/System'
import Network from './pages/Network'
import IO from './pages/IO'
import Docker from './pages/Docker'

function App() {
  return (
    <Router>
      <div className="container-fluid">
        <header className="header">
          <h1>NAS 监控平台</h1>
          <nav className="nav">
            <NavLink to="/" end className={({ isActive }) => isActive ? 'active' : ''}>仪表盘</NavLink>
            <NavLink to="/system" className={({ isActive }) => isActive ? 'active' : ''}>系统状态</NavLink>
            <NavLink to="/network" className={({ isActive }) => isActive ? 'active' : ''}>网络流量</NavLink>
            <NavLink to="/io" className={({ isActive }) => isActive ? 'active' : ''}>IO 状态</NavLink>
            <NavLink to="/docker" className={({ isActive }) => isActive ? 'active' : ''}>Docker 监控</NavLink>
          </nav>
        </header>
        
        <main className="container">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/system" element={<System />} />
            <Route path="/network" element={<Network />} />
            <Route path="/io" element={<IO />} />
            <Route path="/docker" element={<Docker />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App