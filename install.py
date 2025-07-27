#!/usr/bin/env python3
"""
Installation script for Ollama LLM Reformat 2
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("🔧 Installing required packages...")
    
    # Install packages one by one to handle dependencies
    packages = [
        "torch",
        "transformers",
        "peft",
        "bitsandbytes",
        "gradio",
        "ollama",
        "PyPDF2",
        "Pillow",
        "numpy",
        "pandas",
        "scikit-learn",
        "tqdm",
        "psutil",
        "requests",
        "beautifulsoup4"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
    
    print("🎉 Installation complete!")

if __name__ == "__main__":
    install_requirements()
