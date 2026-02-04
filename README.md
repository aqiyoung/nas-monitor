# NAS 监控平台

一个功能完整的 NAS 监控平台，用于监控 NAS 运行状态、网络流量、IO 运行状态和 Docker 容器运行状态。

## 版本信息

**当前版本**：v2.0.0
**发布日期**：2026-02-04

## 迭代更新记录

### v2.0.0 (2026-02-04)

**完全重构**：
- ✅ 前端框架：从 React + TypeScript 迁移到 Vue 3 + Element Plus
- ✅ 前端目录：从 `frontend/` 迁移到 `frontend-vue/`
- ✅ UI 设计：采用现代化卡片式布局，添加渐变效果和动画
- ✅ 布局优化：实现全屏显示，两边不留白
- ✅ 交互体验：添加平滑过渡动画和悬停效果

**功能增强**：
- ✅ 响应式设计：优化移动端和桌面端显示
- ✅ 登录功能：修复登录请求格式问题，支持 JSON 格式
- ✅ 系统监控：增强磁盘 S.M.A.R.T 监控
- ✅ 网络监控：添加网络数据包捕获功能
- ✅ Docker 监控：完善容器管理功能

**技术栈更新**：
- ✅ 前端：Vue 3 + TypeScript + Element Plus + ECharts
- ✅ 后端：Python FastAPI + psutil + docker-py
- ✅ 监控：Node Exporter + cAdvisor + Prometheus + InfluxDB

### v1.1.1 (2026-01-25)

**修复**：
- ✅ Logo显示问题：恢复了原始SVG logo显示
- ✅ 布局拥挤问题：添加了适当的容器类，恢复舒适的边距和间距
- ✅ SVG数据URL语法错误：修复了导致编译失败的SVG数据URL问题

### v1.1.0 (2026-01-23)

**修复**：
- ✅ Docker 依赖问题：将 docker 库的导入从模块顶部移到函数内部，添加了异常处理，确保后端服务在没有 Docker 守护进程的环境中也能正常启动

### v1.0.0 (2026-01-23)

**新增功能**：
- ✅ 用户管理系统：基于 OAuth2 和 JWT 的身份验证，支持用户的创建、编辑、删除和状态管理
- ✅ 告警系统：包括系统异常告警、Docker 异常告警、外部访问 IP 监控和 IP 地理定位
- ✅ Docker 镜像拉取功能：支持从 Docker Hub 拉取最新镜像
- ✅ 优化的数据刷新机制：减少不必要的组件重新渲染，解决容器闪烁问题
- ✅ 新增页面：优化了 Dashboard、Docker、IO、Network 和 System 页面，提高了性能和用户体验

### v0.1.0 (初始版本)

**核心功能**：
- ✅ 系统运行状态监控：CPU、内存、磁盘使用情况
- ✅ 网络流量监控：发送/接收字节数、数据包统计
- ✅ IO 运行状态监控：磁盘 IO 统计、系统 IO 总统计
- ✅ Docker 容器监控：容器列表、资源使用率、镜像列表

## 功能特性

### 1. 系统运行状态监控
- **CPU 使用率**：总使用率和每核使用率
- **内存使用情况**：物理内存和交换分区
- **磁盘使用情况**：各分区使用率
- **磁盘 S.M.A.R.T**：硬盘健康状态监控
- **系统基本信息**：主机名、操作系统、启动时间等

### 2. 网络流量监控
- **发送和接收字节数**
- **发送和接收数据包数**
- **错误和丢弃数据包统计**
- **网络接口信息**：状态、速度、IP 地址等
- **网络数据包捕获**：支持指定接口和时长的数据包捕获

### 3. IO 运行状态监控
- **磁盘 IO 统计**：读取/写入字节数、次数、时间
- **系统 IO 总统计**
- **各磁盘详细 IO 信息**

### 4. Docker 容器监控
- **容器列表**：运行状态、镜像、创建时间等
- **容器资源使用率**：CPU、内存、网络、IO
- **容器管理**：启动、停止、重启容器
- **容器日志**：查看容器运行日志
- **镜像列表**：大小、创建时间等
- **镜像拉取**：支持从 Docker Hub 拉取最新镜像

### 5. 用户管理
- **用户认证**：基于 OAuth2 和 JWT 的身份验证
- **用户管理**：创建、编辑、删除用户
- **用户状态控制**：启用/禁用用户
- **密码加密**：安全的密码存储

### 6. 告警系统
- **系统异常告警**：CPU、内存、磁盘使用率过高
- **Docker 异常告警**：容器状态变化、资源使用率过高
- **外部访问 IP 监控**：记录和告警外部访问 IP
- **IP 地理定位**：显示访问 IP 的地理位置
- **告警记录**：保存和查询告警历史
- **告警配置**：自定义告警规则

## 技术栈

- **后端**：Python FastAPI
- **前端**：Vue 3 + TypeScript + Element Plus + ECharts
- **监控库**：psutil, docker-py, pySMART
- **网络库**：python-pcap, aiofiles
- **容器化**：Docker, Docker Compose
- **监控系统**：Node Exporter, cAdvisor, Prometheus, InfluxDB
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
cd frontend-vue
npm install
npm run dev
```

### 2. Docker 部署

```bash
docker compose up -d
```

## 访问地址

- **前端监控平台**：http://localhost:3003
- **后端 API**：http://localhost:8017
- **Prometheus**：http://localhost:9090
- **Node Exporter**：http://localhost:9100
- **cAdvisor**：http://localhost:8080

## 项目结构

```
as-monitor/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── services/     # 业务逻辑
│   │   ├── core/         # 核心配置
│   │   └── models/       # 数据模型
│   ├── main.py           # 应用入口
│   ├── requirements.txt  # 依赖配置
│   └── Dockerfile        # Docker 配置
├── frontend-vue/         # 前端应用
│   ├── src/
│   │   ├── components/   # 组件
│   │   ├── views/        # 页面
│   │   ├── router/       # 路由
│   │   └── services/     # 服务
│   ├── index.html        # HTML 入口
│   ├── package.json      # 依赖配置
│   ├── Dockerfile        # Docker 配置
│   └── nginx.conf        # Nginx 配置
├── prometheus/           # Prometheus 配置
│   └── config/           # 配置文件
├── docker-compose.yml    # Docker Compose 配置
└── .github/workflows/    # GitHub Actions 工作流
```

## 页面说明

1. **仪表盘**：系统概览，显示 CPU、内存、磁盘和网络的主要指标
2. **系统状态**：详细的 CPU、内存和磁盘使用情况，包括 S.M.A.R.T 信息
3. **网络流量**：网络流量统计、接口信息和数据包捕获功能
4. **IO 状态**：磁盘和系统 IO 详细信息
5. **Docker 监控**：容器和镜像管理，支持容器操作和日志查看
6. **告警管理**：告警记录查看、告警配置和访问 IP 管理

## GitHub Actions

项目配置了 Docker 镜像构建工作流，当代码推送到 `main` 分支时，会自动构建并推送 Docker 镜像到 GitHub Container Registry。

## 许可证

MIT License
