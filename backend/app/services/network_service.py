import psutil
import platform
try:
    import pcap
except ImportError:
    print("python-pcap library not installed. Network packet capture will be disabled.")
    pcap = None
try:
    import aiofiles
except ImportError:
    print("aiofiles library not installed. Asynchronous file operations will be disabled.")
    aiofiles = None
import asyncio
import time
import os

def get_wifi_name():
    """获取当前连接的WiFi名称"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows系统 - 使用更可靠的方式处理编码
            import subprocess
            # 先捕获原始字节输出，然后手动解码
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=False,  # 先以字节形式获取输出
                check=True
            )
            # 尝试使用GBK解码，如果失败则使用Latin-1作为后备
            try:
                output = result.stdout.decode('gbk')
            except UnicodeDecodeError:
                output = result.stdout.decode('latin-1')
            
            for line in output.splitlines():
                if "SSID" in line and ":" in line:
                    # 分割并处理不同语言的情况
                    parts = line.split(":")
                    if len(parts) > 1:
                        ssid = parts[1].strip()
                        # 排除未连接状态（中文系统显示"无"，英文系统显示""）
                        if ssid and ssid != "无":
                            return ssid
        elif system == "Darwin":  # macOS
            import subprocess
            result = subprocess.run(
                ["networksetup", "-getairportnetwork", "en0"],
                capture_output=True,
                text=True,
                check=True
            )
            if "Current Wi-Fi Network:" in result.stdout:
                return result.stdout.split(":")[1].strip()
        elif system == "Linux":
            # 尝试不同的Linux命令
            import subprocess
            commands = [
                # 方法1: 使用iwgetid
                ["iwgetid", "-r"],
                # 方法2: 使用nmcli
                ["nmcli", "--get-values", "SSID", "device", "wifi", "list", "--active"],
                # 方法3: 使用iw
                ["iw", "dev", "wlan0", "link"]
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    ssid = result.stdout.strip()
                    if ssid and ssid != "off/any":
                        return ssid
                except:
                    continue
    except Exception as e:
        print(f"Error getting WiFi name: {e}")
    
    return None

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
            "dropout": net_io.dropout,
            "wifi_name": get_wifi_name()  # 添加WiFi名称
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
            "dropout": 0,
            "wifi_name": None  # 添加WiFi名称默认值
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
                    # 打印调试信息，帮助诊断问题
                    print(f"Processing address: {addr.address}, family: {addr.family}")
                    
                    # 先检查地址族获取IP地址，这是最可靠的方式
                    # 使用数值比较而不是常量，确保跨平台兼容性
                    if addr.family == 2:  # psutil.AF_INET (IPv4)
                        # 检查broadcast属性是否存在，避免AttributeError
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": getattr(addr, 'broadcast', None)
                        })
                    elif addr.family == 23:  # psutil.AF_INET6 (IPv6)
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask
                        })
                    # 同时检查地址格式，确保不会错过任何IP地址
                    elif '.' in addr.address and not ':' in addr.address:  # 可能是IPv4地址
                        # 尝试解析为IPv4地址
                        ip_parts = addr.address.split('.')
                        if len(ip_parts) == 4 and all(part.isdigit() for part in ip_parts):
                            ip_addresses.append({
                                "ip": addr.address,
                                "netmask": getattr(addr, 'netmask', ''),
                                "broadcast": getattr(addr, 'broadcast', None)
                            })
                    elif ':' in addr.address:  # 可能是IPv6地址
                        # 尝试解析为IPv6地址
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": getattr(addr, 'netmask', '')
                        })
                    # 检查是否为MAC地址
                    elif len(addr.address) in [17, 14] and (':' in addr.address or '-' in addr.address):
                        mac_address = addr.address
                    # 最后检查AF_LINK，确保跨平台兼容性
                    elif addr.family == psutil.AF_LINK or addr.family == -1:  # -1是Windows上的AF_LINK
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

async def capture_network_packets(interface=None, duration=60, output_file="network_capture.log"):
    """捕获网络数据包并异步写入日志"""
    if pcap is None:
        return {"error": "python-pcap library not installed"}
    
    if aiofiles is None:
        return {"error": "aiofiles library not installed"}
    
    try:
        # 如果没有指定接口，使用默认接口
        if not interface:
            interfaces = psutil.net_if_addrs()
            # 选择第一个非loopback接口
            for iface in interfaces:
                if iface != "lo" and iface != "Loopback":
                    interface = iface
                    break
            if not interface:
                return {"error": "No network interface found"}
        
        # 打开网络接口进行抓包
        pc = pcap.pcap(interface)
        
        # 过滤关键端口（80/443/22/23）
        pc.setfilter("port 80 or port 443 or port 22 or port 23")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_file)) or '.', exist_ok=True)
        
        # 打开输出文件
        async with aiofiles.open(output_file, 'a') as f:
            start_time = time.time()
            packet_count = 0
            
            # 写入开始信息
            await f.write(f"\n=== Network capture started on {interface} at {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            
            # 捕获数据包
            for timestamp, packet in pc:
                if time.time() - start_time > duration:
                    break
                
                packet_count += 1
                # 写入数据包信息
                await f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}] Packet #{packet_count}, Length: {len(packet)}\n")
            
            # 写入结束信息
            await f.write(f"=== Network capture ended at {time.strftime('%Y-%m-%d %H:%M:%S')}, Captured {packet_count} packets ===\n")
        
        return {
            "success": True,
            "interface": interface,
            "duration": duration,
            "packet_count": packet_count,
            "output_file": output_file
        }
    except Exception as e:
        print(f"Error capturing network packets: {e}")
        return {"error": str(e)}

async def get_network_logs(log_file="network_capture.log", lines=100):
    """获取网络日志"""
    if aiofiles is None:
        return {"error": "aiofiles library not installed"}
    
    try:
        if not os.path.exists(log_file):
            return {"error": "Log file not found"}
        
        async with aiofiles.open(log_file, 'r') as f:
            # 读取文件的最后N行
            log_lines = []
            async for line in f:
                log_lines.append(line.strip())
            
            # 返回最后N行
            return {
                "success": True,
                "logs": log_lines[-lines:],
                "total_lines": len(log_lines),
                "shown_lines": min(lines, len(log_lines))
            }
    except Exception as e:
        print(f"Error getting network logs: {e}")
        return {"error": str(e)}
