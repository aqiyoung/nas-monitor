import psutil
import platform
import time
import logging
from datetime import datetime, timedelta
import os
import re

logger = logging.getLogger("nas-monitor.system")

try:
    from pySMART import DeviceList
except ImportError:
    logger.warning("pySMART library not installed. Disk S.M.A.R.T monitoring will be disabled.")
    DeviceList = None


def get_system_status():
    """获取系统基本状态"""
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
                for line in f.read().splitlines():
                    if line.startswith("NAME="):
                        os_system = line.split("=")[1].strip('"')
                    elif line.startswith("VERSION="):
                        os_version = line.split("=")[1].strip('"')
        elif platform.system() == "Linux":
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
                arch_match = re.search(r"model name\s*:\s*(.+)", f.read())
                if arch_match:
                    architecture = arch_match.group(1).strip()
        else:
            architecture = platform.machine()

        # 获取启动时间和运行时间
        if os.path.exists("/proc/uptime"):
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.read().split()[0])
                boot_time = datetime.now() - timedelta(seconds=uptime_seconds)
        else:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime_seconds = (datetime.now() - boot_time).total_seconds()

        # 计算运行时间
        days = int(uptime_seconds // (24 * 3600))
        hours = int((uptime_seconds % (24 * 3600)) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"

    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime_seconds = (datetime.now() - boot_time).total_seconds()
            days = int(uptime_seconds // (24 * 3600))
            hours = int((uptime_seconds % (24 * 3600)) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            seconds = int(uptime_seconds % 60)
            uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
            hostname = platform.node()
            os_system = platform.system()
            os_version = platform.version()
            architecture = platform.machine()
        except Exception as backup_e:
            logger.error(f"Backup error: {backup_e}")

    return {
        "hostname": hostname,
        "os": os_system,
        "os_version": os_version,
        "architecture": architecture,
        "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": uptime_str,
    }


def get_cpu_usage():
    """获取 CPU 使用情况"""
    total_usage = 0.0
    per_core_usage = []
    cpu_count = {"physical": 0, "logical": 0}

    try:
        if os.path.exists("/proc/stat"):
            with open("/proc/stat", "r") as f:
                lines1 = f.readlines()
            time.sleep(0.1)
            with open("/proc/stat", "r") as f:
                lines2 = f.readlines()

            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if line1.startswith("cpu"):
                    parts1 = list(map(int, line1.split()[1:]))
                    parts2 = list(map(int, line2.split()[1:]))
                    total_diff = sum(parts2) - sum(parts1)
                    idle_diff = parts2[3] - parts1[3]
                    if total_diff > 0:
                        usage = 100.0 * (1.0 - idle_diff / total_diff)
                        if i == 0:
                            total_usage = usage
                        else:
                            per_core_usage.append(usage)

            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
                cpu_count = {
                    "physical": len(set(re.findall(r"physical id\s*:\s*(\d+)", cpuinfo))),
                    "logical": len(re.findall(r"processor\s*:\s*(\d+)", cpuinfo)),
                }
        else:
            total_usage = psutil.cpu_percent(interval=0.1)
            per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
            cpu_count = {
                "physical": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True),
            }
    except Exception as e:
        logger.error(f"Error getting CPU usage: {e}")
        try:
            total_usage = psutil.cpu_percent(interval=0.1)
            per_core_usage = psutil.cpu_percent(interval=0, percpu=True)
            cpu_count = {
                "physical": psutil.cpu_count(logical=False),
                "logical": psutil.cpu_count(logical=True),
            }
        except Exception as backup_e:
            logger.error(f"Backup error: {backup_e}")

    return {
        "total_usage": total_usage,
        "per_core_usage": per_core_usage,
        "cpu_count": cpu_count,
    }


def get_memory_usage():
    """获取内存使用情况"""
    memory = {"total": 0, "available": 0, "used": 0, "percent": 0.0}
    swap = {"total": 0, "used": 0, "free": 0, "percent": 0.0}

    try:
        if os.path.exists("/proc/meminfo"):
            with open("/proc/meminfo", "r") as f:
                meminfo = f.read()

            patterns = {
                "MemTotal": r"MemTotal:\s*(\d+)\s*kB",
                "MemAvailable": r"MemAvailable:\s*(\d+)\s*kB",
                "SwapTotal": r"SwapTotal:\s*(\d+)\s*kB",
                "SwapFree": r"SwapFree:\s*(\d+)\s*kB",
            }
            values = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, meminfo)
                values[key] = int(match.group(1)) * 1024 if match else 0

            memory["total"] = values["MemTotal"]
            memory["available"] = values["MemAvailable"]
            if memory["total"] > 0:
                memory["used"] = memory["total"] - memory["available"]
                memory["percent"] = (memory["used"] / memory["total"]) * 100

            swap["total"] = values["SwapTotal"]
            swap["free"] = values["SwapFree"]
            if swap["total"] > 0:
                swap["used"] = swap["total"] - swap["free"]
                swap["percent"] = (swap["used"] / swap["total"]) * 100
        else:
            mem = psutil.virtual_memory()
            swap_mem = psutil.swap_memory()
            memory = {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
            }
            swap = {
                "total": swap_mem.total,
                "used": swap_mem.used,
                "free": swap_mem.free,
                "percent": swap_mem.percent,
            }
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        try:
            mem = psutil.virtual_memory()
            swap_mem = psutil.swap_memory()
            memory = {
                "total": mem.total,
                "available": mem.available,
                "used": mem.used,
                "percent": mem.percent,
            }
            swap = {
                "total": swap_mem.total,
                "used": swap_mem.used,
                "free": swap_mem.free,
                "percent": swap_mem.percent,
            }
        except Exception as backup_e:
            logger.error(f"Backup error: {backup_e}")

    return {"memory": memory, "swap": swap}


def get_disk_usage():
    """获取磁盘使用情况"""
    disks = []
    skip_fs_types = {"proc", "sysfs", "tmpfs", "devtmpfs", "devpts", "cgroup", "overlay", "aufs", "shm"}
    skip_paths = {"/var/lib/docker", "/var/lib/containerd"}

    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r") as f:
                mounts = f.readlines()

            for mount in mounts:
                parts = mount.split()
                if len(parts) < 6:
                    continue
                device, mountpoint, fstype = parts[0], parts[1], parts[2]

                if fstype in skip_fs_types or any(p in mountpoint for p in skip_paths):
                    continue

                try:
                    usage = psutil.disk_usage(mountpoint)
                    disks.append({
                        "device": device,
                        "mountpoint": mountpoint,
                        "fstype": fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent,
                    })
                except (PermissionError, OSError):
                    continue
        else:
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
                        "percent": usage.percent,
                    })
                except (PermissionError, OSError):
                    continue
    except Exception as e:
        logger.error(f"Error getting disk usage: {e}")

    return disks


def get_disk_smart_info():
    """获取磁盘S.M.A.R.T信息"""
    if DeviceList is None:
        return {"error": "pySMART library not installed"}

    disks = []
    try:
        devices = DeviceList()
        for device in devices:
            try:
                disk_info = {
                    "device": device.name,
                    "model": device.model,
                    "serial": device.serial,
                    "firmware": device.firmware,
                    "interface": device.interface,
                    "size": device.capacity,
                    "health": device.health,
                    "temperature": getattr(device, "temperature", None),
                    "smart_attributes": [],
                }

                if hasattr(device, "attributes"):
                    for attr in device.attributes:
                        if attr is not None:
                            disk_info["smart_attributes"].append({
                                "id": attr.id,
                                "name": attr.name,
                                "value": attr.value,
                                "worst": attr.worst,
                                "threshold": attr.threshold,
                                "raw_value": attr.raw,
                                "status": attr.status,
                            })

                disks.append(disk_info)
            except Exception as e:
                logger.error(f"Error getting S.M.A.R.T info for {device.name}: {e}")
                continue
    except Exception as e:
        logger.error(f"Error getting disk S.M.A.R.T info: {e}")
        return {"error": str(e)}

    return disks
