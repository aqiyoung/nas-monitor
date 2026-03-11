from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Optional
import json
import asyncio
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        # 存储活动的WebSocket连接
        # key: client_id, value: WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # 存储客户端订阅的主题
        # key: client_id, value: List[str]
        self.subscriptions: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """接受WebSocket连接"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.subscriptions[client_id] = []
        logger.info(f"客户端 {client_id} 已连接")
    
    def disconnect(self, client_id: str):
        """断开WebSocket连接"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            del self.subscriptions[client_id]
            logger.info(f"客户端 {client_id} 已断开连接")
    
    async def send_personal_message(self, message: Dict, client_id: str):
        """向特定客户端发送消息"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
                return True
            except Exception as e:
                logger.error(f"向客户端 {client_id} 发送消息失败: {str(e)}")
                return False
        return False
    
    async def broadcast(self, message: Dict, topic: str = None):
        """广播消息给所有订阅了特定主题的客户端"""
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            # 如果指定了主题，只发送给订阅了该主题的客户端
            if topic and topic not in self.subscriptions.get(client_id, []):
                continue
            
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"向客户端 {client_id} 广播消息失败: {str(e)}")
                disconnected_clients.append(client_id)
        
        # 清理断开的连接
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def subscribe(self, client_id: str, topics: List[str]):
        """订阅主题"""
        if client_id in self.subscriptions:
            for topic in topics:
                if topic not in self.subscriptions[client_id]:
                    self.subscriptions[client_id].append(topic)
            logger.info(f"客户端 {client_id} 已订阅主题: {topics}")
    
    def unsubscribe(self, client_id: str, topics: List[str]):
        """取消订阅主题"""
        if client_id in self.subscriptions:
            for topic in topics:
                if topic in self.subscriptions[client_id]:
                    self.subscriptions[client_id].remove(topic)
            logger.info(f"客户端 {client_id} 已取消订阅主题: {topics}")

# 创建全局连接管理器实例
manager = ConnectionManager()

async def send_realtime_data(topic: str, data: Dict):
    """发送实时数据"""
    message = {
        "type": "realtime_data",
        "topic": topic,
        "data": data,
        "timestamp": asyncio.get_event_loop().time()
    }
    await manager.broadcast(message, topic)

async def send_alert_notification(alert_data: Dict):
    """发送告警通知"""
    message = {
        "type": "alert",
        "data": alert_data,
        "timestamp": asyncio.get_event_loop().time()
    }
    await manager.broadcast(message, "alerts")

async def send_log_notification(log_data: Dict):
    """发送日志通知"""
    message = {
        "type": "log",
        "data": log_data,
        "timestamp": asyncio.get_event_loop().time()
    }
    await manager.broadcast(message, "logs")
