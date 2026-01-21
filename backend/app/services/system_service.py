import psutil
import platform
import time
from datetime import datetime

def get_system_status():
    """获取系统基本状态"""
    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "boot_time": datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": get_uptime()
    }

def get_uptime():
    """获取系统运行时间"""
    uptime_seconds = int(time.time() - psutil.boot_time())
    days = uptime_seconds // (24 * 3600)
    hours = (uptime_seconds % (24 * 3600)) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_cpu_usage():
    """获取 CPU 使用情况"""
    # 只调用一次cpu_percent，使用interval=0获取当前值
    psutil.cpu_percent(interval=0)
    # 立即获取当前CPU使用率，不阻塞
    total_usage = psutil.cpu_percent(interval=0)
    per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
    
    return {
        "total_usage": total_usage,
        "per_core_usage": per_core_usage,
        "cpu_count": {
            "physical": psutil.cpu_count(logical=False),
            "logical": psutil.cpu_count(logical=True)
        }
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
