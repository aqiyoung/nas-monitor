from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationProvider(ABC):
    """通知提供者基类"""
    
    @abstractmethod
    async def send_message(self, message: str, severity: str = "info") -> bool:
        """发送消息"""
        pass

class NotificationService:
    """通知服务"""
    
    def __init__(self):
        self.providers: Dict[str, NotificationProvider] = {}
    
    def register_provider(self, name: str, provider: NotificationProvider):
        """注册通知提供者"""
        self.providers[name] = provider
    
    async def send_notification(self, message: str, severity: str = "info", providers: List[str] = None):
        """发送通知
        
        Args:
            message: 通知消息
            severity: 严重程度 (info, warning, critical)
            providers: 指定的通知提供者列表， None 表示使用所有注册的提供者
        """
        if not providers:
            providers = list(self.providers.keys())
        
        results = {}
        for provider_name in providers:
            if provider_name in self.providers:
                try:
                    success = await self.providers[provider_name].send_message(message, severity)
                    results[provider_name] = success
                    if success:
                        logger.info(f"通知已发送到 {provider_name}")
                    else:
                        logger.warning(f"通知发送到 {provider_name} 失败")
                except Exception as e:
                    logger.error(f"发送通知到 {provider_name} 时发生错误: {str(e)}")
                    results[provider_name] = False
            else:
                logger.warning(f"通知提供者 {provider_name} 未注册")
                results[provider_name] = False
        
        return results

# 创建全局通知服务实例
notification_service = NotificationService()
