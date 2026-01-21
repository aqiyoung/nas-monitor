import psutil

def get_disk_io():
    """获取磁盘 IO 信息"""
    disk_io = psutil.disk_io_counters(perdisk=True)
    result = []
    
    for disk_name, io_stats in disk_io.items():
        result.append({
            "disk_name": disk_name,
            "read_bytes": io_stats.read_bytes,
            "write_bytes": io_stats.write_bytes,
            "read_count": io_stats.read_count,
            "write_count": io_stats.write_count,
            "read_time": io_stats.read_time,
            "write_time": io_stats.write_time
        })
    
    return result

def get_system_io():
    """获取系统 IO 统计信息"""
    system_io = psutil.disk_io_counters(perdisk=False)
    return {
        "total_read_bytes": system_io.read_bytes,
        "total_write_bytes": system_io.write_bytes,
        "total_read_count": system_io.read_count,
        "total_write_count": system_io.write_count,
        "total_read_time": system_io.read_time,
        "total_write_time": system_io.write_time
    }
