import asyncio
import aiohttp
import logging
import json
import time
from typing import Dict, Optional, Callable

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FeishuLongPolling:
    """飞书机器人长链接实现"""
    
    def __init__(self, app_id: str, app_secret: str):
        """
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire_time = 0
        self.lark_host = "https://open.feishu.cn"
        self.message_handler: Optional[Callable] = None
        self.running = False
    
    async def get_access_token(self) -> Optional[str]:
        """获取访问令牌"""
        try:
            # 检查令牌是否有效
            if self.access_token and self.token_expire_time > time.time():
                return self.access_token
            
            # 请求新令牌
            url = f"{self.lark_host}/open-apis/auth/v3/tenant_access_token/internal/"
            payload = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 0:
                            self.access_token = data.get("tenant_access_token")
                            self.token_expire_time = time.time() + data.get("expire", 3600)
                            logger.info("获取飞书访问令牌成功")
                            return self.access_token
                        else:
                            logger.error(f"获取飞书访问令牌失败: {data.get('msg')}")
                    else:
                        logger.error(f"飞书API响应错误: {response.status}")
        except Exception as e:
            logger.error(f"获取飞书访问令牌时发生错误: {str(e)}")
        return None
    
    async def get_event_list(self) -> Optional[Dict]:
        """获取事件列表"""
        access_token = await self.get_access_token()
        if not access_token:
            return None
        
        try:
            url = f"{self.lark_host}/open-apis/event/v1/events"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("code") == 0:
                            return data
                        else:
                            logger.error(f"获取事件列表失败: {data.get('msg')}")
                    else:
                        logger.error(f"飞书API响应错误: {response.status}")
        except Exception as e:
            logger.error(f"获取事件列表时发生错误: {str(e)}")
        return None
    
    async def process_event(self, event: Dict):
        """处理事件"""
        try:
            event_type = event.get("header", {}).get("event_type")
            event_body = event.get("event", {})
            
            logger.info(f"收到飞书事件: {event_type}")
            
            # 调用消息处理器
            if self.message_handler:
                await self.message_handler(event_type, event_body)
            else:
                logger.warning("未设置消息处理器")
        except Exception as e:
            logger.error(f"处理事件时发生错误: {str(e)}")
    
    async def start(self, message_handler: Callable):
        """启动长链接
        
        Args:
            message_handler: 消息处理器函数，接收(event_type, event_body)参数
        """
        self.message_handler = message_handler
        self.running = True
        
        logger.info("启动飞书长链接服务")
        
        while self.running:
            try:
                # 获取事件列表
                result = await self.get_event_list()
                if result:
                    events = result.get("data", {}).get("items", [])
                    for event in events:
                        await self.process_event(event)
                
                # 等待一段时间后再次轮询
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"长链接服务出错: {str(e)}")
                await asyncio.sleep(10)
    
    def stop(self):
        """停止长链接"""
        self.running = False
        logger.info("停止飞书长链接服务")

# 示例使用
async def example_message_handler(event_type: str, event_body: Dict):
    """示例消息处理器"""
    print(f"处理事件类型: {event_type}")
    print(f"事件内容: {json.dumps(event_body, indent=2, ensure_ascii=False)}")

async def main():
    """主函数"""
    # 替换为实际的app_id和app_secret
    feishu = FeishuLongPolling(
        app_id="your_app_id",
        app_secret="your_app_secret"
    )
    
    # 启动长链接
    await feishu.start(example_message_handler)

if __name__ == "__main__":
    import time
    asyncio.run(main())
