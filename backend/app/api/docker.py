from fastapi import APIRouter, HTTPException, Body
from app.services import docker_service

router = APIRouter()

@router.get("/containers")
async def get_containers():
    """获取所有容器信息"""
    try:
        return docker_service.get_containers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_docker_stats():
    """获取 Docker 容器统计信息"""
    try:
        return docker_service.get_docker_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images")
async def get_images():
    """获取 Docker 镜像信息"""
    try:
        return docker_service.get_images()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/images/pull")
async def pull_docker_image(image_name: str = Body(..., embed=True)):
    """拉取最新的 Docker 镜像"""
    try:
        return docker_service.pull_image(image_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/images/{image_id}")
async def delete_docker_image(image_id: str):
    """删除 Docker 镜像"""
    try:
        return docker_service.delete_image(image_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
