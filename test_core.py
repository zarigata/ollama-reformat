#!/usr/bin/env python3
"""
Test script to verify core functionality
"""

import os
import sys
import platform

def test_hardware_detection():
    """Test hardware detection"""
    print("=" * 50)
    print("🔧 HARDWARE DETECTION TEST")
    print("=" * 50)
    
    try:
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✅ PyTorch available")
        print(f"🎯 Device: {device}")
        
        if torch.cuda.is_available():
            print(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            print(f"🎮 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB")
        
    except ImportError:
        print("⚠️  PyTorch not available - will use CPU fallback")
        device = "cpu"
    
    print(f"💻 CPU Cores: {os.cpu_count()}")
    print(f"💾 Platform: {platform.system()} {platform.release()}")
    
    return device

def test_file_structure():
    """Test file structure"""
    print("\n" + "=" * 50)
    print("📁 FILE STRUCTURE TEST")
    print("=" * 50)
    
    required_files = [
        "main.py",
        "requirements.txt",
        "src/core/hardware_detector.py",
        "src/core/model_discovery.py",
        "src/core/data_processor.py",
        "src/core/prompt_unlocker.py",
        "src/interface/main_interface.py"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")

def test_ollama_availability():
    """Test Ollama availability"""
    print("\n" + "=" * 50)
    print("🦙 OLLAMA TEST")
    print("=" * 50)
    
    try:
        import subprocess
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama available: {result.stdout.strip()}")
        else:
            print("⚠️  Ollama not responding")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ Ollama not found - please install from ollama.ai")

if __name__ == "__main__":
    print("🚀 Ollama LLM Reformat 2 - Core Test")
    
    device = test_hardware_detection()
    test_file_structure()
    test_ollama_availability()
    
    print(f"\n🎉 Core test complete!")
    print(f"📱 Ready to run with device: {device}")
