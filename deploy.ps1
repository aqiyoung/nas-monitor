# Feiniu NAS Monitor Deployment Script (PowerShell Version)
# This script allows you to quickly deploy the complete monitoring system

# 日志文件
$LOG_FILE = "nas-monitor-deploy.log"

# 日志记录函数
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Output $logMessage | Tee-Object -FilePath $LOG_FILE -Append
}

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Host "=====================================================" -ForegroundColor Red
    Write-Host "警告: 请以管理员身份运行此脚本" -ForegroundColor Red
    Write-Host "=====================================================" -ForegroundColor Red
    Write-Host "此脚本需要管理员权限来安装系统依赖和配置服务" -ForegroundColor Yellow
    Write-Host "请右键点击PowerShell图标，选择'以管理员身份运行'，然后重新执行此脚本" -ForegroundColor Yellow
    Write-Host "`n按任意键退出..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Feiniu NAS Monitor Deployment Script (PowerShell Version)" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "日志文件: $LOG_FILE" -ForegroundColor Yellow

# 初始化日志文件
"===============================================" | Out-File -FilePath $LOG_FILE -Force
"Feiniu NAS Monitor 部署日志" | Out-File -FilePath $LOG_FILE -Append
"开始时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")" | Out-File -FilePath $LOG_FILE -Append
"===============================================" | Out-File -FilePath $LOG_FILE -Append
Write-Log "开始部署 Feiniu NAS 监控系统"

# Check system environment
Write-Log "检查系统环境"
Write-Host "`nChecking system environment..." -ForegroundColor Yellow

# Check if Git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Log "安装Git..."
    Write-Host "Installing Git..." -ForegroundColor Yellow
    # Download and install Git
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\GitInstaller.exe"
    try {
        Write-Log "下载Git安装包: $gitInstallerUrl"
        Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
        Write-Log "运行Git安装程序"
        Start-Process -FilePath $gitInstallerPath -ArgumentList "/SILENT" -Wait
        Remove-Item $gitInstallerPath
        # Add Git to environment variables
        $env:PATH += ";C:\Program Files\Git\bin"
        Write-Log "Git安装成功"
        Write-Host "Git installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Git安装失败: $($_.Exception.Message)" "ERROR"
        Write-Host "Git installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Git已安装"
    Write-Host "Git is already installed" -ForegroundColor Green
}

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Log "安装Python 3..."
    Write-Host "Installing Python 3..." -ForegroundColor Yellow
    # Download and install Python
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\PythonInstaller.exe"
    try {
        Write-Log "下载Python安装包: $pythonInstallerUrl"
        Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
        Write-Log "运行Python安装程序"
        Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Remove-Item $pythonInstallerPath
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        Write-Log "Python安装成功"
        Write-Host "Python installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Python安装失败: $($_.Exception.Message)" "ERROR"
        Write-Host "Python installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Python已安装"
    Write-Host "Python is already installed" -ForegroundColor Green
}

# Check if Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Log "安装Node.js..."
    Write-Host "Installing Node.js..." -ForegroundColor Yellow
    # Download and install Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v18.18.0/node-v18.18.0-x64.msi"
    $nodeInstallerPath = "$env:TEMP\NodeInstaller.msi"
    try {
        Write-Log "下载Node.js安装包: $nodeInstallerUrl"
        Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath
        Write-Log "运行Node.js安装程序"
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeInstallerPath /quiet /qn /norestart" -Wait
        Remove-Item $nodeInstallerPath
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        Write-Log "Node.js安装成功"
        Write-Host "Node.js installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Node.js安装失败: $($_.Exception.Message)" "ERROR"
        Write-Host "Node.js installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Node.js已安装"
    Write-Host "Node.js is already installed" -ForegroundColor Green
}

# Clone project
Write-Log "克隆项目代码..."
Write-Host "`nCloning project code..." -ForegroundColor Yellow
if (Test-Path "nas-monitor") {
    Write-Log "删除已存在的nas-monitor目录"
    Remove-Item -Recurse -Force "nas-monitor"
}
try {
    Write-Log "克隆项目: https://github.com/aqiyoung/nas-monitor.git"
    git clone https://github.com/aqiyoung/nas-monitor.git
    Write-Log "项目代码克隆成功"
    Write-Host "Project code cloned successfully" -ForegroundColor Green
    cd nas-monitor
    
    # Run installation script
    Write-Log "运行安装脚本..."
    Write-Host "`nRunning installation script..." -ForegroundColor Yellow
    try {
        Write-Log "执行install.py脚本"
        python install.py
        Write-Log "安装脚本执行成功"
        Write-Host "Installation script executed successfully" -ForegroundColor Green
    } catch {
        Write-Log "安装脚本执行失败: $($_.Exception.Message)" "ERROR"
        Write-Host "Installation script failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} catch {
    Write-Log "项目代码克隆失败: $($_.Exception.Message)" "ERROR"
    Write-Host "Project code cloning failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Log "部署完成"
Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Backend service address: http://localhost:8017" -ForegroundColor Blue
Write-Host "Frontend access address: http://localhost" -ForegroundColor Blue
Write-Host "`nUse the following commands to manage the service:" -ForegroundColor Yellow
Write-Host "  python -m uvicorn main:app --host 0.0.0.0 --port 8017 # Start service"
Write-Host "  Ctrl+C # Stop service"
Write-Host "`n部署日志已保存到: $LOG_FILE" -ForegroundColor Yellow
Write-Host "如果部署失败，请查看日志文件了解详细原因" -ForegroundColor Yellow
Write-Host "`nEnjoy using Feiniu NAS Monitor!" -ForegroundColor Green

# 记录部署结束时间
Write-Log "部署结束"
"===============================================" | Out-File -FilePath $LOG_FILE -Append
"结束时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")" | Out-File -FilePath $LOG_FILE -Append
"===============================================" | Out-File -FilePath $LOG_FILE -Append
