# Feiniu NAS Monitor Deployment Script (PowerShell Version)
# This script allows you to quickly deploy the complete monitoring system

# Log file
$LOG_FILE = "nas-monitor-deploy.log"

# Logging function
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
    Write-Host "Warning: Please run this script as administrator" -ForegroundColor Red
    Write-Host "=====================================================" -ForegroundColor Red
    Write-Host "This script requires administrator privileges to install dependencies and configure services" -ForegroundColor Yellow
    Write-Host "Please right-click on PowerShell icon, select 'Run as administrator', and then re-execute this script" -ForegroundColor Yellow
    Write-Host "`nPress any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Feiniu NAS Monitor Deployment Script (PowerShell Version)" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Cyan
Write-Host "Log file: $LOG_FILE" -ForegroundColor Yellow

# Initialize log file
"===============================================" | Out-File -FilePath $LOG_FILE -Force
"Feiniu NAS Monitor Deployment Log" | Out-File -FilePath $LOG_FILE -Append
"Start time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")" | Out-File -FilePath $LOG_FILE -Append
"===============================================" | Out-File -FilePath $LOG_FILE -Append
Write-Log "Starting Feiniu NAS Monitor deployment"

# Check system environment
Write-Log "Checking system environment"
Write-Host "`nChecking system environment..." -ForegroundColor Yellow

# Check if Git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Log "Installing Git..."
    Write-Host "Installing Git..." -ForegroundColor Yellow
    # Download and install Git
    $gitInstallerUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstallerPath = "$env:TEMP\GitInstaller.exe"
    try {
        Write-Log "Downloading Git installer: $gitInstallerUrl"
        Invoke-WebRequest -Uri $gitInstallerUrl -OutFile $gitInstallerPath
        Write-Log "Running Git installer"
        Start-Process -FilePath $gitInstallerPath -ArgumentList "/SILENT" -Wait
        Remove-Item $gitInstallerPath
        # Add Git to environment variables
        $env:PATH += ";C:\Program Files\Git\bin"
        Write-Log "Git installed successfully"
        Write-Host "Git installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Git installation failed: $($_.Exception.Message)" "ERROR"
        Write-Host "Git installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Git is already installed"
    Write-Host "Git is already installed" -ForegroundColor Green
}

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Log "Installing Python 3..."
    Write-Host "Installing Python 3..." -ForegroundColor Yellow
    # Download and install Python
    $pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    $pythonInstallerPath = "$env:TEMP\PythonInstaller.exe"
    try {
        Write-Log "Downloading Python installer: $pythonInstallerUrl"
        Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $pythonInstallerPath
        Write-Log "Running Python installer"
        Start-Process -FilePath $pythonInstallerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
        Remove-Item $pythonInstallerPath
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        Write-Log "Python installed successfully"
        Write-Host "Python installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Python installation failed: $($_.Exception.Message)" "ERROR"
        Write-Host "Python installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Python is already installed"
    Write-Host "Python is already installed" -ForegroundColor Green
}

# Check if Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Log "Installing Node.js..."
    Write-Host "Installing Node.js..." -ForegroundColor Yellow
    # Download and install Node.js
    $nodeInstallerUrl = "https://nodejs.org/dist/v18.18.0/node-v18.18.0-x64.msi"
    $nodeInstallerPath = "$env:TEMP\NodeInstaller.msi"
    try {
        Write-Log "Downloading Node.js installer: $nodeInstallerUrl"
        Invoke-WebRequest -Uri $nodeInstallerUrl -OutFile $nodeInstallerPath
        Write-Log "Running Node.js installer"
        Start-Process -FilePath "msiexec.exe" -ArgumentList "/i $nodeInstallerPath /quiet /qn /norestart" -Wait
        Remove-Item $nodeInstallerPath
        # Refresh environment variables
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        Write-Log "Node.js installed successfully"
        Write-Host "Node.js installed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Node.js installation failed: $($_.Exception.Message)" "ERROR"
        Write-Host "Node.js installation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Log "Node.js is already installed"
    Write-Host "Node.js is already installed" -ForegroundColor Green
}

# Clone project
Write-Log "Cloning project code..."
Write-Host "`nCloning project code..." -ForegroundColor Yellow
if (Test-Path "nas-monitor") {
    Write-Log "Removing existing nas-monitor directory"
    Remove-Item -Recurse -Force "nas-monitor"
}
try {
    Write-Log "Cloning project: https://github.com/aqiyoung/nas-monitor.git"
    git clone https://github.com/aqiyoung/nas-monitor.git
    Write-Log "Project code cloned successfully"
    Write-Host "Project code cloned successfully" -ForegroundColor Green
    cd nas-monitor
    
    # Run installation script
    Write-Log "Running installation script..."
    Write-Host "`nRunning installation script..." -ForegroundColor Yellow
    try {
        Write-Log "Executing install.py script"
        python install.py
        Write-Log "Installation script executed successfully"
        Write-Host "Installation script executed successfully" -ForegroundColor Green
    } catch {
        Write-Log "Installation script failed: $($_.Exception.Message)" "ERROR"
        Write-Host "Installation script failed: $($_.Exception.Message)" -ForegroundColor Red
    }
} catch {
    Write-Log "Project code cloning failed: $($_.Exception.Message)" "ERROR"
    Write-Host "Project code cloning failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Log "Deployment completed"
Write-Host "`n=====================================================" -ForegroundColor Green
Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "Backend service address: http://localhost:8017" -ForegroundColor Blue
Write-Host "Frontend access address: http://localhost" -ForegroundColor Blue
Write-Host "`nUse the following commands to manage the service:" -ForegroundColor Yellow
Write-Host "  python -m uvicorn main:app --host 0.0.0.0 --port 8017 # Start service"
Write-Host "  Ctrl+C # Stop service"
Write-Host "`nDeployment log saved to: $LOG_FILE" -ForegroundColor Yellow
Write-Host "If deployment failed, please check the log file for details" -ForegroundColor Yellow
Write-Host "`nEnjoy using Feiniu NAS Monitor!" -ForegroundColor Green

# Record deployment end time
Write-Log "Deployment ended"
"===============================================" | Out-File -FilePath $LOG_FILE -Append
"End time: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")" | Out-File -FilePath $LOG_FILE -Append
"===============================================" | Out-File -FilePath $LOG_FILE -Append
