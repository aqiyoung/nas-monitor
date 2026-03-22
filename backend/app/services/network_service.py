import psutil
import platform
import logging

logger = logging.getLogger("nas-monitor.network")

try:
    import pcap
except ImportError:
    logger.warning("python-pcap library not installed. Network packet capture will be disabled.")
    pcap = None

try:
    import aiofiles
except ImportError:
    logger.warning("aiofiles library not installed. Asynchronous file operations will be disabled.")
    aiofiles = None

import asyncio
import time
import os


def get_wifi_name():
    """获取当前连接的WiFi名称"""
    system = platform.system()
    try:
        if system == "Windows":
            import subprocess
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=False,
                check=True,
            )
            try:
                output = result.stdout.decode("gbk")
            except UnicodeDecodeError:
                output = result.stdout.decode("latin-1")

            for line in output.splitlines():
                if "SSID" in line and ":" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        ssid = parts[1].strip()
                        if ssid and ssid != "无":
                            return ssid

        elif system == "Darwin":
            import subprocess
            result = subprocess.run(
                ["networksetup", "-getairportnetwork", "en0"],
                capture_output=True,
                text=True,
                check=True,
            )
            if "Current Wi-Fi Network:" in result.stdout:
                return result.stdout.split(":")[1].strip()

        elif system == "Linux":
            import subprocess
            commands = [
                ["iwgetid", "-r"],
                ["nmcli", "--get-values", "SSID", "device", "wifi", "list", "--active"],
                ["iw", "dev", "wlan0", "link"],
            ]
            for cmd in commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                    ssid = result.stdout.strip()
                    if ssid and ssid != "off/any":
                        return ssid
                except Exception:
                    continue
    except Exception as e:
        logger.error(f"Error getting WiFi name: {e}")

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
            "wifi_name": get_wifi_name(),
        }
    except Exception as e:
        logger.error(f"Error getting network traffic: {e}")
        return {
            "bytes_sent": 0, "bytes_recv": 0,
            "packets_sent": 0, "packets_recv": 0,
            "errin": 0, "errout": 0, "dropin": 0, "dropout": 0,
            "wifi_name": None,
        }


def get_network_interfaces():
    """获取网络接口信息"""
    interfaces = []
    try:
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()

        for interface_name, addresses in net_if_addrs.items():
            interface_stats = net_if_stats.get(interface_name)
            if not interface_stats:
                continue

            ip_addresses = []
            mac_address = None

            for addr in addresses:
                try:
                    if addr.family == 2:  # IPv4
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask,
                            "broadcast": getattr(addr, "broadcast", None),
                        })
                    elif addr.family == 23:  # IPv6
                        ip_addresses.append({
                            "ip": addr.address,
                            "netmask": addr.netmask,
                        })
                    elif addr.family in (psutil.AF_LINK, -1):  # MAC
                        mac_address = addr.address
                except Exception as e:
                    logger.error(f"Error processing address {addr}: {e}")
                    continue

            interfaces.append({
                "name": interface_name,
                "mac_address": mac_address,
                "ip_addresses": ip_addresses,
                "is_up": interface_stats.isup,
                "speed": interface_stats.speed,
                "mtu": interface_stats.mtu,
            })
    except Exception as e:
        logger.error(f"Error getting network interfaces: {e}")

    return interfaces


async def capture_network_packets(interface=None, duration=60, output_file="network_capture.log"):
    """捕获网络数据包并异步写入日志"""
    if pcap is None:
        return {"error": "python-pcap library not installed"}
    if aiofiles is None:
        return {"error": "aiofiles library not installed"}

    try:
        if not interface:
            interfaces = psutil.net_if_addrs()
            for iface in interfaces:
                if iface not in ("lo", "Loopback"):
                    interface = iface
                    break
            if not interface:
                return {"error": "No network interface found"}

        pc = pcap.pcap(interface)
        pc.setfilter("port 80 or port 443 or port 22 or port 23")

        os.makedirs(os.path.dirname(os.path.abspath(output_file)) or ".", exist_ok=True)

        async with aiofiles.open(output_file, "a") as f:
            start_time = time.time()
            packet_count = 0

            await f.write(f"\n=== Network capture started on {interface} at {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")

            for timestamp, packet in pc:
                if time.time() - start_time > duration:
                    break
                packet_count += 1
                await f.write(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))}] "
                    f"Packet #{packet_count}, Length: {len(packet)}\n"
                )

            await f.write(
                f"=== Network capture ended at {time.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Captured {packet_count} packets ===\n"
            )

        return {
            "success": True,
            "interface": interface,
            "duration": duration,
            "packet_count": packet_count,
            "output_file": output_file,
        }
    except Exception as e:
        logger.error(f"Error capturing network packets: {e}")
        return {"error": str(e)}


async def get_network_logs(log_file="network_capture.log", lines=100):
    """获取网络日志"""
    if aiofiles is None:
        return {"error": "aiofiles library not installed"}

    try:
        if not os.path.exists(log_file):
            return {"error": "Log file not found"}

        async with aiofiles.open(log_file, "r") as f:
            log_lines = []
            async for line in f:
                log_lines.append(line.strip())

            return {
                "success": True,
                "logs": log_lines[-lines:],
                "total_lines": len(log_lines),
                "shown_lines": min(lines, len(log_lines)),
            }
    except Exception as e:
        logger.error(f"Error getting network logs: {e}")
        return {"error": str(e)}
