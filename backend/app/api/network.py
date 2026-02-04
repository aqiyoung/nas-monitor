from fastapi import APIRouter, HTTPException
from app.services import network_service

router = APIRouter()

@router.get("/traffic")
async def get_network_traffic():
    """获取网络流量信息"""
    try:
        return network_service.get_network_traffic()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interfaces")
async def get_network_interfaces():
    """获取网络接口信息"""
    try:
        return network_service.get_network_interfaces()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/capture")
async def capture_network_packets(interface: str = None, duration: int = 60, output_file: str = "network_capture.log"):
    """捕获网络数据包"""
    try:
        return await network_service.capture_network_packets(interface, duration, output_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs")
async def get_network_logs(log_file: str = "network_capture.log", lines: int = 100):
    """获取网络日志"""
    try:
        return await network_service.get_network_logs(log_file, lines)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
