# Feiniu NAS Monitor Deployment Script (PowerShell Version)
# This script allows you to quickly deploy the complete monitoring system

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Feiniu NAS Monitor Deployment Script (PowerShell Version)" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan

# Check system environment
Write-Host "`nChecking system environment..." -ForegroundColor Yellow

# Check if Git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Git..." -ForegroundColor Yellow
    # Download and install Git
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\GitInstaller.exe"
    Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
    Start-Process -FilePath $gitInstallerPath -ArgumentList "/SILENT" -Wait
    Remove-Item $gitInstallerPath
    # Add Git to environment variables
    $env:PATH += ";C:\Program Files\Git\bin"
    Write-Host "Git installed successfully" -ForegroundColor Green
} else {
    Write-Host "Git is already installed" -ForegroundColor Green
}

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Python 3..." -ForegroundColor Yellow
    # Download and install Python
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\PythonInstaller.exe"
    Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
    Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $pythonInstallerPath
    # Refresh environment variables
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "Python installed successfully" -ForegroundColor Green
} else {
    Write-Host "Python is already installed" -ForegroundColor Green
}

# Check if Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Node.js..." -ForegroundColor Yellow
    # Download and install Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v18.18.0/node-v18.18.0-x64.msi"
    $nodeInstallerPath = "$env:TEMP\NodeInstaller.msi"
    Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath
    Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeInstallerPath /quiet /qn /norestart" -Wait
    Remove-Item $nodeInstallerPath
    # Refresh environment variables
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    Write-Host "Node.js installed successfully" -ForegroundColor Green
} else {
    Write-Host "Node.js is already installed" -ForegroundColor Green
}

# Clone project
Write-Host "`nCloning project code..." -ForegroundColor Yellow
if (Test-Path "nas-monitor") {
    Remove-Item -Recurse -Force "nas-monitor"
}
git clone https://github.com/aqiyoung/nas-monitor.git
cd nas-monitor

# Run installation script
Write-Host "`nRunning installation script..." -ForegroundColor Yellow
python install.py

Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Backend service address: http://localhost:8017" -ForegroundColor Blue
Write-Host "Frontend access address: http://localhost" -ForegroundColor Blue
Write-Host "`nUse the following commands to manage the service:" -ForegroundColor Yellow
Write-Host "  python -m uvicorn main:app --host 0.0.0.0 --port 8017 # Start service"
Write-Host "  Ctrl+C # Stop service"
Write-Host "`nEnjoy using Feiniu NAS Monitor!" -ForegroundColor Green
