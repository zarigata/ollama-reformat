#!/usr/bin/env python3
"""
Ollama LLM Reformat 2 - Advanced Fine-Tuning Platform
Main entry point for the Gradio-based interface
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.interface.main_interface import create_interface
from src.core.hardware_detector import HardwareDetector

def main():
    """Main entry point for the application"""
    print("🚀 Starting Ollama LLM Reformat 2 - Fine-Tuning Platform")
    
    # Detect hardware capabilities
    hardware = HardwareDetector()
    hardware.print_specs()
    
    # Create and launch interface
    interface = create_interface()
    
    print(f"\n📱 Opening Gradio interface...")
    print(f"🔗 Local URL: http://localhost:7860")
    print(f"🔧 Hardware: {hardware.device.upper()}")
    print(f"⚡ Threads: {hardware.threads}")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        quiet=False,
        show_error=True
    )

if __name__ == "__main__":
    main()
