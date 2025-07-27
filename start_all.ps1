# Ollama Fine-Tuning Studio - One-Click PowerShell Startup
# Run this script to automatically set up and start the application

Write-Host @"
╔══════════════════════════════════════════════════════════════╗
║                Ollama Fine-Tuning Studio                    ║
║                  One-Click Startup                         ║
╚══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

function Write-Status($message, $type = "INFO") {
    $colors = @{
        "INFO" = "Green"
        "WARN" = "Yellow"
        "ERROR" = "Red"
        "SUCCESS" = "Green"
    }
    Write-Host $message -ForegroundColor $colors[$type]
}

# Check prerequisites
Write-Status "🔍 Checking prerequisites..." "INFO"

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Status "❌ Python is not installed or not in PATH" "ERROR"
    Write-Status "Please install Python 3.11+ from https://python.org" "ERROR"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Status "❌ Node.js is not installed or not in PATH" "ERROR"
    Write-Status "Please install Node.js from https://nodejs.org" "ERROR"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Ollama
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 5 -UseBasicParsing
    Write-Status "✅ Ollama is running" "SUCCESS"
} catch {
    Write-Status "⚠️  Ollama is not running. Please start Ollama first:" "WARN"
    Write-Status "   Run: ollama serve" "WARN"
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
$venvPath = Join-Path $PSScriptRoot "venv"
if (-not (Test-Path $venvPath)) {
    Write-Status "📦 Creating Python virtual environment..." "INFO"
    try {
        python -m venv $venvPath
        Write-Status "✅ Virtual environment created" "SUCCESS"
    } catch {
        Write-Status "❌ Failed to create virtual environment: $_" "ERROR"
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Status "✅ Virtual environment already exists" "SUCCESS"
}

# Activate virtual environment and install Python dependencies
Write-Status "📦 Installing Python dependencies..." "INFO"
try {
    $activateScript = Join-Path $venvPath $(if ($IsWindows) { "Scripts\\activate.ps1" } else { "bin/activate" })
    . $activateScript
    
    pip install -r requirements.txt
    Write-Status "✅ Python dependencies installed" "SUCCESS"
} catch {
    Write-Status "❌ Failed to install Python dependencies: $_" "ERROR"
    Read-Host "Press Enter to exit"
    exit 1
}

# Install Node.js dependencies
Write-Status "📦 Installing Node.js dependencies..." "INFO"
try {
    npm install
    Write-Status "✅ Node.js dependencies installed" "SUCCESS"
} catch {
    Write-Status "❌ Failed to install Node.js dependencies: $_" "ERROR"
    Read-Host "Press Enter to exit"
    exit 1
}

# Start backend server
Write-Status "🚀 Starting backend server..." "INFO"
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PSScriptRoot
    . (Join-Path $using:venvPath $(if ($IsWindows) { "Scripts\\activate.ps1" } else { "bin/activate" }))
    python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend server
Write-Status "🚀 Starting frontend server..." "INFO"
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PSScriptRoot
    npm run dev
}

Write-Host ""
Write-Status "🎉 Ollama Fine-Tuning Studio is starting..." "SUCCESS"
Write-Status "🌐 Frontend: http://localhost:3000" "SUCCESS"
Write-Status "🔧 Backend: http://localhost:8000" "SUCCESS"
Write-Host ""
Write-Host "📋 Press Ctrl+C to stop all services" -ForegroundColor Yellow

# Wait for user input to stop
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Status "🛑 Shutting down services..." "WARN"
    if ($backendJob) { Stop-Job $backendJob -ErrorAction SilentlyContinue }
    if ($frontendJob) { Stop-Job $frontendJob -ErrorAction SilentlyContinue }
    Write-Status "✅ All services stopped" "SUCCESS"
}
