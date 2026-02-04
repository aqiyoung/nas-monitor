from prometheus_api_client import PrometheusConnect
from .config import settings


class PrometheusConnection:
    def __init__(self):
        self.prometheus = None
    
    def connect(self):
        """连接到Prometheus"""
        try:
            self.prometheus = PrometheusConnect(
                url=settings.PROMETHEUS_URL,
                disable_ssl=True
            )
            return True
        except Exception as e:
            print(f"Failed to connect to Prometheus: {e}")
            return False
    
    def query(self, query, time=None):
        """执行PromQL查询"""
        if not self.prometheus:
            if not self.connect():
                return []
        
        try:
            result = self.prometheus.custom_query(
                query=query,
                time=time
            )
            return result
        except Exception as e:
            print(f"Failed to query Prometheus: {e}")
            return []
    
    def query_range(self, query, start_time, end_time, step):
        """执行范围查询"""
        if not self.prometheus:
            if not self.connect():
                return []
        
        try:
            result = self.prometheus.custom_query_range(
                query=query,
                start_time=start_time,
                end_time=end_time,
                step=step
            )
            return result
        except Exception as e:
            print(f"Failed to query range from Prometheus: {e}")
            return []


# 创建全局Prometheus连接实例
prometheus_client = PrometheusConnection()
