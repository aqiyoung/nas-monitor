import docker

def get_containers():
    """获取所有容器信息"""
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        result = []
        
        for container in containers:
            result.append({
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else container.image.id,
                "created": container.attrs["Created"],
                "ports": container.attrs["NetworkSettings"]["Ports"],
                "command": container.attrs["Config"]["Cmd"]
            })
        
        client.close()
        return result
    except docker.errors.DockerException as e:
        return {"error": str(e)}

def get_docker_stats():
    """获取 Docker 容器统计信息"""
    try:
        client = docker.from_env()
        containers = client.containers.list()
        stats = []
        
        for container in containers:
            container_stats = container.stats(stream=False)
            stats.append({
                "name": container.name,
                "cpu_usage": container_stats["cpu_stats"]["cpu_usage"]["total_usage"],
                "memory_usage": container_stats["memory_stats"]["usage"],
                "memory_limit": container_stats["memory_stats"]["limit"],
                "network": container_stats["networks"],
                "blkio": container_stats["blkio_stats"]
            })
        
        client.close()
        return stats
    except docker.errors.DockerException as e:
        return {"error": str(e)}

def get_images():
    """获取 Docker 镜像信息"""
    try:
        client = docker.from_env()
        images = client.images.list()
        result = []
        
        for image in images:
            result.append({
                "id": image.id,
                "tags": image.tags,
                "created": image.attrs["Created"],
                "size": image.attrs["Size"],
                "virtual_size": image.attrs["VirtualSize"]
            })
        
        client.close()
        return result
    except docker.errors.DockerException as e:
        return {"error": str(e)}
