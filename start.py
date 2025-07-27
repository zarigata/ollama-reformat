#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
One Ring AI Platform - Ollama Model Fine-Tuning UI
Startup script that handles environment setup, dependencies, and server launch.
"""

import os
import sys
import subprocess
import platform
import time
import venv
import argparse
import shutil
from pathlib import Path
import importlib.util
import json
import re
import logging
from typing import List, Dict, Any, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("start")

# Constants
REQUIRED_PYTHON_VERSION = (3, 11)
VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"
PACKAGE_DIRS = ["src", "src/api", "src/models", "src/ui", "src/utils", "src/data"]
CONFIG_DIR = "config"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
DATA_DIR = "data"

# Windows-specific constants
OLLAMA_WINDOWS_PATH = os.path.expanduser("~\\AppData\\Local\\ollama\\ollama.exe")

def check_python_version() -> bool:
    """Check if the Python version meets the requirements."""
    current_version = sys.version_info[:2]
    if current_version < REQUIRED_PYTHON_VERSION:
        logger.error(
            f"Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} or higher is required. "
            f"You're using Python {current_version[0]}.{current_version[1]}."
        )
        return False
    return True

def setup_virtual_environment(force: bool = False) -> bool:
    """Set up a virtual environment if it doesn't exist or if forced."""
    venv_path = Path(VENV_DIR)
    
    # Check if venv already exists
    if venv_path.exists() and not force:
        logger.info(f"Virtual environment already exists at {venv_path}")
        return True
    
    # Remove existing venv if force is True
    if venv_path.exists() and force:
        logger.info(f"Removing existing virtual environment at {venv_path}")
        shutil.rmtree(venv_path)
    
    # Create new virtual environment
    logger.info(f"Creating virtual environment at {venv_path}")
    try:
        venv.create(venv_path, with_pip=True)
        logger.info("Virtual environment created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create virtual environment: {e}")
        return False

def get_venv_python() -> str:
    """Get the path to the Python executable in the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def get_venv_pip() -> str:
    """Get the path to the pip executable in the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")

def install_dependencies() -> bool:
    """Install dependencies from requirements.txt."""
    if not os.path.exists(REQUIREMENTS_FILE):
        logger.warning(f"{REQUIREMENTS_FILE} not found, creating with default dependencies")
        create_requirements_file()
    
    pip_path = get_venv_pip()
    logger.info("Installing dependencies...")
    
    # Try different installation methods in case of failures
    methods = [
        [pip_path, "install", "-r", REQUIREMENTS_FILE],
        [pip_path, "install", "--no-cache-dir", "-r", REQUIREMENTS_FILE],
        [pip_path, "install", "--no-cache-dir", "--use-deprecated=legacy-resolver", "-r", REQUIREMENTS_FILE]
    ]
    
    for method in methods:
        try:
            subprocess.run(method, check=True)
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            logger.warning(f"Failed to install dependencies with {' '.join(method)}")
    
    logger.error("All dependency installation methods failed")
    return False

def create_requirements_file() -> None:
    """Create a requirements.txt file with default dependencies."""
    with open(REQUIREMENTS_FILE, "w") as f:
        f.write("""# Web framework
fastapi==0.104.1
uvicorn==0.23.2

# Frontend
jinja2==3.1.2
aiofiles==23.2.1

# Data processing
numpy==1.26.0
pandas==2.1.1
pydantic==2.4.2

# PDF processing
PyPDF2==3.0.1
pdfminer.six==20221105

# Ollama integration
requests==2.31.0
websockets==11.0.3

# Hardware detection
py-cpuinfo==9.0.0
psutil==5.9.6
GPUtil==1.4.0

# Utilities
python-dotenv==1.0.0
tqdm==4.66.1
colorama==0.4.6
""")

def create_package_structure() -> None:
    """Create the package directory structure if it doesn't exist."""
    for directory in PACKAGE_DIRS + [CONFIG_DIR, STATIC_DIR, TEMPLATES_DIR, DATA_DIR]:
        os.makedirs(directory, exist_ok=True)
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file) and "static" not in directory and "templates" not in directory and "data" not in directory:
            with open(init_file, "w") as f:
                f.write(f'"""One Ring AI Platform - {directory} package."""\n')

def start_ollama_server() -> bool:
    """Start the Ollama server if not already running (Windows only)."""
    if platform.system() != "Windows":
        logger.info("Ollama server auto-start is only supported on Windows")
        return True
    
    if not os.path.exists(OLLAMA_WINDOWS_PATH):
        logger.warning(f"Ollama executable not found at {OLLAMA_WINDOWS_PATH}")
        logger.warning("Please install Ollama from https://ollama.com/download")
        return False
    
    # Check if Ollama is already running by trying to connect to its API
    import requests
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            logger.info("Ollama server is already running")
            return True
    except:
        pass
    
    # Start Ollama server
    logger.info("Starting Ollama server...")
    try:
        # Start Ollama in the background
        subprocess.Popen([OLLAMA_WINDOWS_PATH, "serve"], 
                         creationflags=subprocess.CREATE_NO_WINDOW)
        
        # Wait for Ollama to start
        max_retries = 10
        for i in range(max_retries):
            try:
                time.sleep(1)
                response = requests.get("http://localhost:11434/api/version", timeout=2)
                if response.status_code == 200:
                    logger.info("Ollama server started successfully")
                    return True
            except:
                if i < max_retries - 1:
                    logger.info(f"Waiting for Ollama server to start ({i+1}/{max_retries})...")
                else:
                    logger.error("Failed to start Ollama server")
                    return False
    except Exception as e:
        logger.error(f"Error starting Ollama server: {e}")
        return False

def detect_hardware() -> Dict[str, Any]:
    """Detect available hardware for AI acceleration."""
    hardware_info = {
        "cpu": {
            "available": True,
            "name": "Unknown",
            "cores": 0
        },
        "cuda": {
            "available": False,
            "devices": []
        },
        "zluda": {
            "available": False
        }
    }
    
    # Detect CPU
    try:
        import cpuinfo
        import psutil
        cpu_info = cpuinfo.get_cpu_info()
        hardware_info["cpu"]["name"] = cpu_info.get("brand_raw", "Unknown")
        hardware_info["cpu"]["cores"] = psutil.cpu_count(logical=False)
    except:
        pass
    
    # Detect CUDA
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            hardware_info["cuda"]["available"] = True
            for gpu in gpus:
                hardware_info["cuda"]["devices"].append({
                    "name": gpu.name,
                    "memory": gpu.memoryTotal
                })
    except:
        pass
    
    # Check for ZLUDA (experimental)
    # This is just a placeholder as ZLUDA detection would require more specific checks
    try:
        # Check for ZLUDA environment variables or specific files
        if os.environ.get("ZLUDA_ENABLED") or os.path.exists("/usr/local/zluda"):
            hardware_info["zluda"]["available"] = True
    except:
        pass
    
    return hardware_info

def create_config_file(hardware_info: Dict[str, Any]) -> None:
    """Create or update the configuration file with hardware information."""
    config_path = os.path.join(CONFIG_DIR, "config.json")
    config = {}
    
    # Load existing config if it exists
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except:
            pass
    
    # Update config with hardware info
    config["hardware"] = hardware_info
    config["github"] = "madebyzarigata"
    
    # Save updated config
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def start_server() -> None:
    """Start the FastAPI server using uvicorn."""
    python_path = get_venv_python()
    
    # Check if the main application file exists
    app_file = "src/api/app.py"
    if not os.path.exists(app_file):
        logger.warning(f"{app_file} not found, creating it")
        create_app_file()
    
    # Start the server
    logger.info("Starting the server...")
    cmd = [python_path, "-m", "uvicorn", "src.api.app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    subprocess.run(cmd)

def create_app_file() -> None:
    """Create the main FastAPI application file if it doesn't exist."""
    app_dir = os.path.dirname("src/api/app.py")
    os.makedirs(app_dir, exist_ok=True)
    
    with open("src/api/app.py", "w") as f:
        f.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"
One Ring AI Platform - FastAPI Application
Main application entry point for the Ollama Model Fine-Tuning UI.
\"\"\"

import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

# Create FastAPI app
app = FastAPI(
    title="One Ring AI Platform",
    description="Ollama Model Fine-Tuning UI",
    version="0.1.0"
)

# Set up templates and static files
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Load configuration
def load_config():
    config_path = BASE_DIR / "config" / "config.json"
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

# Routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config = load_config()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "config": config}
    )

# API routes will be added here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
""")

def create_readme() -> None:
    """Create a README.md file with project information."""
    with open("README.md", "w") as f:
        f.write("""# One Ring AI Platform - Ollama Model Fine-Tuning UI

A modern web interface for fine-tuning Ollama models with advanced features including jailbreak prompt integration, data import, and general fine-tuning capabilities.

## Features

- **Model Management**: View installed models, popular models, and search/download from Ollama website
- **Hardware Detection**: Automatic detection of CUDA, CPU, or ZLUDA for optimal performance
- **Jailbreak Integration**: Search and apply the latest jailbreak prompts
- **Data Import**: Import data from PDFs and other sources for fine-tuning
- **General Fine-Tuning**: Grade and improve models with iterative fine-tuning

## Requirements

- Python 3.11 or higher
- Ollama installed on your system

## Quick Start

1. Clone this repository:
   ```
   git clone https://github.com/madebyzarigata/ollama-reformat-2.git
   cd ollama-reformat-2
   ```

2. Run the startup script:
   ```
   py -3.11 start.py
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Options

- `--force-venv`: Force recreation of the virtual environment
- `--no-server`: Set up the environment but don't start the server

## Troubleshooting

- **Ollama Not Found**: Ensure Ollama is installed from https://ollama.com/download
- **Dependency Issues**: Try running with `--force-venv` to recreate the environment
- **Hardware Detection**: If hardware is not properly detected, check the config file in `config/config.json`

## License

MIT

## Author

Made by Zarigata
""")

def create_gitignore() -> None:
    """Create a .gitignore file with common Python patterns."""
    with open(".gitignore", "w") as f:
        f.write("""# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db

# Project specific
config/config.json
data/user_data/
""")

def main() -> None:
    """Main entry point for the startup script."""
    parser = argparse.ArgumentParser(description="One Ring AI Platform - Startup Script")
    parser.add_argument("--force-venv", action="store_true", help="Force recreation of virtual environment")
    parser.add_argument("--no-server", action="store_true", help="Don't start the server after setup")
    args = parser.parse_args()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment(args.force_venv):
        sys.exit(1)
    
    # Create package structure
    create_package_structure()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create README and .gitignore
    create_readme()
    create_gitignore()
    
    # Start Ollama server (Windows only)
    start_ollama_server()
    
    # Detect hardware
    hardware_info = detect_hardware()
    create_config_file(hardware_info)
    
    # Start the server unless --no-server is specified
    if not args.no_server:
        start_server()
    else:
        logger.info("Setup complete. Run 'py start.py' to start the server.")

if __name__ == "__main__":
    main()
