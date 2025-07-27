#!/usr/bin/env python3
"""
Ollama Reformat 2 - Complete Setup and Launch Script
Creates VENV, installs dependencies, and launches the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print startup banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    OLLAMA REFORMAT 2                        ║
║         Advanced LLM Fine-Tuning Platform                   ║
║                                                              ║
║        🚀 Creating VENV & Installing Dependencies           ║
║        ⚙️  Configuring Environment                          ║
║        🎯 Launching Application                             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")

def create_venv(venv_path: Path) -> bool:
    """Create virtual environment"""
    print(f"📁 Creating virtual environment at: {venv_path}")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                      check=True, capture_output=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_venv_python(venv_path: Path) -> str:
    """Get Python executable path for virtual environment"""
    if platform.system() == "Windows":
        return str(venv_path / "Scripts" / "python.exe")
    else:
        return str(venv_path / "bin" / "python")

def get_venv_pip(venv_path: Path) -> str:
    """Get pip executable path for virtual environment"""
    if platform.system() == "Windows":
        return str(venv_path / "Scripts" / "pip.exe")
    else:
        return str(venv_path / "bin" / "pip")

def install_dependencies(venv_python: str, venv_pip: str) -> bool:
    """Install all required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([venv_pip, "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        requirements_file = Path(__file__).parent / "requirements.txt"
        if requirements_file.exists():
            print("📋 Installing from requirements.txt...")
            subprocess.run([venv_pip, "install", "-r", str(requirements_file)], 
                          check=True, capture_output=True)
        else:
            print("📋 Installing individual packages...")
            packages = [
                "torch", "transformers", "peft", "bitsandbytes", 
                "gradio", "ollama", "PyPDF2", "Pillow", "pytesseract",
                "numpy", "pandas", "scikit-learn", "tqdm", "psutil", 
                "requests", "beautifulsoup4"
            ]
            
            for package in packages:
                print(f"   Installing {package}...")
                subprocess.run([venv_pip, "install", package], 
                              check=True, capture_output=True)
        
        print("✅ All dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_ollama_installation():
    """Check if Ollama is installed"""
    try:
        subprocess.run(["ollama", "--version"], 
                      check=True, capture_output=True)
        print("✅ Ollama is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Ollama not found. Please install from: https://ollama.ai")
        return False

def launch_application(venv_python: str):
    """Launch the main application"""
    print("🚀 Launching Ollama Reformat 2...")
    
    try:
        # Try to use the enhanced interface first
        enhanced_main = Path(__file__).parent / "main_enhanced.py"
        if enhanced_main.exists():
            subprocess.run([venv_python, str(enhanced_main)])
        else:
            # Fallback to simple interface
            subprocess.run([venv_python, "main_simple.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")

def main():
    """Main setup and launch function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Get project directory
    project_dir = Path(__file__).parent
    venv_path = project_dir / "venv"
    
    # Check if venv already exists
    if venv_path.exists():
        print("📁 Virtual environment already exists")
        reinstall = input("🔄 Reinstall dependencies? (y/N): ").lower().strip() == 'y'
    else:
        reinstall = True
        if not create_venv(venv_path):
            sys.exit(1)
    
    # Get venv paths
    venv_python = get_venv_python(venv_path)
    venv_pip = get_venv_pip(venv_path)
    
    # Install dependencies if needed
    if reinstall:
        if not install_dependencies(venv_python, venv_pip):
            print("❌ Setup failed. Please check your internet connection and try again.")
            sys.exit(1)
    
    # Check Ollama
    check_ollama_installation()
    
    # Launch application
    print("\n" + "="*60)
    print("🎉 Setup Complete! Starting Ollama Reformat 2...")
    print("="*60)
    launch_application(venv_python)

if __name__ == "__main__":
    main()
