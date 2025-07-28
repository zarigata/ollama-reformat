@echo off
title AI Model Fine-Tuning Studio - Setup & Process Manager

echo.
echo 🤖 AI Model Fine-Tuning Studio - Smart Launcher
echo ==============================================
echo.

REM Kill any existing Python processes for this app
echo 🧹 Cleaning up previous instances...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul
taskkill /f /im gradio.exe 2>nul

REM Kill any processes using port 7860 (Gradio default)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860') do (
    taskkill /f /pid %%a 2>nul
)

echo ✅ Previous instances closed

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo ✅ Virtual environment ready

REM Activate virtual environment
call venv\Scripts\activate

echo 📥 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ All dependencies installed

echo.
echo 🚀 Starting AI Model Fine-Tuning Studio...
echo Your browser will open automatically at http://localhost:7860
echo.
echo 💡 Tips:
echo    - Press Ctrl+C to stop the application
echo    - This will automatically close any previous instances
echo    - All your data and models are preserved
echo.

python app.py

echo.
echo 🛑 Application stopped
pause
