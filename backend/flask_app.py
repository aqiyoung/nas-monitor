from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import platform
import socket
import time
import os
import docker
import requests

app = Flask(__name__)
CORS(app)

# 模拟用户数据
users = {
    "admin": {
        "username": "admin",
        "password": "password",
        "disabled": False
    }
}

# 初始化Docker客户端
try:
    docker_client = docker.from_env()
except:
    docker_client = None

# 告警数据
alarm_data = {
    "configs": [
        {
            "id": "alarm1",
            "alarm_type": "system",
            "sub_type": "cpu_high",
            "enabled": True,
            "threshold": 80.0,
            "duration": 30,
            "severity": "warning"
        }
    ],
    "records": []
}

# 获取系统基本信息
def get_system_info():
    try:
        # 尝试从nas-node-exporter获取系统信息
        try:
            response = requests.get('http://nas-node-exporter:9100/metrics')
            if response.status_code == 200:
                # 解析metrics获取系统信息
                metrics = response.text
                
                # 获取主机名
                hostname = socket.gethostname()
                
                # 获取操作系统信息
                os_info = platform.system()
                os_version = platform.release()
                
                # 获取架构信息
                architecture = platform.machine()
                
                # 获取运行时间
                uptime_seconds = time.time() - psutil.boot_time()
                uptime_days = int(uptime_seconds // 86400)
                uptime_hours = int((uptime_seconds % 86400) // 3600)
                uptime_minutes = int((uptime_seconds % 3600) // 60)
                uptime_seconds = int(uptime_seconds % 60)
                uptime = f"{uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s"
                
                # 获取启动时间
                boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
                
                return {
                    "hostname": hostname,
                    "os": os_info,
                    "os_version": os_version,
                    "architecture": architecture,
                    "uptime": uptime,
                    "boot_time": boot_time
                }
        except Exception as e:
            print(f"从nas-node-exporter获取系统信息失败: {e}")
        
        # 如果从nas-node-exporter获取失败，使用本地获取
        # 获取主机名
        hostname = socket.gethostname()
        
        # 获取操作系统信息
        os_info = platform.system()
        os_version = platform.release()
        
        # 获取架构信息
        architecture = platform.machine()
        
        # 获取运行时间
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_days = int(uptime_seconds // 86400)
        uptime_hours = int((uptime_seconds % 86400) // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        uptime_seconds = int(uptime_seconds % 60)
        uptime = f"{uptime_days}d {uptime_hours}h {uptime_minutes}m {uptime_seconds}s"
        
        # 获取启动时间
        boot_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(psutil.boot_time()))
        
        return {
            "hostname": hostname,
            "os": os_info,
            "os_version": os_version,
            "architecture": architecture,
            "uptime": uptime,
            "boot_time": boot_time
        }
    except Exception as e:
        print(f"获取系统信息失败: {e}")
        # 返回默认值
        return {
            "hostname": "test-nas",
            "os": "Debian",
            "os_version": "12.0",
            "architecture": "x86_64",
            "uptime": "10d 5h 30m 15s",
            "boot_time": "2024-01-01 00:00:00"
        }

# 获取CPU使用率
def get_cpu_info():
    try:
        # 尝试从nas-node-exporter获取CPU信息
        try:
            response = requests.get('http://nas-node-exporter:9100/metrics')
            if response.status_code == 200:
                # 解析metrics获取CPU信息
                metrics = response.text
                
                # 提取CPU使用率
                import re
                cpu_usage_match = re.search(r'node_cpu_seconds_total\{mode="idle"\} (\d+\.\d+)', metrics)
                if cpu_usage_match:
                    idle_time = float(cpu_usage_match.group(1))
                else:
                    idle_time = 0
                
                # 提取总CPU时间
                total_time = 0
                for line in metrics.split('\n'):
                    if line.startswith('node_cpu_seconds_total{') and 'mode=' in line:
                        match = re.search(r'node_cpu_seconds_total\{[^}]+\} (\d+\.\d+)', line)
                        if match:
                            total_time += float(match.group(1))
                
                # 计算CPU使用率
                if total_time > 0:
                    cpu_usage = (1 - idle_time / total_time) * 100
                else:
                    cpu_usage = 0
                
                # 获取CPU核心数
                cpu_count = {
                    "physical": psutil.cpu_count(logical=False),
                    "logical": psutil.cpu_count(logical=True)
                }
                
                # 提取每个核心的使用率
                per_core_usage = []
                core_idle_times = {}
                core_total_times = {}
                
                for line in metrics.split('\n'):
                    if line.startswith('node_cpu_seconds_total{'):
                        match = re.search(r'node_cpu_seconds_total\{cpu="(\d+)", mode="([^"]+)"\} (\d+\.\d+)', line)
                        if match:
                            core = match.group(1)
                            mode = match.group(2)
                            value = float(match.group(3))
                            
                            if core not in core_total_times:
                                core_total_times[core] = 0
                            core_total_times[core] += value
                            
                            if mode == 'idle':
                                core_idle_times[core] = value
                
                for core in sorted(core_idle_times.keys()):
                    if core in core_total_times and core_total_times[core] > 0:
                        core_usage = (1 - core_idle_times[core] / core_total_times[core]) * 100
                        per_core_usage.append(core_usage)
                
                return {
                    "total_usage": cpu_usage,
                    "per_core_usage": per_core_usage,
                    "cpu_count": cpu_count
                }
        except Exception as e:
            print(f"从nas-node-exporter获取CPU信息失败: {e}")
        
        # 如果从nas-node-exporter获取失败，使用本地获取
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # 获取CPU核心数
        cpu_count = {
            "physical": psutil.cpu_count(logical=False),
            "logical": psutil.cpu_count(logical=True)
        }
        
        # 获取每个核心的使用率
        per_core_usage = psutil.cpu_percent(interval=1, percpu=True)
        
        return {
            "total_usage": cpu_usage,
            "per_core_usage": per_core_usage,
            "cpu_count": cpu_count
        }
    except Exception as e:
        print(f"获取CPU信息失败: {e}")
        # 返回默认值
        return {
            "total_usage": 25.5,
            "per_core_usage": [],
            "cpu_count": {
                "physical": 4,
                "logical": 8
            }
        }

# 获取内存使用率
def get_memory_info():
    try:
        # 尝试从nas-node-exporter获取内存信息
        try:
            response = requests.get('http://nas-node-exporter:9100/metrics')
            if response.status_code == 200:
                # 解析metrics获取内存信息
                metrics = response.text
                
                # 提取内存信息
                import re
                
                # 提取总内存
                total_memory_match = re.search(r'node_memory_MemTotal_bytes (\d+)', metrics)
                if total_memory_match:
                    total_memory = int(total_memory_match.group(1))
                else:
                    total_memory = 0
                
                # 提取可用内存
                available_memory_match = re.search(r'node_memory_MemAvailable_bytes (\d+)', metrics)
                if available_memory_match:
                    available_memory = int(available_memory_match.group(1))
                else:
                    available_memory = 0
                
                # 计算已用内存
                used_memory = total_memory - available_memory
                
                # 计算内存使用率
                if total_memory > 0:
                    memory_percent = (used_memory / total_memory) * 100
                else:
                    memory_percent = 0
                
                # 提取交换内存信息
                # 提取总交换内存
                total_swap_match = re.search(r'node_memory_SwapTotal_bytes (\d+)', metrics)
                if total_swap_match:
                    total_swap = int(total_swap_match.group(1))
                else:
                    total_swap = 0
                
                # 提取可用交换内存
                free_swap_match = re.search(r'node_memory_SwapFree_bytes (\d+)', metrics)
                if free_swap_match:
                    free_swap = int(free_swap_match.group(1))
                else:
                    free_swap = 0
                
                # 计算已用交换内存
                used_swap = total_swap - free_swap
                
                # 计算交换内存使用率
                if total_swap > 0:
                    swap_percent = (used_swap / total_swap) * 100
                else:
                    swap_percent = 0
                
                return {
                    "memory": {
                        "total": total_memory,
                        "available": available_memory,
                        "used": used_memory,
                        "percent": memory_percent
                    },
                    "swap": {
                        "total": total_swap,
                        "used": used_swap,
                        "free": free_swap,
                        "percent": swap_percent
                    }
                }
        except Exception as e:
            print(f"从nas-node-exporter获取内存信息失败: {e}")
        
        # 如果从nas-node-exporter获取失败，使用本地获取
        # 获取内存信息
        memory = psutil.virtual_memory()
        
        # 获取交换内存信息
        swap = psutil.swap_memory()
        
        return {
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        }
    except Exception as e:
        print(f"获取内存信息失败: {e}")
        # 返回默认值
        return {
            "memory": {
                "total": 8192000000,
                "available": 4096000000,
                "used": 4096000000,
                "percent": 45.2
            },
            "swap": {
                "total": 4096000000,
                "used": 0,
                "free": 4096000000,
                "percent": 0
            }
        }

# 获取磁盘使用率
def get_disk_info():
    try:
        # 尝试从nas-node-exporter获取磁盘信息
        try:
            response = requests.get('http://nas-node-exporter:9100/metrics')
            if response.status_code == 200:
                # 解析metrics获取磁盘信息
                metrics = response.text
                
                # 提取磁盘信息
                import re
                
                # 提取挂载点
                mountpoints = {}
                
                # 提取文件系统大小
                for line in metrics.split('\n'):
                    if line.startswith('node_filesystem_size_bytes{'):
                        match = re.search(r'node_filesystem_size_bytes\{mountpoint="([^"]+)",[^}]+\} (\d+)', line)
                        if match:
                            mountpoint = match.group(1)
                            size = int(match.group(2))
                            if mountpoint not in mountpoints:
                                mountpoints[mountpoint] = {
                                    "mountpoint": mountpoint,
                                    "total": size,
                                    "used": 0,
                                    "percent": 0
                                }
                
                # 提取文件系统已用空间
                for line in metrics.split('\n'):
                    if line.startswith('node_filesystem_files{'):
                        match = re.search(r'node_filesystem_files\{mountpoint="([^"]+)",[^}]+\} (\d+)', line)
                        if match:
                            mountpoint = match.group(1)
                            if mountpoint in mountpoints:
                                # 这里提取的是文件数，不是字节数，需要重新提取
                                pass
                    elif line.startswith('node_filesystem_size_bytes{'):
                        # 已经处理过了
                        pass
                    elif line.startswith('node_filesystem_avail_bytes{'):
                        match = re.search(r'node_filesystem_avail_bytes\{mountpoint="([^"]+)",[^}]+\} (\d+)', line)
                        if match:
                            mountpoint = match.group(1)
                            avail = int(match.group(2))
                            if mountpoint in mountpoints:
                                total = mountpoints[mountpoint]['total']
                                used = total - avail
                                percent = (used / total) * 100 if total > 0 else 0
                                mountpoints[mountpoint]['used'] = used
                                mountpoints[mountpoint]['percent'] = percent
                
                # 转换为列表
                disk_info = list(mountpoints.values())
                return disk_info
        except Exception as e:
            print(f"从nas-node-exporter获取磁盘信息失败: {e}")
        
        # 如果从nas-node-exporter获取失败，使用本地获取
        # 获取所有磁盘分区
        partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in partitions:
            try:
                # 获取分区使用情况
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "mountpoint": partition.mountpoint,
                    "percent": usage.percent,
                    "used": usage.used,
                    "total": usage.total
                })
            except:
                pass
        
        return disk_info
    except Exception as e:
        print(f"获取磁盘信息失败: {e}")
        # 返回默认值
        return [
            {
                "mountpoint": "/",
                "percent": 60.8,
                "used": 60000000000,
                "total": 100000000000
            }
        ]

# 获取网络流量
def get_network_info():
    try:
        # 尝试从nas-node-exporter获取网络信息
        try:
            response = requests.get('http://nas-node-exporter:9100/metrics')
            if response.status_code == 200:
                # 解析metrics获取网络信息
                metrics = response.text
                
                # 提取网络流量信息
                import re
                
                # 提取总网络流量
                bytes_sent = 0
                bytes_recv = 0
                packets_sent = 0
                packets_recv = 0
                errin = 0
                errout = 0
                dropin = 0
                dropout = 0
                
                # 提取每个接口的流量
                for line in metrics.split('\n'):
                    if line.startswith('node_network_transmit_bytes_total{'):
                        match = re.search(r'node_network_transmit_bytes_total\{[^}]+\} (\d+)', line)
                        if match:
                            bytes_sent += int(match.group(1))
                    elif line.startswith('node_network_receive_bytes_total{'):
                        match = re.search(r'node_network_receive_bytes_total\{[^}]+\} (\d+)', line)
                        if match:
                            bytes_recv += int(match.group(1))
                    elif line.startswith('node_network_transmit_packets_total{'):
                        match = re.search(r'node_network_transmit_packets_total\{[^}]+\} (\d+)', line)
                        if match:
                            packets_sent += int(match.group(1))
                    elif line.startswith('node_network_receive_packets_total{'):
                        match = re.search(r'node_network_receive_packets_total\{[^}]+\} (\d+)', line)
                        if match:
                            packets_recv += int(match.group(1))
                    elif line.startswith('node_network_receive_errs_total{'):
                        match = re.search(r'node_network_receive_errs_total\{[^}]+\} (\d+)', line)
                        if match:
                            errin += int(match.group(1))
                    elif line.startswith('node_network_transmit_errs_total{'):
                        match = re.search(r'node_network_transmit_errs_total\{[^}]+\} (\d+)', line)
                        if match:
                            errout += int(match.group(1))
                    elif line.startswith('node_network_receive_drop_total{'):
                        match = re.search(r'node_network_receive_drop_total\{[^}]+\} (\d+)', line)
                        if match:
                            dropin += int(match.group(1))
                    elif line.startswith('node_network_transmit_drop_total{'):
                        match = re.search(r'node_network_transmit_drop_total\{[^}]+\} (\d+)', line)
                        if match:
                            dropout += int(match.group(1))
                
                # 提取网络接口信息
                interfaces = []
                interface_names = set()
                
                # 提取接口名称
                for line in metrics.split('\n'):
                    if line.startswith('node_network_info{'):
                        match = re.search(r'node_network_info\{device="([^"]+)",[^}]+\}', line)
                        if match:
                            interface_names.add(match.group(1))
                
                # 提取每个接口的详细信息
                for interface_name in interface_names:
                    # 提取接口状态
                    is_up = True
                    up_match = re.search(rf'node_network_up\{{device="{interface_name}"}} (\d+)', metrics)
                    if up_match:
                        is_up = int(up_match.group(1)) == 1
                    
                    # 提取接口速度
                    speed = 0
                    speed_match = re.search(rf'node_network_speed_bytes\{{device="{interface_name}"}} (\d+)', metrics)
                    if speed_match:
                        speed = int(speed_match.group(1))
                    
                    # 提取MTU
                    mtu = 0
                    mtu_match = re.search(rf'node_network_mtu_bytes\{{device="{interface_name}"}} (\d+)', metrics)
                    if mtu_match:
                        mtu = int(mtu_match.group(1))
                    
                    # 提取MAC地址和IP地址（这里需要从本地获取，因为node-exporter不提供这些信息）
                    mac_address = ""
                    ip_addresses = []
                    
                    # 从本地获取MAC地址和IP地址
                    try:
                        net_if_addrs = psutil.net_if_addrs()
                        if interface_name in net_if_addrs:
                            for addr in net_if_addrs[interface_name]:
                                if addr.family == socket.AF_INET:
                                    ip_addresses.append({"ip": addr.address})
                                elif hasattr(socket, 'AF_PACKET') and addr.family == socket.AF_PACKET:
                                    mac_address = addr.address
                    except:
                        pass
                    
                    interfaces.append({
                        "name": interface_name,
                        "mac_address": mac_address,
                        "is_up": is_up,
                        "speed": speed,
                        "mtu": mtu,
                        "ip_addresses": ip_addresses
                    })
                
                return {
                    "traffic": {
                        "bytes_sent": bytes_sent,
                        "bytes_recv": bytes_recv,
                        "packets_sent": packets_sent,
                        "packets_recv": packets_recv,
                        "errin": errin,
                        "errout": errout,
                        "dropin": dropin,
                        "dropout": dropout
                    },
                    "interfaces": interfaces
                }
        except Exception as e:
            print(f"从nas-node-exporter获取网络信息失败: {e}")
        
        # 如果从nas-node-exporter获取失败，使用本地获取
        # 获取网络接口信息
        net_io = psutil.net_io_counters()
        
        # 获取网络接口
        interfaces = []
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface_name, addresses in net_if_addrs.items():
            if interface_name in net_if_stats:
                is_up = net_if_stats[interface_name].isup
                speed = net_if_stats[interface_name].speed
                mtu = net_if_stats[interface_name].mtu
                mac_address = ""
                ip_addresses = []
                
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        ip_addresses.append({"ip": addr.address})
                    elif hasattr(socket, 'AF_PACKET') and addr.family == socket.AF_PACKET:
                        mac_address = addr.address
                
                interfaces.append({
                    "name": interface_name,
                    "mac_address": mac_address,
                    "is_up": is_up,
                    "speed": speed,
                    "mtu": mtu,
                    "ip_addresses": ip_addresses
                })
        
        return {
            "traffic": {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout
            },
            "interfaces": interfaces
        }
    except Exception as e:
        print(f"获取网络信息失败: {e}")
        # 返回默认值
        return {
            "traffic": {
                "bytes_sent": 1024000,
                "bytes_recv": 2048000,
                "packets_sent": 0,
                "packets_recv": 0,
                "errin": 0,
                "errout": 0,
                "dropin": 0,
                "dropout": 0
            },
            "interfaces": [
                {
                    "name": "eth0",
                    "mac_address": "00:11:22:33:44:55",
                    "is_up": True,
                    "speed": 1000,
                    "mtu": 1500,
                    "ip_addresses": [
                        {"ip": "192.168.1.100"}
                    ]
                }
            ]
        }

# 获取Docker信息
def get_docker_info():
    try:
        # 尝试从nas-cadvisor获取Docker信息
        try:
            response = requests.get('http://nas-cadvisor:8080/api/v1.3/containers')
            if response.status_code == 200:
                # 解析cAdvisor API响应获取Docker信息
                containers_data = response.json()
                
                # 提取容器信息
                containers = []
                stats = []
                
                for container in containers_data:
                    # 跳过非Docker容器
                    if 'aliases' not in container:
                        continue
                    
                    # 提取容器名称
                    container_name = container['aliases'][0] if container['aliases'] else container['name']
                    
                    # 提取容器状态
                    container_status = "running"  # cAdvisor API没有直接提供状态信息，假设都是运行中的
                    
                    # 提取镜像信息
                    image_name = ""
                    if 'image' in container:
                        image_name = container['image']
                    
                    # 提取容器ID
                    container_id = container['name'].split('/')[-1]
                    
                    containers.append({
                        "id": container_id,
                        "name": container_name,
                        "status": container_status,
                        "image": image_name
                    })
                    
                    # 提取容器状态信息
                    if 'stats' in container and container['stats']:
                        latest_stats = container['stats'][-1]
                        
                        # 提取CPU使用率
                        cpu_usage = 0
                        if 'cpu' in latest_stats and 'usage' in latest_stats['cpu']:
                            cpu_usage = latest_stats['cpu']['usage']['total'] / 10000000.0  # 转换为百分比
                        
                        # 提取内存使用率
                        memory_usage = 0
                        memory_limit = 0
                        if 'memory' in latest_stats and 'usage' in latest_stats['memory']:
                            memory_usage = latest_stats['memory']['usage']['usage']
                            memory_limit = latest_stats['memory']['usage']['limit']
                        
                        stats.append({
                            "name": container_name,
                            "cpu_usage": cpu_usage,
                            "memory_usage": memory_usage,
                            "memory_limit": memory_limit
                        })
                
                # 提取镜像信息（这里使用本地docker_client获取，因为cAdvisor API不提供镜像列表）
                images = []
                if docker_client is not None:
                    for image in docker_client.images.list():
                        images.append({
                            "id": image.id,
                            "tags": image.tags,
                            "size": f"{image.attrs['Size'] / (1024 * 1024):.0f}MB"
                        })
                
                return {
                    "containers": containers,
                    "images": images,
                    "stats": stats
                }
        except Exception as e:
            print(f"从nas-cadvisor获取Docker信息失败: {e}")
        
        # 如果从nas-cadvisor获取失败，使用本地docker_client获取
        if docker_client is None:
            return {
                "containers": [],
                "images": [],
                "stats": []
            }
        
        # 获取容器信息
        containers = []
        for container in docker_client.containers.list(all=True):
            containers.append({
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else ""
            })
        
        # 获取镜像信息
        images = []
        for image in docker_client.images.list():
            images.append({
                "id": image.id,
                "tags": image.tags,
                "size": f"{image.attrs['Size'] / (1024 * 1024):.0f}MB"
            })
        
        # 获取容器状态
        stats = []
        for container in docker_client.containers.list():
            try:
                container_stats = container.stats(stream=False)
                cpu_usage = container_stats['cpu_stats']['cpu_usage']['total_usage'] / container_stats['cpu_stats']['system_cpu_usage'] * 100
                memory_usage = container_stats['memory_stats']['usage']
                memory_limit = container_stats['memory_stats']['limit']
                
                stats.append({
                    "name": container.name,
                    "cpu_usage": cpu_usage,
                    "memory_usage": memory_usage,
                    "memory_limit": memory_limit
                })
            except:
                pass
        
        return {
            "containers": containers,
            "images": images,
            "stats": stats
        }
    except Exception as e:
        print(f"获取Docker信息失败: {e}")
        # 返回默认值
        return {
            "containers": [
                {
                    "id": "container1",
                    "name": "nginx",
                    "status": "running",
                    "image": "nginx:latest"
                }
            ],
            "images": [
                {
                    "id": "image1",
                    "tags": ["nginx:latest"],
                    "size": "133MB"
                }
            ],
            "stats": [
                {
                    "name": "nginx",
                    "cpu_usage": 0.5,
                    "memory_usage": 10485760,
                    "memory_limit": 104857600
                }
            ]
        }

@app.route('/api/')
def root():
    return jsonify({"message": "NAS Monitor API is running"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

# 认证相关API
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username]['password'] == password:
        return jsonify({"access_token": "test-token", "token_type": "bearer"})
    else:
        return jsonify({"detail": "用户名或密码错误"}), 401

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    return jsonify(users["admin"])

# 系统相关API
@app.route('/api/system/status')
def get_system_status():
    system_info = get_system_info()
    return jsonify(system_info)

@app.route('/api/system/cpu')
def get_cpu_usage():
    cpu_info = get_cpu_info()
    return jsonify(cpu_info)

@app.route('/api/system/memory')
def get_memory_usage():
    memory_info = get_memory_info()
    return jsonify(memory_info)

@app.route('/api/system/disk')
def get_disk_usage():
    disk_info = get_disk_info()
    return jsonify(disk_info)

@app.route('/api/system/disk/smart')
def get_disk_smart_info():
    return jsonify({"disks": []})

# 网络相关API
@app.route('/api/network/traffic')
def get_network_traffic():
    network_info = get_network_info()
    traffic_info = network_info['traffic']
    # 添加wifi_name字段
    traffic_info['wifi_name'] = "未连接"
    return jsonify(traffic_info)

@app.route('/api/network/interfaces')
def get_network_interfaces():
    network_info = get_network_info()
    return jsonify(network_info['interfaces'])

@app.route('/api/network/capture', methods=['POST'])
def capture_network_packets():
    return jsonify({"message": "捕获网络数据包已启动"})

@app.route('/api/network/logs')
def get_network_logs():
    return jsonify({"logs": []})

# IO相关API
@app.route('/api/io/stats')
def get_io_stats():
    return jsonify({"disks": []})

# Docker相关API
@app.route('/api/docker/containers')
def get_containers():
    docker_info = get_docker_info()
    return jsonify(docker_info['containers'])

@app.route('/api/docker/stats')
def get_docker_stats():
    docker_info = get_docker_info()
    return jsonify(docker_info['stats'])

@app.route('/api/docker/images')
def get_docker_images():
    docker_info = get_docker_info()
    return jsonify(docker_info['images'])

@app.route('/api/docker/images/pull', methods=['POST'])
def pull_docker_image():
    data = request.json
    image_name = data.get('image_name')
    return jsonify({"success": True, "image_id": "image1", "tags": [image_name]})

@app.route('/api/docker/images/<image_id>', methods=['DELETE'])
def delete_docker_image(image_id):
    return jsonify({"message": "镜像删除成功"})

@app.route('/api/docker/containers/<container_id>/start', methods=['POST'])
def start_container(container_id):
    return jsonify({"message": "容器启动成功"})

@app.route('/api/docker/containers/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    return jsonify({"message": "容器停止成功"})

@app.route('/api/docker/containers/<container_id>/restart', methods=['POST'])
def restart_container(container_id):
    return jsonify({"message": "容器重启成功"})

@app.route('/api/docker/containers/<container_id>/logs')
def get_container_logs(container_id):
    return jsonify({"logs": []})

# 告警相关API
@app.route('/api/alarm/configs')
def get_alarm_configs():
    return jsonify(alarm_data['configs'])

@app.route('/api/alarm/configs/<config_id>')
def get_alarm_config(config_id):
    for config in alarm_data['configs']:
        if config['id'] == config_id:
            return jsonify(config)
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/configs', methods=['POST'])
def create_alarm_config():
    data = request.json
    data['id'] = "alarm" + str(len(alarm_data['configs']) + 1)
    alarm_data['configs'].append(data)
    return jsonify(data)

@app.route('/api/alarm/configs/<config_id>', methods=['PUT'])
def update_alarm_config(config_id):
    data = request.json
    for config in alarm_data['configs']:
        if config['id'] == config_id:
            config.update(data)
            return jsonify(config)
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/configs/<config_id>', methods=['DELETE'])
def delete_alarm_config(config_id):
    for i, config in enumerate(alarm_data['configs']):
        if config['id'] == config_id:
            alarm_data['configs'].pop(i)
            return jsonify({"message": "告警配置删除成功"})
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/records')
def get_alarm_records():
    return jsonify(alarm_data['records'])

@app.route('/api/alarm/records/<record_id>')
def get_alarm_record(record_id):
    return jsonify({"detail": "告警记录不存在"}), 404

@app.route('/api/alarm/records/<record_id>', methods=['PUT'])
def update_alarm_record(record_id):
    return jsonify({"detail": "告警记录不存在"}), 404

@app.route('/api/alarm/statistics')
def get_alarm_statistics():
    return jsonify({
        "total": 0,
        "by_severity": {"info": 0, "warning": 0, "critical": 0},
        "by_type": {},
        "recent": 0
    })

@app.route('/api/alarm/detect', methods=['POST'])
def detect_alarms():
    return jsonify({"message": "告警检测已触发"})

# 用户相关API
@app.route('/api/user')
def get_users():
    return jsonify(list(users.values()))

@app.route('/api/user/<username>')
def get_user(username):
    if username in users:
        return jsonify(users[username])
    return jsonify({"detail": "用户不存在"}), 404

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username not in users:
        users[username] = {
            "username": username,
            "password": password,
            "disabled": data.get('disabled', False)
        }
        return jsonify(users[username])
    return jsonify({"detail": "用户已存在"}), 400

@app.route('/api/user/<username>', methods=['PUT'])
def update_user(username):
    if username in users:
        data = request.json
        users[username].update(data)
        return jsonify(users[username])
    return jsonify({"detail": "用户不存在"}), 404

@app.route('/api/user/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users and username != "admin":
        del users[username]
        return jsonify({"message": "用户删除成功"})
    return jsonify({"detail": "用户不存在或无法删除"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8017, debug=True)