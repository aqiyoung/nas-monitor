import psutil
import platform
import time
from datetime import datetime

def get_system_status():
    """获取系统基本状态"""
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    current_time = datetime.now()
    uptime_seconds = int((current_time - boot_time).total_seconds())
    
    # 计算运行时间
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    # 获取OS版本信息
    os_system = platform.system()
    if os_system == "Windows":
        # 对于Windows系统，使用win32_ver获取更详细的版本信息
        os_version = " ".join(platform.win32_ver())
    else:
        # 对于其他系统，使用platform.version()
        os_version = platform.version()
    
    return {
        "hostname": platform.node(),
        "os": os_system,
        "os_version": os_version,
        "architecture": platform.machine(),
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": uptime_str
    }

def get_cpu_usage():
    """获取 CPU 使用情况"""
    # 使用0.1秒间隔获取更准确的CPU使用率
    total_usage = psutil.cpu_percent(interval=0.1)
    per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
    
    cpu_count = {
        "physical": psutil.cpu_count(logical=False),
        "logical": psutil.cpu_count(logical=True)
    }
    
    return {
        "total_usage": total_usage,
        "per_core_usage": per_core_usage,
        "cpu_count": cpu_count
    }

def get_memory_usage():
    """获取内存使用情况"""
    memory = psutil.virtual_memory()
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

def get_disk_usage():
    """获取磁盘使用情况"""
    disks = []
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
    return disks