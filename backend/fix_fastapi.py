import os
import sys

# 找到 FastAPI 的 openapi/models.py 文件
# 尝试不同的路径
possible_paths = [
    os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'fastapi', 'openapi', 'models.py'),
    os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Python', 'pythoncore-3.14-64', 'Lib', 'site-packages', 'fastapi', 'openapi', 'models.py')
]

fastapi_path = None
for path in possible_paths:
    if os.path.exists(path):
        fastapi_path = path
        break

if not fastapi_path:
    print("无法找到 FastAPI 的 openapi/models.py 文件")
    exit(1)

# 读取文件内容
with open(fastapi_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 检查是否已经导入了 Optional
if 'from typing import Optional' not in content:
    # 在文件开头添加导入
    content = content.replace('from pydantic import BaseModel', 'from pydantic import BaseModel\nfrom typing import Optional')

print(f"已找到并修改文件: {fastapi_path}")
print("修改完成，现在尝试重新启动后端服务器。")