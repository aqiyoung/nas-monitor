#!/usr/bin/env python3
"""
飞牛NAS监控系统安装脚本
提供交互式命令行界面，支持Telegram和飞书机器人配置
"""

import os
import sys
import json
import argparse
import subprocess
import time
from getpass import getpass

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

# 颜色代码
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_color(text, color=Colors.OKGREEN):
    """打印带颜色的文本"""
    print(f"{color}{text}{Colors.ENDC}")

def print_header(text):
    """打印标题"""
    print_color(f"\n{text}", Colors.HEADER)
    print_color("-" * len(text), Colors.HEADER)

def print_error(text):
    """打印错误信息"""
    print_color(f"错误: {text}", Colors.FAIL)

def print_warning(text):
    """打印警告信息"""
    print_color(f"警告: {text}", Colors.WARNING)

def print_success(text):
    """打印成功信息"""
    print_color(f"成功: {text}", Colors.OKGREEN)

def run_command(cmd, cwd=None, capture_output=False):
    """运行命令"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, cwd=cwd)
            return result.returncode
    except Exception as e:
        print_error(f"运行命令失败: {e}")
        return 1

def check_system():
    """检查系统环境"""
    print_header("检查系统环境")
    
    # 检查Python
    code, stdout, stderr = run_command("python3 --version", capture_output=True)
    if code != 0:
        print_error("Python 3 未安装")
        return False
    print_success(f"Python 版本: {stdout.strip()}")
    
    # 检查Node.js
    code, stdout, stderr = run_command("node --version", capture_output=True)
    if code != 0:
        print_warning("Node.js 未安装，前端构建将跳过")
    else:
        print_success(f"Node.js 版本: {stdout.strip()}")
    
    # 检查Git
    code, stdout, stderr = run_command("git --version", capture_output=True)
    if code != 0:
        print_error("Git 未安装")
        return False
    print_success(f"Git 版本: {stdout.strip()}")
    
    return True

def setup_backend():
    """设置后端环境"""
    print_header("设置后端环境")
    
    # 创建虚拟环境
    venv_path = os.path.join(BACKEND_DIR, 'venv')
    if not os.path.exists(venv_path):
        print("创建虚拟环境...")
        # 根据操作系统选择正确的Python命令
        import platform
        if platform.system() == "Windows":
            python_cmd = "python"
        else:
            # 在Linux系统上优先使用python3
            python_cmd = "python3"
        # 捕获详细的错误信息
        code, stdout, stderr = run_command(f"{python_cmd} -m venv venv", cwd=BACKEND_DIR, capture_output=True)
        if code != 0:
            print_error("创建虚拟环境失败")
            if stdout:
                print_error(f"标准输出: {stdout}")
            if stderr:
                print_error(f"错误输出: {stderr}")
            return False
        print_success("虚拟环境创建成功")
    else:
        print_success("虚拟环境已存在")
    
    # 安装依赖
    print("安装后端依赖...")
    # 根据操作系统选择正确的pip路径
    import platform
    if platform.system() == "Windows":
        pip_path = ".\\venv\\Scripts\\pip"
    else:
        pip_path = "./venv/bin/pip"
    code = run_command(f"{pip_path} install -r requirements.txt", cwd=BACKEND_DIR)
    if code != 0:
        print_error("安装依赖失败")
        return False
    print_success("后端依赖安装成功")
    
    return True

def setup_frontend():
    """设置前端环境"""
    print_header("设置前端环境")
    
    # 检查Node.js
    code, stdout, stderr = run_command("node --version", capture_output=True)
    if code != 0:
        print_warning("Node.js 未安装，跳过前端构建")
        return True
    
    # 安装依赖
    print("安装前端依赖...")
    # 移除--production标志，安装所有依赖（包括开发环境依赖）
    code = run_command("npm install", cwd=FRONTEND_DIR)
    if code != 0:
        print_error("安装前端依赖失败")
        return False
    print_success("前端依赖安装成功")
    
    # 构建前端
    print("构建前端...")
    # 使用npx运行本地的vite，避免全局vite不存在的问题
    # 捕获详细的错误信息
    code, stdout, stderr = run_command("npx vite build", cwd=FRONTEND_DIR, capture_output=True)
    if code != 0:
        print_error("构建前端失败")
        if stdout:
            print_error(f"标准输出: {stdout}")
        if stderr:
            print_error(f"错误输出: {stderr}")
        return False
    print_success("前端构建成功")
    
    return True

def validate_telegram_token(token):
    """验证Telegram机器人token"""
    import requests
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_username = data['result'].get('username')
                print_success(f"Telegram机器人验证成功: @{bot_username}")
                return True
            else:
                print_error(f"Telegram机器人验证失败: {data.get('description')}")
                return False
        else:
            print_error(f"Telegram API 响应错误: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"验证Telegram token时发生错误: {e}")
        return False

def setup_telegram_bot():
    """设置Telegram机器人"""
    print_header("设置Telegram机器人")
    
    # 获取token
    token = getpass("请输入Telegram Bot Token: ")
    if not token:
        print_error("Token不能为空")
        return False
    
    # 验证token
    if not validate_telegram_token(token):
        return False
    
    # 获取chat_id
    chat_id = input("请输入接收消息的Chat ID: ")
    if not chat_id:
        print_error("Chat ID不能为空")
        return False
    
    # 保存配置
    channel_config = {
        "id": f"telegram_{int(time.time())}",
        "name": "Telegram通知",
        "type": "telegram",
        "enabled": True,
        "config": {
            "token": token,
            "chat_id": chat_id
        }
    }
    
    # 保存到通知渠道文件
    data_dir = os.path.join(BACKEND_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    channels_file = os.path.join(data_dir, 'notification_channels.json')
    
    if os.path.exists(channels_file):
        with open(channels_file, 'r', encoding='utf-8') as f:
            channels = json.load(f)
    else:
        channels = []
    
    channels.append(channel_config)
    
    with open(channels_file, 'w', encoding='utf-8') as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)
    
    print_success("Telegram机器人配置成功")
    return True

def setup_feishu_bot():
    """设置飞书机器人"""
    print_header("设置飞书机器人")
    
    # 获取webhook URL
    webhook_url = input("请输入飞书机器人Webhook URL: ")
    if not webhook_url:
        print_error("Webhook URL不能为空")
        return False
    
    # 保存配置
    channel_config = {
        "id": f"feishu_{int(time.time())}",
        "name": "飞书通知",
        "type": "feishu",
        "enabled": True,
        "config": {
            "webhook_url": webhook_url
        }
    }
    
    # 保存到通知渠道文件
    data_dir = os.path.join(BACKEND_DIR, 'data')
    os.makedirs(data_dir, exist_ok=True)
    channels_file = os.path.join(data_dir, 'notification_channels.json')
    
    if os.path.exists(channels_file):
        with open(channels_file, 'r', encoding='utf-8') as f:
            channels = json.load(f)
    else:
        channels = []
    
    channels.append(channel_config)
    
    with open(channels_file, 'w', encoding='utf-8') as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)
    
    print_success("飞书机器人配置成功")
    print_warning("飞书机器人将使用长链接(Long Polling)方式接收和处理消息")
    return True

def setup_bots():
    """设置机器人"""
    print_header("设置通知机器人")
    
    while True:
        print("\n请选择要设置的机器人类型:")
        print("1. Telegram (TG) 机器人")
        print("2. 飞书机器人")
        print("3. 跳过")
        
        choice = input("请输入选项编号: ").strip()
        
        if choice == '1':
            if setup_telegram_bot():
                # 询问是否继续设置其他机器人
                continue_setup = input("是否继续设置其他机器人? (y/n): ").strip()
                if continue_setup.lower() != 'y':
                    break
        elif choice == '2':
            if setup_feishu_bot():
                # 询问是否继续设置其他机器人
                continue_setup = input("是否继续设置其他机器人? (y/n): ").strip()
                if continue_setup.lower() != 'y':
                    break
        elif choice == '3':
            break
        else:
            print_error("无效选项，请重新输入")
    
    return True

def setup_system_service():
    """设置系统服务"""
    print_header("设置系统服务")
    
    # 检查是否为root用户
    if os.geteuid() != 0:
        print_warning("非root用户，跳过系统服务设置")
        return True
    
    # 创建服务文件
    service_file = "/etc/systemd/system/nas-monitor-backend.service"
    service_content = f"""
[Unit]
Description=NAS Monitor Backend Service
After=network.target

[Service]
User={os.getlogin()}
WorkingDirectory={BACKEND_DIR}
ExecStart={BACKEND_DIR}/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8017
Restart=always

[Install]
WantedBy=multi-user.target
"""
    
    try:
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # 启用服务
        run_command("systemctl enable nas-monitor-backend")
        run_command("systemctl start nas-monitor-backend")
        
        print_success("系统服务设置成功")
        return True
    except Exception as e:
        print_error(f"设置系统服务失败: {e}")
        return False

def main():
    """主函数"""
    print_color("飞牛NAS监控系统安装脚本", Colors.HEADER)
    print_color("=" * 40, Colors.HEADER)
    
    # 检查系统环境
    if not check_system():
        print_error("系统环境检查失败，退出安装")
        return 1
    
    # 设置后端
    if not setup_backend():
        print_error("后端设置失败，退出安装")
        return 1
    
    # 设置前端
    if not setup_frontend():
        print_error("前端设置失败，退出安装")
        return 1
    
    # 设置机器人
    if not setup_bots():
        print_error("机器人设置失败，退出安装")
        return 1
    
    # 设置系统服务
    setup_system_service()
    
    print_color("\n安装完成！", Colors.OKGREEN)
    print_color("=" * 40, Colors.HEADER)
    print("后端服务地址: http://localhost:8017")
    print("前端访问地址: http://localhost")
    print("\n使用以下命令管理服务:")
    print("  sudo systemctl start nas-monitor-backend   # 启动服务")
    print("  sudo systemctl stop nas-monitor-backend    # 停止服务")
    print("  sudo systemctl restart nas-monitor-backend # 重启服务")
    print("  sudo systemctl status nas-monitor-backend  # 查看状态")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
