import logging

logger = logging.getLogger("nas-monitor.docker")

try:
    import docker
    from docker.errors import DockerException
except ImportError:
    logger.warning("Docker library not installed. Docker features will be disabled.")
    docker = None
    DockerException = Exception


def _get_client():
    """获取 Docker 客户端，失败返回 None"""
    if docker is None:
        logger.warning("Docker library not available")
        return None
    try:
        return docker.from_env()
    except DockerException as e:
        logger.error(f"Docker API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error connecting to Docker: {e}")
        return None


def get_containers():
    """获取所有容器信息"""
    client = _get_client()
    if client is None:
        return []

    result = []
    try:
        for container in client.containers.list(all=True):
            try:
                image_tag = container.image.tags[0] if container.image.tags else container.image.id
                result.append({
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": image_tag,
                    "created": container.attrs["Created"],
                    "ports": container.attrs["NetworkSettings"]["Ports"],
                    "command": container.attrs["Config"]["Cmd"],
                })
            except Exception as e:
                logger.error(f"Error processing container {container.id}: {e}")
                continue
    except (DockerException, Exception) as e:
        logger.error(f"Error listing containers: {e}")
    finally:
        client.close()

    return result


def get_docker_stats():
    """获取 Docker 容器统计信息"""
    client = _get_client()
    if client is None:
        return []

    stats = []
    try:
        for container in client.containers.list():
            try:
                container_stats = container.stats(stream=False)
                stats.append({
                    "name": container.name,
                    "cpu_usage": container_stats["cpu_stats"]["cpu_usage"]["total_usage"],
                    "memory_usage": container_stats["memory_stats"]["usage"],
                    "memory_limit": container_stats["memory_stats"]["limit"],
                    "network": container_stats["networks"],
                    "blkio": container_stats["blkio_stats"],
                })
            except Exception as e:
                logger.error(f"Error getting stats for container {container.name}: {e}")
                continue
    except (DockerException, Exception) as e:
        logger.error(f"Error getting Docker stats: {e}")
    finally:
        client.close()

    return stats


def get_images():
    """获取 Docker 镜像信息"""
    client = _get_client()
    if client is None:
        return []

    result = []
    try:
        for image in client.images.list():
            try:
                result.append({
                    "id": image.id,
                    "tags": image.tags,
                    "created": image.attrs["Created"],
                    "size": image.attrs["Size"],
                    "virtual_size": image.attrs["VirtualSize"],
                })
            except Exception as e:
                logger.error(f"Error processing image {image.id}: {e}")
                continue
    except (DockerException, Exception) as e:
        logger.error(f"Error listing images: {e}")
    finally:
        client.close()

    return result


def pull_image(image_name):
    """拉取最新的 Docker 镜像"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        image = client.images.pull(image_name)
        return {"success": True, "image_id": image.id, "tags": image.tags}
    except (DockerException, Exception) as e:
        logger.error(f"Error pulling image {image_name}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()


def delete_image(image_id):
    """删除 Docker 镜像"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        client.images.remove(image_id, force=True)
        return {"success": True, "message": "镜像删除成功"}
    except (DockerException, Exception) as e:
        logger.error(f"Error deleting image {image_id}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()


def start_container(container_id):
    """启动容器"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        client.containers.get(container_id).start()
        return {"success": True, "message": "容器启动成功"}
    except (DockerException, Exception) as e:
        logger.error(f"Error starting container {container_id}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()


def stop_container(container_id):
    """停止容器"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        client.containers.get(container_id).stop()
        return {"success": True, "message": "容器停止成功"}
    except (DockerException, Exception) as e:
        logger.error(f"Error stopping container {container_id}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()


def restart_container(container_id):
    """重启容器"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        client.containers.get(container_id).restart()
        return {"success": True, "message": "容器重启成功"}
    except (DockerException, Exception) as e:
        logger.error(f"Error restarting container {container_id}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()


def get_container_logs(container_id, tail=100):
    """获取容器日志"""
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Docker library not available"}

    try:
        container = client.containers.get(container_id)
        logs = container.logs(tail=tail).decode("utf-8")
        return {"success": True, "logs": logs}
    except (DockerException, Exception) as e:
        logger.error(f"Error getting logs for container {container_id}: {e}")
        return {"success": False, "error": str(e)}
    finally:
        client.close()
