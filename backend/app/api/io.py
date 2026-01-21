from fastapi import APIRouter, HTTPException
from app.services import io_service

router = APIRouter()

@router.get("/disk")
async def get_disk_io():
    """获取磁盘 IO 信息"""
    try:
        return io_service.get_disk_io()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system")
async def get_system_io():
    """获取系统 IO 统计信息"""
    try:
        return io_service.get_system_io()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
