import aiohttp
import logging
from .notification_service import NotificationProvider

logger = logging.getLogger(__name__)

class TelegramProvider(NotificationProvider):
    """Telegram通知提供者"""
    
    def __init__(self, token: str, chat_id: str):
        """
        Args:
            token: Telegram机器人token
            chat_id: 接收消息的聊天ID
        """
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}/sendMessage"
        self.get_me_url = f"https://api.telegram.org/bot{token}/getMe"
        self.is_connected = False
    
    async def verify_token(self) -> bool:
        """验证Telegram机器人token
        
        Returns:
            bool: token是否有效
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.get_me_url) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("ok"):
                            self.is_connected = True
                            logger.info(f"Telegram机器人验证成功: {data.get('result', {}).get('username')}")
                            return True
                        else:
                            logger.error(f"Telegram机器人验证失败: {data.get('description')}")
                            return False
                    else:
                        logger.error(f"Telegram API 响应错误: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"验证Telegram token时发生错误: {str(e)}")
            return False
    
    async def send_message(self, message: str, severity: str = "info") -> bool:
        """发送消息到Telegram
        
        Args:
            message: 通知消息
            severity: 严重程度 (info, warning, critical)
        
        Returns:
            bool: 发送是否成功
        """
        try:
            # 如果还没有验证token，先验证
            if not self.is_connected:
                if not await self.verify_token():
                    return False
            
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
                payload = {
                    "chat_id": self.chat_id,
                    "text": full_message,
                    "parse_mode": "Markdown"
                }
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        return True
                    else:
                        logger.error(f"Telegram API 响应错误: {response.status}")
                        return False
        except Exception as e:
            logger.error(f"发送Telegram通知时发生错误: {str(e)}")
            return False
