"""
Environment and configuration utilities for handling HF tokens and other settings
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional

class EnvConfig:
    """Handle environment configuration and .env file management"""
    
    def __init__(self, env_path: str = ".env"):
        self.env_path = Path(env_path)
        self.config = {}
        self._load_env()
    
    def _load_env(self):
        """Load environment variables from .env file if it exists"""
        if self.env_path.exists():
            with open(self.env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            key, value = line.split('=', 1)
                            self.config[key.strip()] = value.strip().strip('"\'')
                        except ValueError:
                            continue
    
    def get(self, key: str, default: str = "") -> str:
        """Get a configuration value"""
        return os.environ.get(key) or self.config.get(key, default)
    
    def set(self, key: str, value: str, save: bool = True):
        """Set a configuration value and optionally save to .env"""
        os.environ[key] = value
        self.config[key] = value
        if save:
            self._save_env()
    
    def _save_env(self):
        """Save current configuration to .env file"""
        # Create parent directories if they don't exist
        self.env_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write all config to .env file
        with open(self.env_path, 'w') as f:
            for key, value in self.config.items():
                # Escape newlines and quotes in the value
                safe_value = str(value).replace('\n', '\\n').replace('"', '\\"')
                f.write(f'{key}="{safe_value}"\n')
    
    def get_hf_token(self) -> Optional[str]:
        """Get Hugging Face token from environment or config"""
        return self.get("HF_TOKEN")
    
    def save_hf_token(self, token: str):
        """Save Hugging Face token to environment and .env"""
        self.set("HF_TOKEN", token)

# Global instance
env_config = EnvConfig()
