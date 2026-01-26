FROM python:3.10-slim

WORKDIR /app

# 安装curl用于健康检查
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有文件，但排除data目录（该目录会在运行时挂载）
COPY . .

# 确保数据目录存在
RUN mkdir -p /app/data

EXPOSE 8017

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8017"]
