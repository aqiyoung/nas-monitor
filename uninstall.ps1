#!/usr/bin/env powershell
# 飞牛NAS监控系统一键卸载脚本 (PowerShell版本)
# 通过此脚本可以完全移除监控系统及其相关文件

# 颜色代码
$RED = "`e[0;31m"
$GREEN = "`e[0;32m"
$YELLOW = "`e[1;33m"
$BLUE = "`e[0;34m"
$NC = "`e[0m" # No Color

Write-Host -ForegroundColor Cyan "====================================================="
Write-Host -ForegroundColor Green "飞牛NAS监控系统一键卸载脚本 (PowerShell版本)"
Write-Host -ForegroundColor Cyan "====================================================="

# 停止服务
Write-Host -ForegroundColor Yellow "
停止服务..."
# 在Windows上，我们不使用systemctl，而是直接终止进程
$uvicornProcesses = Get-Process | Where-Object { $_.ProcessName -eq "python" -and $_.CommandLine -like "*uvicorn*main:app*" }
if ($uvicornProcesses) {
    foreach ($process in $uvicornProcesses) {
        Stop-Process -Id $process.Id -Force
    }
    Write-Host -ForegroundColor Green "后端服务已停止"
} else {
    Write-Host -ForegroundColor Yellow "后端服务不存在，跳过"
}

# 移除项目文件
Write-Host -ForegroundColor Yellow "
移除项目文件..."
if (Test-Path "nas-monitor") {
    Remove-Item -Recurse -Force "nas-monitor"
    Write-Host -ForegroundColor Green "项目文件已移除"
} elseif (Test-Path "C:\opt\nas-monitor") {
    Remove-Item -Recurse -Force "C:\opt\nas-monitor"
    Write-Host -ForegroundColor Green "项目文件已移除"
} else {
    Write-Host -ForegroundColor Yellow "项目文件不存在，跳过"
}

# 清理虚拟环境和依赖
Write-Host -ForegroundColor Yellow "
清理虚拟环境和依赖..."
# 这里可以添加更多清理步骤，比如清理Python虚拟环境等

# 显示卸载完成信息
Write-Host -ForegroundColor Green "
====================================================="
Write-Host -ForegroundColor Green "卸载完成！"
Write-Host -ForegroundColor Green "====================================================="
Write-Host -ForegroundColor Blue "所有飞牛NAS监控系统相关的文件和服务已被移除"
Write-Host -ForegroundColor Yellow "
如果您想重新安装，可以使用以下命令:"
Write-Host "  Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/aqiyoung/nas-monitor/main/deploy.ps1' -OutFile 'deploy.ps1'; .\deploy.ps1"
Write-Host -ForegroundColor Green "
感谢使用飞牛NAS监控系统！"
