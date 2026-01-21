# NAS 监控平台

一个功能完整的 NAS 监控平台，用于监控 NAS 运行状态、网络流量、IO 运行状态和 Docker 容器运行状态。

## 功能特性

### 1. 系统运行状态监控
- **CPU 使用率**：总使用率和每核使用率
- **内存使用情况**：物理内存和交换分区
- **磁盘使用情况**：各分区使用率
- **系统基本信息**：主机名、操作系统、启动时间等

### 2. 网络流量监控
- **发送和接收字节数**
- **发送和接收数据包数**
- **错误和丢弃数据包统计**
- **网络接口信息**：状态、速度、IP 地址等

### 3. IO 运行状态监控
- **磁盘 IO 统计**：读取/写入字节数、次数、时间
- **系统 IO 总统计**
- **各磁盘详细 IO 信息**

### 4. Docker 容器监控
- **容器列表**：运行状态、镜像、创建时间等
- **容器资源使用率**：CPU、内存、网络、IO
- **镜像列表**：大小、创建时间等

## 技术栈

- **后端**：Python FastAPI
- **前端**：React + TypeScript + Vite
- **监控库**：psutil, docker-py
- **图表库**：Recharts
- **容器化**：Docker, Docker Compose
- **CI/CD**：GitHub Actions

## 安装和运行

### 1. 本地开发模式

#### 后端服务
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8017
```

#### 前端服务
```bash
cd frontend
npm install
npm run dev
```

### 2. Docker 部署

```bash
docker-compose up -d
```

## 访问地址

- **前端监控平台**：http://localhost:3003
- **后端 API**：http://localhost:8017

## 项目结构

```
as-monitor/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── services/     # 业务逻辑
│   │   └── models/       # 数据模型
│   ├── main.py           # 应用入口
│   ├── requirements.txt  # 依赖配置
│   └── Dockerfile        # Docker 配置
├── frontend/             # 前端应用
│   ├── src/
│   │   ├── components/   # 组件
│   │   ├── pages/        # 页面
│   │   └── services/     # 服务
│   ├── index.html        # HTML 入口
│   ├── package.json      # 依赖配置
│   ├── Dockerfile        # Docker 配置
│   └── nginx.conf        # Nginx 配置
├── docker-compose.yml    # Docker Compose 配置
└── .github/workflows/    # GitHub Actions 工作流
```

## 页面说明

1. **仪表盘**：系统概览，显示 CPU、内存、磁盘和网络的主要指标
2. **系统状态**：详细的 CPU、内存和磁盘使用情况
3. **网络流量**：网络流量统计和接口信息
4. **IO 状态**：磁盘和系统 IO 详细信息
5. **Docker 监控**：容器和镜像管理

## GitHub Actions

项目配置了 Docker 镜像构建工作流，当代码推送到 `main` 分支时，会自动构建并推送 Docker 镜像到 GitHub Container Registry。

## 许可证

MIT License
