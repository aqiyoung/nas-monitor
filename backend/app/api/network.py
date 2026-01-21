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
