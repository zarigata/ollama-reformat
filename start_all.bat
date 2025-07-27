@echo off
title Ollama Fine-Tuning Studio - One-Click Startup
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                Ollama Fine-Tuning Studio                    ║
echo ║                  One-Click Startup                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Ollama is running
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama is not running. Please start Ollama first:
    echo    Run: ollama serve
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo 📦 Installing Python dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo ✅ Node.js dependencies installed

REM Start backend server
echo 🚀 Starting backend server...
start "Backend Server" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

REM Start frontend server
echo 🚀 Starting frontend server...
start "Frontend Server" cmd /k "npm run dev"

echo.
echo 🎉 Ollama Fine-Tuning Studio is starting...
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📋 Close these windows to stop all services
echo.
pause
