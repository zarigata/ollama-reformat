#!/usr/bin/env python3
"""
Ollama Fine-Tuning Studio - One-Click Startup Script
Automatically sets up Python virtual environment, installs dependencies,
and runs both backend and frontend servers.
"""

import os
import sys
import subprocess
import platform
import time
import signal
import threading
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class OllamaStudio:
    def __init__(self):
        self.project_root = Path(__file__).parent.absolute()
        self.venv_path = self.project_root / "venv"
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def print_header(self):
        print(f"{Colors.HEADER}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                Ollama Fine-Tuning Studio                    ║")
        print("║                  One-Click Startup                         ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
    def check_python_version(self):
        """Check if Python 3.11+ is available"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            print(f"{Colors.FAIL}❌ Python 3.11+ is required. Current version: {version.major}.{version.minor}{Colors.ENDC}")
            return False
        print(f"{Colors.OKGREEN}✅ Python {version.major}.{version.minor} detected{Colors.ENDC}")
        return True
        
    def check_node_version(self):
        """Check if Node.js is available"""
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"{Colors.OKGREEN}✅ Node.js {version} detected{Colors.ENDC}")
                return True
        except FileNotFoundError:
            pass
        print(f"{Colors.FAIL}❌ Node.js is required but not found{Colors.ENDC}")
        return False
        
    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get("http://localhost:11434", timeout=5)
            if response.status_code == 200:
                print(f"{Colors.OKGREEN}✅ Ollama is running{Colors.ENDC}")
                return True
        except:
            pass
        print(f"{Colors.WARNING}⚠️  Ollama not detected. Please start Ollama first:{Colors.ENDC}")
        print(f"{Colors.WARNING}   Run: ollama serve{Colors.ENDC}")
        return False
        
    def create_venv(self):
        """Create Python virtual environment"""
        if self.venv_path.exists():
            print(f"{Colors.OKGREEN}✅ Virtual environment already exists{Colors.ENDC}")
            return True
            
        print(f"{Colors.OKBLUE}📦 Creating Python virtual environment...{Colors.ENDC}")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            print(f"{Colors.OKGREEN}✅ Virtual environment created{Colors.ENDC}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}❌ Failed to create virtual environment: {e}{Colors.ENDC}")
            return False
            
    def get_venv_python(self):
        """Get the correct Python executable path for the virtual environment"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
            
    def get_venv_pip(self):
        """Get the correct pip executable path for the virtual environment"""
        if platform.system() == "Windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
            
    def install_python_deps(self):
        """Install Python dependencies"""
        print(f"{Colors.OKBLUE}📦 Installing Python dependencies...{Colors.ENDC}")
        pip_path = str(self.get_venv_pip())
        
        try:
            subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
            print(f"{Colors.OKGREEN}✅ Python dependencies installed{Colors.ENDC}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}❌ Failed to install Python dependencies: {e}{Colors.ENDC}")
            return False
            
    def install_node_deps(self):
        """Install Node.js dependencies"""
        print(f"{Colors.OKBLUE}📦 Installing Node.js dependencies...{Colors.ENDC}")
        try:
            subprocess.run(["npm", "install"], check=True)
            print(f"{Colors.OKGREEN}✅ Node.js dependencies installed{Colors.ENDC}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.FAIL}❌ Failed to install Node.js dependencies: {e}{Colors.ENDC}")
            return False
            
    def start_backend(self):
        """Start the FastAPI backend"""
        print(f"{Colors.OKBLUE}🚀 Starting backend server...{Colors.ENDC}")
        python_path = str(self.get_venv_python())
        
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)
        
        self.backend_process = subprocess.Popen([
            python_path, "-m", "uvicorn", "backend.main:app",
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], env=env)
        
        print(f"{Colors.OKGREEN}✅ Backend started on http://localhost:8000{Colors.ENDC}")
        
    def start_frontend(self):
        """Start the React frontend"""
        print(f"{Colors.OKBLUE}🚀 Starting frontend server...{Colors.ENDC}")
        
        self.frontend_process = subprocess.Popen([
            "npm", "run", "dev"
        ])
        
        print(f"{Colors.OKGREEN}✅ Frontend started on http://localhost:3000{Colors.ENDC}")
        
    def wait_for_services(self):
        """Wait for services to be ready"""
        print(f"{Colors.OKBLUE}⏳ Waiting for services to start...{Colors.ENDC}")
        time.sleep(5)  # Give services time to start
        
    def cleanup(self):
        """Clean up running processes"""
        print(f"{Colors.WARNING}🛑 Shutting down services...{Colors.ENDC}")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            
        print(f"{Colors.OKGREEN}✅ All services stopped{Colors.ENDC}")
        
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        self.cleanup()
        sys.exit(0)
        
    def run(self):
        """Main execution"""
        self.print_header()
        
        # Check prerequisites
        if not self.check_python_version():
            return False
        if not self.check_node_version():
            return False
        if not self.check_ollama():
            return False
            
        # Setup environment
        if not self.create_venv():
            return False
        if not self.install_python_deps():
            return False
        if not self.install_node_deps():
            return False
            
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start services
        self.start_backend()
        time.sleep(2)  # Let backend start first
        self.start_frontend()
        
        # Wait for services
        self.wait_for_services()
        
        # Display success message
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Ollama Fine-Tuning Studio is ready!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}🌐 Frontend: http://localhost:3000{Colors.ENDC}")
        print(f"{Colors.OKGREEN}🔧 Backend API: http://localhost:8000{Colors.ENDC}")
        print(f"{Colors.WARNING}📋 Press Ctrl+C to stop all services{Colors.ENDC}")
        
        # Keep the script running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

if __name__ == "__main__":
    studio = OllamaStudio()
    studio.run()
