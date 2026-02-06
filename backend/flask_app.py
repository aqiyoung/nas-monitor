from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 模拟用户数据
users = {
    "admin": {
        "username": "admin",
        "password": "password",
        "disabled": False
    }
}

# 模拟系统数据
system_data = {
    "hostname": "test-nas",
    "os_system": "Debian",
    "os_version": "12.0",
    "architecture": "x86_64",
    "uptime": "10d 5h 30m 15s",
    "cpu_usage": 25.5,
    "memory_usage": 45.2,
    "disk_usage": 60.8
}

# 模拟网络数据
network_data = {
    "traffic": {
        "sent": 1024000,
        "received": 2048000
    },
    "interfaces": [
        {
            "name": "eth0",
            "ip": "192.168.1.100",
            "mac": "00:11:22:33:44:55",
            "status": "up"
        }
    ]
}

# 模拟 Docker 数据
docker_data = {
    "containers": [
        {
            "id": "container1",
            "name": "nginx",
            "status": "running",
            "image": "nginx:latest"
        }
    ],
    "images": [
        {
            "id": "image1",
            "tags": ["nginx:latest"],
            "size": "133MB"
        }
    ]
}

# 模拟告警数据
alarm_data = {
    "configs": [
        {
            "id": "alarm1",
            "alarm_type": "system",
            "sub_type": "cpu_high",
            "enabled": True,
            "threshold": 80.0,
            "duration": 30,
            "severity": "warning"
        }
    ],
    "records": []
}

@app.route('/api/')
def root():
    return jsonify({"message": "NAS Monitor API is running"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy"})

# 认证相关API
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username]['password'] == password:
        return jsonify({"access_token": "test-token", "token_type": "bearer"})
    else:
        return jsonify({"detail": "用户名或密码错误"}), 401

@app.route('/api/auth/me', methods=['GET'])
def get_current_user():
    return jsonify(users["admin"])

# 系统相关API
@app.route('/api/system/status')
def get_system_status():
    return jsonify({
        "hostname": system_data['hostname'],
        "os": system_data['os_system'],
        "os_version": system_data['os_version'],
        "architecture": system_data['architecture'],
        "boot_time": "",
        "uptime": system_data['uptime']
    })

@app.route('/api/system/cpu')
def get_cpu_usage():
    return jsonify({
        "total_usage": system_data['cpu_usage'],
        "per_core_usage": [],
        "cpu_count": {
            "physical": 4,
            "logical": 8
        }
    })

@app.route('/api/system/memory')
def get_memory_usage():
    return jsonify({
        "memory": {
            "total": 8192000000,
            "available": 4096000000,
            "used": 4096000000,
            "percent": system_data['memory_usage']
        },
        "swap": {
            "total": 4096000000,
            "used": 0,
            "free": 4096000000,
            "percent": 0
        }
    })

@app.route('/api/system/disk')
def get_disk_usage():
    return jsonify([
        {
            "mountpoint": "/",
            "percent": system_data['disk_usage'],
            "used": 60000000000,
            "total": 100000000000
        }
    ])

@app.route('/api/system/disk/smart')
def get_disk_smart_info():
    return jsonify({"disks": []})

# 网络相关API
@app.route('/api/network/traffic')
def get_network_traffic():
    return jsonify({
        "bytes_sent": network_data['traffic']['sent'],
        "bytes_recv": network_data['traffic']['received'],
        "packets_sent": 0,
        "packets_recv": 0,
        "errin": 0,
        "errout": 0,
        "dropin": 0,
        "dropout": 0,
        "wifi_name": "未连接"
    })

@app.route('/api/network/interfaces')
def get_network_interfaces():
    return jsonify(network_data['interfaces'])

@app.route('/api/network/capture', methods=['POST'])
def capture_network_packets():
    return jsonify({"message": "捕获网络数据包已启动"})

@app.route('/api/network/logs')
def get_network_logs():
    return jsonify({"logs": []})

# IO相关API
@app.route('/api/io/stats')
def get_io_stats():
    return jsonify({"disks": []})

# Docker相关API
@app.route('/api/docker/containers')
def get_containers():
    return jsonify(docker_data['containers'])

@app.route('/api/docker/stats')
def get_docker_stats():
    return jsonify([
        {
            "name": "nginx",
            "cpu_usage": 0.5,
            "memory_usage": 10485760,
            "memory_limit": 104857600
        }
    ])

@app.route('/api/docker/images')
def get_docker_images():
    return jsonify(docker_data['images'])

@app.route('/api/docker/images/pull', methods=['POST'])
def pull_docker_image():
    data = request.json
    image_name = data.get('image_name')
    return jsonify({"success": True, "image_id": "image1", "tags": [image_name]})

@app.route('/api/docker/images/<image_id>', methods=['DELETE'])
def delete_docker_image(image_id):
    return jsonify({"message": "镜像删除成功"})

@app.route('/api/docker/containers/<container_id>/start', methods=['POST'])
def start_container(container_id):
    return jsonify({"message": "容器启动成功"})

@app.route('/api/docker/containers/<container_id>/stop', methods=['POST'])
def stop_container(container_id):
    return jsonify({"message": "容器停止成功"})

@app.route('/api/docker/containers/<container_id>/restart', methods=['POST'])
def restart_container(container_id):
    return jsonify({"message": "容器重启成功"})

@app.route('/api/docker/containers/<container_id>/logs')
def get_container_logs(container_id):
    return jsonify({"logs": []})

# 告警相关API
@app.route('/api/alarm/configs')
def get_alarm_configs():
    return jsonify(alarm_data['configs'])

@app.route('/api/alarm/configs/<config_id>')
def get_alarm_config(config_id):
    for config in alarm_data['configs']:
        if config['id'] == config_id:
            return jsonify(config)
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/configs', methods=['POST'])
def create_alarm_config():
    data = request.json
    data['id'] = "alarm" + str(len(alarm_data['configs']) + 1)
    alarm_data['configs'].append(data)
    return jsonify(data)

@app.route('/api/alarm/configs/<config_id>', methods=['PUT'])
def update_alarm_config(config_id):
    data = request.json
    for config in alarm_data['configs']:
        if config['id'] == config_id:
            config.update(data)
            return jsonify(config)
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/configs/<config_id>', methods=['DELETE'])
def delete_alarm_config(config_id):
    for i, config in enumerate(alarm_data['configs']):
        if config['id'] == config_id:
            alarm_data['configs'].pop(i)
            return jsonify({"message": "告警配置删除成功"})
    return jsonify({"detail": "告警配置不存在"}), 404

@app.route('/api/alarm/records')
def get_alarm_records():
    return jsonify(alarm_data['records'])

@app.route('/api/alarm/records/<record_id>')
def get_alarm_record(record_id):
    return jsonify({"detail": "告警记录不存在"}), 404

@app.route('/api/alarm/records/<record_id>', methods=['PUT'])
def update_alarm_record(record_id):
    return jsonify({"detail": "告警记录不存在"}), 404

@app.route('/api/alarm/statistics')
def get_alarm_statistics():
    return jsonify({
        "total": 0,
        "by_severity": {"info": 0, "warning": 0, "critical": 0},
        "by_type": {},
        "recent": 0
    })

@app.route('/api/alarm/detect', methods=['POST'])
def detect_alarms():
    return jsonify({"message": "告警检测已触发"})

# 用户相关API
@app.route('/api/user')
def get_users():
    return jsonify(list(users.values()))

@app.route('/api/user/<username>')
def get_user(username):
    if username in users:
        return jsonify(users[username])
    return jsonify({"detail": "用户不存在"}), 404

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if username not in users:
        users[username] = {
            "username": username,
            "password": password,
            "disabled": data.get('disabled', False)
        }
        return jsonify(users[username])
    return jsonify({"detail": "用户已存在"}), 400

@app.route('/api/user/<username>', methods=['PUT'])
def update_user(username):
    if username in users:
        data = request.json
        users[username].update(data)
        return jsonify(users[username])
    return jsonify({"detail": "用户不存在"}), 404

@app.route('/api/user/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users and username != "admin":
        del users[username]
        return jsonify({"message": "用户删除成功"})
    return jsonify({"detail": "用户不存在或无法删除"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8017, debug=True)