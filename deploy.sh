#!/bin/bash
# 飞牛NAS监控系统一键部署脚本
# 通过此脚本可以快速部署完整的监控系统

# 日志文件
LOG_FILE="nas-monitor-deploy.log"

# 颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志记录函数
log() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    local message="$1"
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

echo -e "${BLUE}=====================================================${NC}"
echo -e "${GREEN}飞牛NAS监控系统一键部署脚本${NC}"
echo -e "${BLUE}=====================================================${NC}"
echo -e "${YELLOW}日志文件: $LOG_FILE${NC}"

# 初始化日志文件
echo "===============================================" > "$LOG_FILE"
echo "飞牛NAS监控系统部署日志" >> "$LOG_FILE"
echo "开始时间: $(date +"%Y-%m-%d %H:%M:%S")" >> "$LOG_FILE"
echo "===============================================" >> "$LOG_FILE"
log "开始部署飞牛NAS监控系统"

# 检查系统环境
log "检查系统环境"

# 检查是否为Debian系统
if [ ! -f /etc/debian_version ]; then
    log "错误: 此脚本仅支持Debian系统"
    echo -e "${RED}错误: 此脚本仅支持Debian系统${NC}"
    exit 1
fi

# 检查sudo权限
if ! sudo -n true 2>/dev/null; then
    log "提示: 您需要sudo权限来安装系统依赖"
    echo -e "${YELLOW}提示: 您需要sudo权限来安装系统依赖${NC}"
    log "请确保您有sudo权限，或者在运行此脚本前获取root权限"
    echo -e "${YELLOW}请确保您有sudo权限，或者在运行此脚本前获取root权限${NC}"
fi

# 检查curl是否安装
if ! command -v curl &> /dev/null; then
    log "安装curl..."
    echo -e "${YELLOW}安装curl...${NC}"
    if sudo apt update && sudo apt install -y curl; then
        log "curl安装成功"
        echo -e "${GREEN}curl安装成功${NC}"
    else
        log "curl安装失败，请手动安装后重试"
        echo -e "${RED}curl安装失败，请手动安装后重试${NC}"
    fi
else
    log "curl已安装"
    echo -e "${GREEN}curl已安装${NC}"
fi

# 检查git是否安装
if ! command -v git &> /dev/null; then
    log "安装git..."
    echo -e "${YELLOW}安装git...${NC}"
    if sudo apt update && sudo apt install -y git; then
        log "git安装成功"
        echo -e "${GREEN}git安装成功${NC}"
    else
        log "git安装失败，请手动安装后重试"
        echo -e "${RED}git安装失败，请手动安装后重试${NC}"
    fi
else
    log "git已安装"
    echo -e "${GREEN}git已安装${NC}"
fi

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    log "安装Python 3..."
    echo -e "${YELLOW}安装Python 3...${NC}"
    if sudo apt update && sudo apt install -y python3 python3-pip python3-venv; then
        log "Python 3安装成功"
        echo -e "${GREEN}Python 3安装成功${NC}"
    else
        log "Python 3安装失败，请手动安装后重试"
        echo -e "${RED}Python 3安装失败，请手动安装后重试${NC}"
    fi
else
    log "Python 3已安装"
    echo -e "${GREEN}Python 3已安装${NC}"
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    log "安装Node.js..."
    echo -e "${YELLOW}安装Node.js...${NC}"
    if curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs; then
        log "Node.js安装成功"
        echo -e "${GREEN}Node.js安装成功${NC}"
    else
        log "Node.js安装失败，请手动安装后重试"
        echo -e "${RED}Node.js安装失败，请手动安装后重试${NC}"
    fi
else
    log "Node.js已安装"
    echo -e "${GREEN}Node.js已安装${NC}"
fi

# 克隆项目
log "克隆项目代码..."
echo -e "\n${YELLOW}克隆项目代码...${NC}"
if git clone https://github.com/aqiyoung/nas-monitor.git; then
    log "项目代码克隆成功"
    echo -e "${GREEN}项目代码克隆成功${NC}"
    cd nas-monitor
    
    # 运行安装脚本
    log "运行安装脚本..."
    echo -e "\n${YELLOW}运行安装脚本...${NC}"
    if python3 install.py; then
        log "安装脚本执行成功"
        echo -e "${GREEN}安装脚本执行成功${NC}"
    else
        log "安装脚本执行失败"
        echo -e "${RED}安装脚本执行失败，请查看日志文件了解详细原因${NC}"
    fi
else
    log "项目代码克隆失败"
    echo -e "${RED}项目代码克隆失败，请查看日志文件了解详细原因${NC}"
fi

log "部署完成"
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
echo -e "\n${YELLOW}部署日志已保存到: $LOG_FILE${NC}"
echo -e "${YELLOW}如果部署失败，请查看日志文件了解详细原因${NC}"
echo -e "\n${GREEN}祝您使用愉快！${NC}"

# 记录部署结束时间
log "部署结束"
echo "===============================================" >> "$LOG_FILE"
echo "结束时间: $(date +"%Y-%m-%d %H:%M:%S")" >> "$LOG_FILE"
echo "===============================================" >> "$LOG_FILE"
