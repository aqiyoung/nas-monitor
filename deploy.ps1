# 飞牛NAS监控系统一键部署脚本 (PowerShell版本)
# 通过此脚本可以快速部署完整的监控系统

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "飞牛NAS监控系统一键部署脚本 (PowerShell版本)" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan

# 检查系统环境
Write-Host "`n检查系统环境..." -ForegroundColor Yellow

# 检查Git是否安装
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "安装Git..." -ForegroundColor Yellow
    # 下载并安装Git
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\GitInstaller.exe"
    Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
    Start-Process -FilePath $gitInstallerPath -ArgumentList "/SILENT" -Wait
    Remove-Item $gitInstallerPath
    # 添加Git到环境变量
    $env:PATH += ";C:\Program Files\Git\bin"
    Write-Host "Git安装成功" -ForegroundColor Green
} else {
    Write-Host "Git已安装" -ForegroundColor Green
}

# 检查Python是否安装
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "安装Python 3..." -ForegroundColor Yellow
    # 下载并安装Python
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\PythonInstaller.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $pythonInstallerPath
    # 刷新环境变量
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "Python安装成功" -ForegroundColor Green
} else {
    Write-Host "Python已安装" -ForegroundColor Green
}

# 检查Node.js是否安装
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "安装Node.js..." -ForegroundColor Yellow
    # 下载并安装Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v18.18.0/node-v18.18.0-x64.msi"
    $nodeInstallerPath = "$env:TEMP\NodeInstaller.msi"
    Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeInstallerPath /quiet /qn /norestart" -Wait
    Remove-Item $nodeInstallerPath
    # 刷新环境变量
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "Node.js安装成功" -ForegroundColor Green
} else {
    Write-Host "Node.js已安装" -ForegroundColor Green
}

# 克隆项目
Write-Host "`n克隆项目代码..." -ForegroundColor Yellow
if (Test-Path "nas-monitor") {
    Remove-Item -Recurse -Force "nas-monitor"
}
git clone https://github.com/aqiyoung/nas-monitor.git
cd nas-monitor

# 运行安装脚本
Write-Host "`n运行安装脚本..." -ForegroundColor Yellow
python install.py

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "部署完成！" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "后端服务地址: http://localhost:8017" -ForegroundColor Blue
Write-Host "前端访问地址: http://localhost" -ForegroundColor Blue
Write-Host "`n使用以下命令管理服务:" -ForegroundColor Yellow
Write-Host "  python -m uvicorn main:app --host 0.0.0.0 --port 8017 # 启动服务"
Write-Host "  Ctrl+C # 停止服务"
Write-Host "`n祝您使用愉快！" -ForegroundColor Green
