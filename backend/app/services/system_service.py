import psutil
import platform
import time
from datetime import datetime
import os
import re
try:
    from pySMART import DeviceList
except ImportError:
    print("pySMART library not installed. Disk S.M.A.R.T monitoring will be disabled.")
    DeviceList = None

def get_system_status():
    """获取系统基本状态"""
    # 初始化默认值
    hostname = "Unknown"
    os_system = "Unknown"
    os_version = "Unknown"
    architecture = "Unknown"
    boot_time = datetime.now()
    uptime_str = "0d 0h 0m 0s"
    
    try:
        # 尝试从/proc获取宿主机信息（适用于Docker容器）
        if os.path.exists("/proc/sys/kernel/hostname"):
            with open("/proc/sys/kernel/hostname", "r") as f:
                hostname = f.read().strip()
        else:
            hostname = platform.node()
        
        # 获取OS信息
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                os_release = f.read()
                # 解析os-release文件
                for line in os_release.splitlines():
                    if line.startswith("NAME="):
                        os_system = line.split("=")[1].strip('"')
                    elif line.startswith("VERSION="):
                        os_version = line.split("=")[1].strip('"')
        elif platform.system() == "Linux":
            # 尝试使用distro库
            try:
                import distro
                os_system = distro.name()
                os_version = distro.version()
            except ImportError:
                os_version = platform.version()
        elif platform.system() == "Windows":
            os_system = platform.system()
            os_version = " ".join(platform.win32_ver())
        else:
            os_system = platform.system()
            os_version = platform.version()
        
        # 获取架构信息
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                arch_match = re.search(r"model name\s*:\s*(.+)", cpuinfo)
                if arch_match:
                    architecture = arch_match.group(1)
        else:
            architecture = platform.machine()
        
        # 获取启动时间和运行时间
        if os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.read().split()[0])
                boot_time = datetime.now() - datetime.timedelta(seconds=uptime_seconds)
        else:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            uptime_seconds = int((current_time - boot_time).total_seconds())
        
        # 计算运行时间
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        
    except Exception as e:
        print(f"Error getting system status: {e}")
        # 发生错误时，使用psutil获取容器内的信息作为备选
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            current_time = datetime.now()
            uptime_seconds = int((current_time - boot_time).total_seconds())
            days = uptime_seconds // (24 * 3600)
            hours = (uptime_seconds % (24 * 3600)) // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
            
            hostname = platform.node()
            os_system = platform.system()
            os_version = platform.version()
            architecture = platform.machine()
        except Exception as backup_e:
            print(f"Backup error: {backup_e}")
    
    return {
        "hostname": hostname,
        "os": os_system,
        "os_version": os_version,
        "architecture": architecture,
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": uptime_str
    }

def get_cpu_usage():
    """获取 CPU 使用情况"""
    # 初始化默认值
    total_usage = 0.0
    per_core_usage = []
    cpu_count = {
        "physical": 0,
        "logical": 0
    }
    
    try:
        # 尝试从/proc/stat获取CPU使用率（适用于Docker容器）
        if os.path.exists("/proc/stat"):
            # 读取第一次CPU状态
            with open("/proc/stat", "r") as f:
                lines1 = f.readlines()
            
            # 等待0.1秒
            time.sleep(0.1)
            
            # 读取第二次CPU状态
            with open("/proc/stat", "r") as f:
                lines2 = f.readlines()
            
            # 解析CPU状态
            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if line1.startswith("cpu"):
                    parts1 = list(map(int, line1.split()[1:]))
                    parts2 = list(map(int, line2.split()[1:]))
                    
                    # 计算CPU使用率
                    total1 = sum(parts1)
                    total2 = sum(parts2)
                    idle1 = parts1[3]
                    idle2 = parts2[3]
                    
                    # 计算总时间差和空闲时间差
                    total_diff = total2 - total1
                    idle_diff = idle2 - idle1
                    
                    if total_diff > 0:
                        usage = 100.0 * (1.0 - idle_diff / total_diff)
                        if i == 0:
                            # 总CPU使用率
                            total_usage = usage
                        else:
                            # 每个核心的使用率
                            per_core_usage.append(usage)
            
            # 获取CPU核心数
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                physical_cores = len(set(re.findall(r"physical id\s*:\s*(\d+)", cpuinfo)))
                logical_cores = len(re.findall(r"processor\s*:\s*(\d+)", cpuinfo))
                cpu_count = {
                    "physical": physical_cores,
                    "logical": logical_cores
                }
        else:
            # 使用psutil获取CPU信息
            total_usage = psutil.cpu_percent(interval=0.1)
            per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
            cpu_count = {
                "physical": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True)
            }
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        # 发生错误时，使用psutil作为备选
        try:
            total_usage = psutil.cpu_percent(interval=0.1)
            per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
            cpu_count = {
                "physical": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True)
            }
        except Exception as backup_e:
            print(f"Backup error: {backup_e}")
    
    return {
        "total_usage": total_usage,
        "per_core_usage": per_core_usage,
        "cpu_count": cpu_count
    }

def get_memory_usage():
    """获取内存使用情况"""
    # 初始化默认值
    memory = {
        "total": 0,
        "available": 0,
        "used": 0,
        "percent": 0.0
    }
    swap = {
        "total": 0,
        "used": 0,
        "free": 0,
        "percent": 0.0
    }
    
    try:
        # 尝试从/proc/meminfo获取内存信息（适用于Docker容器）
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read()
            
            # 解析内存信息
            mem_total_match = re.search(r"MemTotal:\s*(\d+)\s*kB", meminfo)
            mem_available_match = re.search(r"MemAvailable:\s*(\d+)\s*kB", meminfo)
            mem_free_match = re.search(r"MemFree:\s*(\d+)\s*kB", meminfo)
            mem_buffers_match = re.search(r"Buffers:\s*(\d+)\s*kB", meminfo)
            mem_cached_match = re.search(r"Cached:\s*(\d+)\s*kB", meminfo)
            swap_total_match = re.search(r"SwapTotal:\s*(\d+)\s*kB", meminfo)
            swap_free_match = re.search(r"SwapFree:\s*(\d+)\s*kB", meminfo)
            
            if mem_total_match:
                total_kb = int(mem_total_match.group(1))
                total = total_kb * 1024  # 转换为字节
                memory["total"] = total
            
            if mem_available_match:
                available_kb = int(mem_available_match.group(1))
                available = available_kb * 1024  # 转换为字节
                memory["available"] = available
            
            if memory["total"] > 0 and memory["available"] > 0:
                memory["used"] = memory["total"] - memory["available"]
                memory["percent"] = (memory["used"] / memory["total"]) * 100
            
            # 解析交换分区信息
            if swap_total_match:
                swap_total_kb = int(swap_total_match.group(1))
                swap_total = swap_total_kb * 1024  # 转换为字节
                swap["total"] = swap_total
            
            if swap_free_match:
                swap_free_kb = int(swap_free_match.group(1))
                swap_free = swap_free_kb * 1024  # 转换为字节
                swap["free"] = swap_free
            
            if swap["total"] > 0:
                swap["used"] = swap["total"] - swap["free"]
                swap["percent"] = (swap["used"] / swap["total"]) * 100
        else:
            # 使用psutil获取内存信息
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            memory = {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent
            }
            swap = {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
    except Exception as e:
        print(f"Error getting memory usage: {e}")
        # 发生错误时，使用psutil作为备选
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            memory = {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent
            }
            swap = {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        except Exception as backup_e:
            print(f"Backup error: {backup_e}")
    
    return {
        "memory": memory,
        "swap": swap
    }

def get_disk_usage():
    """获取磁盘使用情况"""
    disks = []
    
    try:
        # 尝试从/proc/mounts获取挂载点信息（适用于Docker容器）
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r") as f:
                mounts = f.readlines()
            
            # 解析挂载点信息
            for mount in mounts:
                parts = mount.split()
                if len(parts) < 6:
                    continue
                
                device = parts[0]
                mountpoint = parts[1]
                fstype = parts[2]
                
                # 跳过特殊文件系统和虚拟文件系统
                if fstype in ["proc", "sysfs", "tmpfs", "devtmpfs", "devpts", "cgroup", "overlay", "aufs", "shm"]:
                    continue
                
                # 跳过Docker相关的挂载点
                if "/var/lib/docker" in mountpoint or "/var/lib/containerd" in mountpoint:
                    continue
                
                try:
                    # 使用psutil获取磁盘使用情况
                    usage = psutil.disk_usage(mountpoint)
                    disks.append({
                        "device": device,
                        "mountpoint": mountpoint,
                        "fstype": fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except Exception as e:
                    # 跳过无法访问的挂载点
                    continue
        else:
            # 使用psutil获取磁盘信息
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except PermissionError:
                    continue
    except Exception as e:
        print(f"Error getting disk usage: {e}")
        # 发生错误时，使用psutil作为备选
        try:
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except PermissionError:
                    continue
        except Exception as backup_e:
            print(f"Backup error: {backup_e}")
    
    return disks

def get_disk_smart_info():
    """获取磁盘S.M.A.R.T信息"""
    if DeviceList is None:
        return {"error": "pySMART library not installed"}
    
    disks = []
    try:
        # 获取所有设备
        devices = DeviceList()
        
        for device in devices:
            try:
                # 构建磁盘信息
                disk_info = {
                    "device": device.name,
                    "model": device.model,
                    "serial": device.serial,
                    "firmware": device.firmware,
                    "interface": device.interface,
                    "size": device.capacity,
                    "health": device.health,
                    "temperature": device.temperature if hasattr(device, 'temperature') else None,
                    "smart_attributes": []
                }
                
                # 获取S.M.A.R.T属性
                if hasattr(device, 'attributes'):
                    for attr in device.attributes:
                        if attr is not None:
                            disk_info["smart_attributes"].append({
                                "id": attr.id,
                                "name": attr.name,
                                "value": attr.value,
                                "worst": attr.worst,
                                "threshold": attr.threshold,
                                "raw_value": attr.raw,
                                "status": attr.status
                            })
                
                disks.append(disk_info)
            except Exception as e:
                print(f"Error getting S.M.A.R.T info for {device.name}: {e}")
                continue
    except Exception as e:
        print(f"Error getting disk S.M.A.R.T info: {e}")
        return {"error": str(e)}
    
    return disks