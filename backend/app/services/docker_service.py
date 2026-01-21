import docker

def get_containers():
    """获取所有容器信息"""
    result = []
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        
        for container in containers:
            try:
                # 获取镜像标签，处理空列表情况
                image_tag = container.image.tags[0] if container.image.tags else container.image.id
                
                result.append({
                    "id": container.id,
                    "name": container.name,
                    "status": container.status,
                    "image": image_tag,
                    "created": container.attrs["Created"],
                    "ports": container.attrs["NetworkSettings"]["Ports"],
                    "command": container.attrs["Config"]["Cmd"]
                })
            except Exception as e:
                # 跳过有问题的容器，继续处理其他容器
                continue
        
        client.close()
    except docker.errors.DockerException as e:
        # 记录错误，但返回空列表而不是错误对象，以便前端能正常处理
        print(f"Docker API error: {e}")
    except Exception as e:
        # 捕获其他所有异常，确保函数始终返回列表
        print(f"Unexpected error in get_containers: {e}")
    
    return result

def get_docker_stats():
    """获取 Docker 容器统计信息"""
    stats = []
    try:
        client = docker.from_env()
        containers = client.containers.list()
        
        for container in containers:
            try:
                container_stats = container.stats(stream=False)
                stats.append({
                    "name": container.name,
                    "cpu_usage": container_stats["cpu_stats"]["cpu_usage"]["total_usage"],
                    "memory_usage": container_stats["memory_stats"]["usage"],
                    "memory_limit": container_stats["memory_stats"]["limit"],
                    "network": container_stats["networks"],
                    "blkio": container_stats["blkio_stats"]
                })
            except Exception as e:
                # 跳过有问题的容器，继续处理其他容器
                continue
        
        client.close()
    except docker.errors.DockerException as e:
        # 记录错误，但返回空列表而不是错误对象
        print(f"Docker API error: {e}")
    except Exception as e:
        # 捕获其他所有异常，确保函数始终返回列表
        print(f"Unexpected error in get_docker_stats: {e}")
    
    return stats

def get_images():
    """获取 Docker 镜像信息"""
    result = []
    try:
        client = docker.from_env()
        images = client.images.list()
        
        for image in images:
            try:
                result.append({
                    "id": image.id,
                    "tags": image.tags,
                    "created": image.attrs["Created"],
                    "size": image.attrs["Size"],
                    "virtual_size": image.attrs["VirtualSize"]
                })
            except Exception as e:
                # 跳过有问题的镜像，继续处理其他镜像
                continue
        
        client.close()
    except docker.errors.DockerException as e:
        # 记录错误，但返回空列表而不是错误对象
        print(f"Docker API error: {e}")
    except Exception as e:
        # 捕获其他所有异常，确保函数始终返回列表
        print(f"Unexpected error in get_images: {e}")
    
    return result
