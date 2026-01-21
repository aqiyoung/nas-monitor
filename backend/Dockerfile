FROM python:3.10-slim

WORKDIR /app

# 安装curl用于健康检查
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8017

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8017"]
