import React from 'react'

// 用于调试组件渲染的高阶组件
export const withRenderDebug = <P extends object>(Component: React.ComponentType<P>, componentName: string) => {
  return React.memo((props: P) => {
    console.log(`${componentName} rendered at`, new Date().toISOString())
    return <Component {...props} />
  })
}
