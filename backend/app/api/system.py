from fastapi import APIRouter, HTTPException
from app.services import system_service

router = APIRouter()

@router.get("/status")
async def get_system_status():
    """获取系统基本状态"""
    try:
        return system_service.get_system_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cpu")
async def get_cpu_usage():
    """获取 CPU 使用情况"""
    try:
        return system_service.get_cpu_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory")
async def get_memory_usage():
    """获取内存使用情况"""
    try:
        return system_service.get_memory_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/disk")
async def get_disk_usage():
    """获取磁盘使用情况"""
    try:
        return system_service.get_disk_usage()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/disk/smart")
async def get_disk_smart_info():
    """获取磁盘S.M.A.R.T信息"""
    try:
        return system_service.get_disk_smart_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
