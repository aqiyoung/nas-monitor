from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import logging
from app.services.notification.notification_storage import storage
from app.services.notification.telegram_provider import TelegramProvider
from app.services.notification.feishu_provider import FeishuProvider
from app.services.notification.feishu_openclaw_provider import FeishuOpenClawProvider

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
        self._load_channels()
    
    def _load_channels(self):
        """从存储加载通知渠道并创建提供者"""
        channels = storage.get_channels()
        for channel in channels:
            if channel.enabled:
                self._create_provider(channel)
    
    def _create_provider(self, channel):
        """根据渠道类型创建通知提供者"""
        try:
            if channel.type == "telegram":
                if "token" in channel.config and "chat_id" in channel.config:
                    provider = TelegramProvider(
                        token=channel.config["token"],
                        chat_id=channel.config["chat_id"]
                    )
                    self.providers[channel.id] = provider
                    logger.info(f"已创建Telegram通知提供者: {channel.name}")
            elif channel.type == "feishu":
                if "webhook_url" in channel.config:
                    provider = FeishuProvider(
                        webhook_url=channel.config["webhook_url"]
                    )
                    self.providers[channel.id] = provider
                    logger.info(f"已创建飞书通知提供者: {channel.name}")
            elif channel.type == "feishu_openclaw":
                if "api_url" in channel.config and "api_key" in channel.config and "chat_id" in channel.config:
                    provider = FeishuOpenClawProvider(
                        api_url=channel.config["api_url"],
                        api_key=channel.config["api_key"],
                        chat_id=channel.config["chat_id"]
                    )
                    self.providers[channel.id] = provider
                    logger.info(f"已创建OpenClaw飞书通知提供者: {channel.name}")
        except Exception as e:
            logger.error(f"创建通知提供者时发生错误: {str(e)}")
    
    def register_provider(self, name: str, provider: NotificationProvider):
        """注册通知提供者"""
        self.providers[name] = provider
    
    def update_provider(self, channel):
        """更新通知提供者"""
        if channel.id in self.providers:
            del self.providers[channel.id]
        if channel.enabled:
            self._create_provider(channel)
    
    def remove_provider(self, channel_id):
        """移除通知提供者"""
        if channel_id in self.providers:
            del self.providers[channel_id]
            logger.info(f"已移除通知提供者: {channel_id}")
    
    async def send_notification(self, message: str, severity: str = "info", providers: List[str] = None):
        """发送通知
        
        Args:
            message: 通知消息
            severity: 严重程度 (info, warning, critical)
            providers: 指定的通知提供者列表， None 表示使用所有注册的提供者
        """
        # 重新加载渠道，确保使用最新配置
        self._load_channels()
        
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
