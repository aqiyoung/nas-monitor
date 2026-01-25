import { useState, useEffect, useCallback, useMemo } from 'react'
import api from '../utils/api'

// 数据比较函数，用于判断数据是否真正变化
const dataChanged = (oldData: any, newData: any): boolean => {
  if (oldData === null || newData === null) {
    return oldData !== newData
  }
  
  // 对于对象，比较其JSON字符串
  return JSON.stringify(oldData) !== JSON.stringify(newData)
}

interface UseDataFetchingOptions<T> {
  initialData?: T
  interval?: number
  onSuccess?: (data: T) => void
  onError?: (error: any) => void
}

// 通用数据获取钩子
export const useDataFetching = <T>(
  endpoint: string,
  options: UseDataFetchingOptions<T> = {}
) => {
  const { 
    initialData = null as unknown as T,
    interval = 5000,
    onSuccess,
    onError
  } = options

  const [data, setData] = useState<T>(initialData)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const response = await api.get<T>(endpoint)
      
      // 只有当数据真正变化时才更新状态，避免不必要的重新渲染
      if (dataChanged(data, response.data)) {
        setData(response.data)
        onSuccess?.(response.data)
      }
      
      if (error) {
        setError(null)
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '获取数据失败，请检查后端服务是否正常运行'
      setError(errorMessage)
      onError?.(err)
      console.error(`Error fetching data from ${endpoint}:`, err)
    } finally {
      // 只有在初始加载时才设置loading为false
      if (loading) {
        setLoading(false)
      }
    }
  }, [data, endpoint, error, loading, onSuccess, onError])

  useEffect(() => {
    fetchData()
    const intervalId = setInterval(fetchData, interval)
    return () => clearInterval(intervalId)
  }, [fetchData, interval])

  return { data, loading, error, refetch: fetchData }
}

// 批量数据获取钩子
export const useBatchDataFetching = <T = any>(
  endpoints: Record<string, string>,
  interval: number = 5000
) => {
  const [data, setData] = useState<T>({} as T)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const requests = Object.entries(endpoints).map(([key, endpoint]) => 
        api.get(endpoint).then(response => ({ key, data: response.data }))
      )

      const results = await Promise.all(requests)
      const newData: any = {}
      let hasChanges = false

      results.forEach(({ key, data: responseData }) => {
        const oldData = (data as any)[key]
        if (dataChanged(oldData, responseData)) {
          newData[key] = responseData
          hasChanges = true
        }
      })

      if (hasChanges) {
        setData(prevData => ({ ...prevData, ...newData } as T))
      }

      if (error) {
        setError(null)
      }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || '获取数据失败，请检查后端服务是否正常运行'
      setError(errorMessage)
      console.error('Error fetching batch data:', err)
    } finally {
      if (loading) {
        setLoading(false)
      }
    }
  }, [data, endpoints, error, loading])

  useEffect(() => {
    fetchData()
    const intervalId = setInterval(fetchData, interval)
    return () => clearInterval(intervalId)
  }, [fetchData, interval])

  return { data, loading, error, refetch: fetchData }
}
