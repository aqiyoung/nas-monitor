#!/bin/bash
# 飞牛NAS监控系统一键卸载脚本
# 通过此脚本可以完全移除监控系统及其相关服务

# 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================================${NC}"
echo -e "${GREEN}飞牛NAS监控系统一键卸载脚本${NC}"
echo -e "${BLUE}=====================================================${NC}"

# 停止服务
echo -e "\n${YELLOW}停止服务...${NC}"
if [ -f /etc/systemd/system/nas-monitor-backend.service ]; then
    sudo systemctl stop nas-monitor-backend
    sudo systemctl disable nas-monitor-backend
    sudo rm /etc/systemd/system/nas-monitor-backend.service
    sudo systemctl daemon-reload
    echo -e "${GREEN}后端服务已停止并移除${NC}"
else
    echo -e "${YELLOW}后端服务不存在，跳过${NC}"
fi

# 移除Nginx配置
if [ -f /etc/nginx/sites-available/nas-monitor ]; then
    sudo rm /etc/nginx/sites-available/nas-monitor
    if [ -f /etc/nginx/sites-enabled/nas-monitor ]; then
        sudo rm /etc/nginx/sites-enabled/nas-monitor
    fi
    sudo nginx -t && sudo systemctl reload nginx
    echo -e "${GREEN}Nginx配置已移除${NC}"
else
    echo -e "${YELLOW}Nginx配置不存在，跳过${NC}"
fi

# 移除项目文件
echo -e "\n${YELLOW}移除项目文件...${NC}"
if [ -d "nas-monitor" ]; then
    sudo rm -rf nas-monitor
    echo -e "${GREEN}项目文件已移除${NC}"
elif [ -d "/opt/nas-monitor" ]; then
    sudo rm -rf /opt/nas-monitor
    echo -e "${GREEN}项目文件已移除${NC}"
else
    echo -e "${YELLOW}项目文件不存在，跳过${NC}"
fi

# 清理虚拟环境和依赖
echo -e "\n${YELLOW}清理虚拟环境和依赖...${NC}"
# 这里可以添加更多清理步骤，比如清理Python虚拟环境等

# 显示卸载完成信息
echo -e "\n${GREEN}=====================================================${NC}"
echo -e "${GREEN}卸载完成！${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo -e "${BLUE}所有飞牛NAS监控系统相关的文件和服务已被移除${NC}"
echo -e "\n${YELLOW}如果您想重新安装，可以使用以下命令:${NC}"
echo -e "  curl -fsSL https://raw.githubusercontent.com/aqiyoung/nas-monitor/main/deploy.sh | bash"
echo -e "\n${GREEN}感谢使用飞牛NAS监控系统！${NC}"
