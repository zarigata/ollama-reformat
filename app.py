#!/usr/bin/env python3
"""
Hugging Face Model Fine-Tuning UI
A modern Gradio-based interface for fine-tuning Hugging Face models compatible with Ollama
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.hardware_detector import HardwareDetector
from src.model_manager import ModelManager
from src.ui.main_interface import create_gradio_interface
from src.config import Config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('hf_finetune.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Hugging Face Fine-Tuning UI")
        
        # Initialize configuration
        config = Config()
        
        # Detect hardware capabilities
        hardware = HardwareDetector()
        hardware_info = hardware.detect_hardware()
        logger.info(f"Hardware detected: {hardware_info}")
        
        # Initialize model manager
        model_manager = ModelManager(config, hardware_info)
        
        # Create and launch Gradio interface
        interface = create_gradio_interface(model_manager, hardware_info)
        
        logger.info("Launching Gradio interface...")
        interface.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            inbrowser=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise

if __name__ == "__main__":
    main()
