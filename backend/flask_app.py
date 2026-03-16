from flask import Flask, request, jsonify
from flask_cors import CORS
import platform
import time
import psutil

app = Flask(__name__)
CORS(app)

# 模拟用户存储
users = {
    "admin": {
        "username": "admin",
        "password": "password",
        "disabled": False
    }
}

# 验证用户
def authenticate_user(username: str, password: str):
    user = users.get(username)
    if not user:
        return False
    if user["disabled"]:
        return False
    # 简单验证密码
    if password != user["password"]:
        return False
    return user

@app.route('/')
def index():
    return {'message': '运维监控中心 API is running'}

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

# 登录接口
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"detail": "请提供用户名和密码"}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate_user(username, password)
    if not user:
        return jsonify({"detail": "用户名或密码错误"}), 401
    
    # 生成简单的token
    access_token = f"token-{username}-{password}"
    return jsonify({"access_token": access_token, "token_type": "bearer"})

# 系统状态接口
@app.route('/api/system/status')
def get_system_status():
    try:
        # 获取系统基本信息
        hostname = platform.node()
        os = platform.system()
        os_version = platform.version()
        architecture = platform.architecture()[0]
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        
        # 格式化启动时间
        boot_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(boot_time))
        
        # 格式化运行时间
        uptime_str = f"{int(uptime // 3600)}小时 {int((uptime % 3600) // 60)}分钟"
        
        return jsonify({
            "hostname": hostname,
            "os": os,
            "os_version": os_version,
            "architecture": architecture,
            "boot_time": boot_time_str,
            "uptime": uptime_str
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CPU使用率接口
@app.route('/api/system/cpu')
def get_cpu_usage():
    try:
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        total_usage = sum(cpu_percent) / len(cpu_percent)
        
        # 获取CPU核心数
        cpu_count = psutil.cpu_count(logical=False)
        logical_count = psutil.cpu_count(logical=True)
        
        return jsonify({
            "total_usage": total_usage,
            "per_core_usage": cpu_percent,
            "cpu_count": {
                "physical": cpu_count,
                "logical": logical_count
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 内存使用率接口
@app.route('/api/system/memory')
def get_memory_usage():
    try:
        # 获取内存信息
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return jsonify({
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
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 磁盘使用率接口
@app.route('/api/system/disk')
def get_disk_usage():
    try:
        # 获取磁盘信息
        disk_partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
            except:
                pass
        
        return jsonify(disk_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 磁盘S.M.A.R.T信息接口
@app.route('/api/system/disk/smart')
def get_disk_smart():
    try:
        # 模拟S.M.A.R.T信息
        disk_smart = [
            {
                "device": "/dev/sda",
                "model": "Samsung SSD 860 EVO 500GB",
                "serial": "S1AXNSAF900000",
                "firmware": "RVT02B6Q",
                "interface": "SATA III",
                "size": "500GB",
                "health": "良好",
                "temperature": 35,
                "smart_attributes": [
                    {"id": 1, "name": "Raw Read Error Rate", "value": 100, "worst": 100, "threshold": 50, "raw_value": "0", "status": "OK"},
                    {"id": 5, "name": "Reallocated Sector Count", "value": 100, "worst": 100, "threshold": 10, "raw_value": "0", "status": "OK"},
                    {"id": 9, "name": "Power-On Hours", "value": 98, "worst": 98, "threshold": 0, "raw_value": "1200", "status": "OK"},
                    {"id": 12, "name": "Power Cycle Count", "value": 99, "worst": 99, "threshold": 0, "raw_value": "350", "status": "OK"},
                    {"id": 187, "name": "Reported Uncorrectable Errors", "value": 100, "worst": 100, "threshold": 0, "raw_value": "0", "status": "OK"},
                    {"id": 194, "name": "Temperature Celsius", "value": 65, "worst": 65, "threshold": 0, "raw_value": "35", "status": "OK"},
                    {"id": 197, "name": "Current Pending Sector Count", "value": 100, "worst": 100, "threshold": 0, "raw_value": "0", "status": "OK"},
                    {"id": 198, "name": "Offline Uncorrectable", "value": 100, "worst": 100, "threshold": 0, "raw_value": "0", "status": "OK"}
                ]
            }
        ]
        
        return jsonify(disk_smart)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8017)
