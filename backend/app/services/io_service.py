import logging

logger = logging.getLogger("nas-monitor.io")

try:
    import psutil
except ImportError:
    logger.error("psutil library not installed")
    psutil = None


def get_disk_io():
    """获取磁盘 IO 信息"""
    if psutil is None:
        return []

    result = []
    try:
        disk_io = psutil.disk_io_counters(perdisk=True)
        if disk_io is None:
            return result

        for disk_name, io_stats in disk_io.items():
            result.append({
                "disk_name": disk_name,
                "read_bytes": io_stats.read_bytes,
                "write_bytes": io_stats.write_bytes,
                "read_count": io_stats.read_count,
                "write_count": io_stats.write_count,
                "read_time": io_stats.read_time,
                "write_time": io_stats.write_time,
            })
    except Exception as e:
        logger.error(f"Error getting disk IO: {e}")

    return result


def get_system_io():
    """获取系统 IO 统计信息"""
    if psutil is None:
        return {
            "total_read_bytes": 0, "total_write_bytes": 0,
            "total_read_count": 0, "total_write_count": 0,
            "total_read_time": 0, "total_write_time": 0,
        }

    try:
        system_io = psutil.disk_io_counters(perdisk=False)
        if system_io is None:
            return {
                "total_read_bytes": 0, "total_write_bytes": 0,
                "total_read_count": 0, "total_write_count": 0,
                "total_read_time": 0, "total_write_time": 0,
            }

        return {
            "total_read_bytes": system_io.read_bytes,
            "total_write_bytes": system_io.write_bytes,
            "total_read_count": system_io.read_count,
            "total_write_count": system_io.write_count,
            "total_read_time": system_io.read_time,
            "total_write_time": system_io.write_time,
        }
    except Exception as e:
        logger.error(f"Error getting system IO: {e}")
        return {
            "total_read_bytes": 0, "total_write_bytes": 0,
            "total_read_count": 0, "total_write_count": 0,
            "total_read_time": 0, "total_write_time": 0,
        }
