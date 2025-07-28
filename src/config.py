"""
Simple configuration for the Hugging Face Fine-Tuning UI
Designed for non-technical users - everything works out of the box
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from .utils.env_utils import EnvConfig, env_config

class SimpleConfig:
    """Ultra-simple configuration - works automatically"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".hf_finetune"
        self.config_dir.mkdir(exist_ok=True)
        
        # Auto-configured paths
        self.upload_dir = self.config_dir / "uploads"
        self.models_dir = self.config_dir / "models"
        self.processed_dir = self.config_dir / "processed"
        
        # Initialize environment config
        self.env_config = EnvConfig()
        # Load environment settings
        self.hf_token = self.env_config.get_hf_token() or ''
        
        # Create directories
        for dir_path in [self.upload_dir, self.models_dir, self.processed_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize config
        self.config = self.default_training_config
        self.load_config()
    
    @property
    def supported_formats(self):
        return [".pdf", ".txt", ".docx", ".csv", ".json", ".md"]
    
    @property
    def default_training_config(self):
        """Pre-configured training settings that work for most users"""
        return {
            "batch_size": 2,  # Safe for most systems
            "learning_rate": 2e-4,
            "num_epochs": 3,
            "max_seq_length": 1024,  # Conservative
            "lora_r": 16,
            "lora_alpha": 32,
        }
    
    def load_config(self):
        """Load configuration - simplified for this app"""
        # For this simple version, we'll use defaults
        pass
    
    def save_config(self):
        """Save configuration - simplified for this app"""
        # For this simple version, we'll skip saving
        pass
