import os
import platform

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

# 测试函数
if __name__ == "__main__":
    wifi_name = get_wifi_name()
    print(f"Current WiFi name: {wifi_name}")
