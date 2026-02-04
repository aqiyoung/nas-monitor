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

@router.post("/containers/{container_id}/start")
async def start_container(container_id: str):
    """启动容器"""
    try:
        return docker_service.start_container(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/stop")
async def stop_container(container_id: str):
    """停止容器"""
    try:
        return docker_service.stop_container(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/containers/{container_id}/restart")
async def restart_container(container_id: str):
    """重启容器"""
    try:
        return docker_service.restart_container(container_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/containers/{container_id}/logs")
async def get_container_logs(container_id: str, tail: int = 100):
    """获取容器日志"""
    try:
        return docker_service.get_container_logs(container_id, tail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
