from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from .config import settings
import asyncio
import aiofiles


class InfluxDBConnection:
    def __init__(self):
        self.client = None
        self.write_api = None
        self.query_api = None
    
    def connect(self):
        """连接到InfluxDB"""
        try:
            self.client = InfluxDBClient(
                url=settings.INFLUXDB_URL,
                token=settings.INFLUXDB_TOKEN,
                org=settings.INFLUXDB_ORG
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            return True
        except Exception as e:
            print(f"Failed to connect to InfluxDB: {e}")
            return False
    
    def write_data(self, measurement, tags, fields, time=None):
        """写入数据到InfluxDB"""
        if not self.write_api:
            if not self.connect():
                return False
        
        try:
            point = Point(measurement)
            for tag_key, tag_value in tags.items():
                point = point.tag(tag_key, tag_value)
            for field_key, field_value in fields.items():
                point = point.field(field_key, field_value)
            if time:
                point = point.time(time)
            
            self.write_api.write(bucket=settings.INFLUXDB_BUCKET, record=point)
            return True
        except Exception as e:
            print(f"Failed to write data to InfluxDB: {e}")
            return False
    
    def query_data(self, query):
        """从InfluxDB查询数据"""
        if not self.query_api:
            if not self.connect():
                return []
        
        try:
            result = self.query_api.query(query=query)
            return result
        except Exception as e:
            print(f"Failed to query data from InfluxDB: {e}")
            return []
    
    def close(self):
        """关闭连接"""
        if self.write_api:
            self.write_api.close()
        if self.query_api:
            self.query_api.close()
        if self.client:
            self.client.close()


# 创建全局InfluxDB连接实例
influxdb_client = InfluxDBConnection()
