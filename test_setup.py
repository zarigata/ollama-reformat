#!/usr/bin/env python3
"""
Quick test script to verify all imports work correctly
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all imports"""
    print("🔍 Testing imports...")
    
    try:
        from src.config import SimpleConfig as Config
        print("✅ Config import OK")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from src.hardware_detector import HardwareDetector
        print("✅ HardwareDetector import OK")
    except Exception as e:
        print(f"❌ HardwareDetector import failed: {e}")
        return False
    
    try:
        from src.model_manager import ModelManager
        print("✅ ModelManager import OK")
    except Exception as e:
        print(f"❌ ModelManager import failed: {e}")
        return False
    
    try:
        from src.ui.main_interface import create_gradio_interface
        print("✅ Gradio interface import OK")
    except Exception as e:
        print(f"❌ Gradio interface import failed: {e}")
        return False
    
    try:
        import gradio as gr
        print("✅ Gradio import OK")
    except Exception as e:
        print(f"❌ Gradio import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        from src.config import SimpleConfig as Config
        config = Config()
        print(f"✅ Config initialized: {config.config_dir}")
    except Exception as e:
        print(f"❌ Config failed: {e}")
        return False
    
    try:
        from src.hardware_detector import HardwareDetector
        detector = HardwareDetector()
        hardware = detector.detect_hardware()
        print(f"✅ Hardware detected: {hardware['device_name']}")
    except Exception as e:
        print(f"❌ Hardware detection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 AI Model Fine-Tuning Studio - Setup Test")
    print("=" * 50)
    
    if test_imports():
        if test_basic_functionality():
            print("\n✅ All tests passed! Ready to run app.py")
        else:
            print("\n❌ Basic functionality test failed")
    else:
        print("\n❌ Import test failed")
    
    input("\nPress Enter to continue...")
