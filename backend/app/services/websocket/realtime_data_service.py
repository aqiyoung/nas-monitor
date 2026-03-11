import asyncio
import logging
from app.services.system_service import get_cpu_usage, get_memory_usage, get_disk_usage
from app.services.network_service import get_network_stats
from app.services.io_service import get_io_stats
from app.services.docker_service import get_containers
from app.services.websocket.websocket_service import send_realtime_data

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_system_data():
    """发送系统数据"""
    try:
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        
        system_data = {
            "cpu": cpu_usage,
            "memory": memory_usage,
            "disk": disk_usage
        }
        
        await send_realtime_data("system", system_data)
    except Exception as e:
        logger.error(f"发送系统数据失败: {str(e)}")

async def send_network_data():
    """发送网络数据"""
    try:
        network_stats = get_network_stats()
        await send_realtime_data("network", network_stats)
    except Exception as e:
        logger.error(f"发送网络数据失败: {str(e)}")

async def send_io_data():
    """发送IO数据"""
    try:
        io_stats = get_io_stats()
        await send_realtime_data("io", io_stats)
    except Exception as e:
        logger.error(f"发送IO数据失败: {str(e)}")

async def send_docker_data():
    """发送Docker数据"""
    try:
        containers = get_containers()
        await send_realtime_data("docker", {"containers": containers})
    except Exception as e:
        logger.error(f"发送Docker数据失败: {str(e)}")

async def realtime_data_task():
    """实时数据推送任务"""
    logger.info("启动实时数据推送任务")
    
    while True:
        try:
            # 发送系统数据
            await send_system_data()
            # 发送网络数据
            await send_network_data()
            # 发送IO数据
            await send_io_data()
            # 发送Docker数据
            await send_docker_data()
        except Exception as e:
            logger.error(f"实时数据推送任务失败: {str(e)}")
        
        # 等待1秒后再次发送
        await asyncio.sleep(1)

# 启动实时数据推送任务
def start_realtime_data_task():
    """启动实时数据推送任务"""
    loop = asyncio.get_event_loop()
    loop.create_task(realtime_data_task())
    logger.info("实时数据推送任务已启动")
