import psutil

def get_network_traffic():
    """获取网络流量信息"""
    try:
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "errin": net_io.errin,
            "errout": net_io.errout,
            "dropin": net_io.dropin,
            "dropout": net_io.dropout
        }
    except Exception as e:
        # 记录错误，并返回默认值
        print(f"Error getting network traffic: {e}")
        return {
            "bytes_sent": 0,
            "bytes_recv": 0,
            "packets_sent": 0,
            "packets_recv": 0,
            "errin": 0,
            "errout": 0,
            "dropin": 0,
            "dropout": 0
        }

def get_network_interfaces():
    """获取网络接口信息"""
    interfaces = []
    try:
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface_name, addresses in net_if_addrs.items():
            interface_stats = net_if_stats.get(interface_name, None)
            if not interface_stats:
                continue
            
            ip_addresses = []
            mac_address = None
            
            for addr in addresses:
                try:
                    if addr.family == psutil.AF_INET:
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": addr.broadcast
                        })
                    elif addr.family == psutil.AF_INET6:
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask
                        })
                    elif addr.family == psutil.AF_LINK:
                        mac_address = addr.address
                except Exception as e:
                    # 跳过有问题的地址，继续处理其他地址
                    print(f"Error processing address {addr}: {e}")
                    continue
            
            interfaces.append({
                "name": interface_name,
                "mac_address": mac_address,
                "ip_addresses": ip_addresses,
                "is_up": interface_stats.isup,
                "speed": interface_stats.speed,
                "mtu": interface_stats.mtu
            })
    except Exception as e:
        # 记录错误，并返回空列表
        print(f"Error getting network interfaces: {e}")
    
    return interfaces
