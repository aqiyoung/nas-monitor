import psutil

def get_network_traffic():
    """获取网络流量信息"""
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

def get_network_interfaces():
    """获取网络接口信息"""
    interfaces = []
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()
    
    for interface_name, addresses in net_if_addrs.items():
        interface_stats = net_if_stats.get(interface_name, None)
        if not interface_stats:
            continue
        
        ip_addresses = []
        mac_address = None
        
        for addr in addresses:
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
        
        interfaces.append({
            "name": interface_name,
            "mac_address": mac_address,
            "ip_addresses": ip_addresses,
            "is_up": interface_stats.isup,
            "speed": interface_stats.speed,
            "mtu": interface_stats.mtu
        })
    
    return interfaces
