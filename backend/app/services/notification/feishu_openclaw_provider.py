import aiohttp
import logging
from .notification_service import NotificationProvider

logger = logging.getLogger(__name__)

class FeishuOpenClawProvider(NotificationProvider):
    """OpenClaw飞书通知提供者"""
    
    def __init__(self, api_url: str, api_key: str, chat_id: str):
        """
        Args:
            api_url: OpenClaw服务API地址
            api_key: OpenClaw API密钥
            chat_id: 飞书聊天ID
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.chat_id = chat_id
    
    async def send_message(self, message: str, severity: str = "info") -> bool:
        """通过OpenClaw发送消息到飞书
        
        Args:
            message: 通知消息
            severity: 严重程度 (info, warning, critical)
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 根据严重程度添加前缀
            prefix = ""
            if severity == "critical":
                prefix = "🚨 严重告警: "
            elif severity == "warning":
                prefix = "⚠️ 警告: "
            elif severity == "info":
                prefix = "ℹ️ 信息: "
            
            full_message = f"{prefix}{message}"
            
            async with aiohttp.ClientSession() as session:
                # 构造OpenClaw API请求
                payload = {
                    "chat_id": self.chat_id,
                    "message": full_message,
                    "severity": severity
                }
                
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # 发送请求到OpenClaw API
                async with session.post(
                    f"{self.api_url}/api/feishu/send",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"OpenClaw API 响应错误: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"通过OpenClaw发送飞书通知时发生错误: {str(e)}")
            return False
