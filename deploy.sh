#!/bin/bash
# 飞牛NAS监控系统一键部署脚本
# 通过此脚本可以快速部署完整的监控系统

# 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${GREEN}飞牛NAS监控系统一键部署脚本${NC}"
echo -e "${BLUE}=====================================================${NC}"

# 检查系统环境
echo -e "\n${YELLOW}检查系统环境...${NC}"

# 检查是否为Debian系统
if [ ! -f /etc/debian_version ]; then
    echo -e "${RED}错误: 此脚本仅支持Debian系统${NC}"
    exit 1
fi

# 检查curl是否安装
if ! command -v curl &> /dev/null; then
    echo -e "${YELLOW}安装curl...${NC}"
    sudo apt update && sudo apt install -y curl
fi

# 检查git是否安装
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}安装git...${NC}"
    sudo apt update && sudo apt install -y git
fi

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}安装Python 3...${NC}"
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}安装Node.js...${NC}"
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
fi

# 克隆项目
echo -e "\n${YELLOW}克隆项目代码...${NC}"
git clone https://github.com/aqiyoung/nas-monitor.git
cd nas-monitor

# 运行安装脚本
echo -e "\n${YELLOW}运行安装脚本...${NC}"
python3 install.py

echo -e "\n${GREEN}=====================================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo -e "${BLUE}后端服务地址: http://localhost:8017${NC}"
echo -e "${BLUE}前端访问地址: http://localhost${NC}"
echo -e "\n${YELLOW}使用以下命令管理服务:${NC}"
echo -e "  sudo systemctl start nas-monitor-backend   # 启动服务"
echo -e "  sudo systemctl stop nas-monitor-backend    # 停止服务"
echo -e "  sudo systemctl restart nas-monitor-backend # 重启服务"
echo -e "  sudo systemctl status nas-monitor-backend  # 查看状态"
echo -e "\n${GREEN}祝您使用愉快！${NC}"
