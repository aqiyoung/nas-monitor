import React from 'react'

interface DashboardLayoutProps {
  children: React.ReactNode
}

// Dashboard页面的容器组件，只负责布局，不依赖数据状态
const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  return (
    <div>
      <div className="grid">
        {/* 系统状态卡片容器 */}
        <div className="card">
          <h2>系统状态</h2>
          {/* 系统状态数据将通过children传入 */}
          {children}
        </div>
      </div>
    </div>
  )
}

export default React.memo(DashboardLayout)