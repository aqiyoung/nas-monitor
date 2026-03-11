import aiohttp
import logging
from .notification_service import NotificationProvider

logger = logging.getLogger(__name__)

class FeishuProvider(NotificationProvider):
    """飞书通知提供者"""
    
    def __init__(self, webhook_url: str):
        """
        Args:
            webhook_url: 飞书机器人webhook URL
        """
        self.webhook_url = webhook_url
    
    async def send_message(self, message: str, severity: str = "info") -> bool:
        """发送消息到飞书
        
        Args:
            message: 通知消息
            severity: 严重程度 (info, warning, critical)
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 根据严重程度添加前缀和颜色
            prefix = ""
            color = "default"
            if severity == "critical":
                prefix = "🚨 严重告警: "
                color = "red"
            elif severity == "warning":
                prefix = "⚠️ 警告: "
                color = "orange"
            elif severity == "info":
                prefix = "ℹ️ 信息: "
                color = "blue"
            
            full_message = f"{prefix}{message}"
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "msg_type": "text",
                    "content": {
                        "text": full_message
                    }
                }
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"飞书 API 响应错误: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"发送飞书通知时发生错误: {str(e)}")
            return False
