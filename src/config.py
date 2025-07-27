""
Configuration Settings for Ollama Model Fine-Tuning UI

This module handles configuration settings for the application.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file if it exists
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "name": "Ollama Model Fine-Tuning UI",
        "version": "0.1.0",
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "secret_key": os.getenv("SECRET_KEY", "change-this-in-production"),
    },
    "server": {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "reload": os.getenv("RELOAD", "false").lower() == "true",
    },
    "ollama": {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "timeout": int(os.getenv("OLLAMA_TIMEOUT", "60")),  # seconds
    },
    "paths": {
        "models": os.getenv("MODELS_DIR", str(BASE_DIR / "models")),
        "data": os.getenv("DATA_DIR", str(BASE_DIR / "data")),
        "logs": os.getenv("LOGS_DIR", str(BASE_DIR / "logs")),
        "uploads": os.getenv("UPLOADS_DIR", str(BASE_DIR / "uploads")),
        "temp": os.getenv("TEMP_DIR", str(BASE_DIR / "temp")),
    },
    "fine_tuning": {
        "default_epochs": int(os.getenv("DEFAULT_EPOCHS", "3")),
        "default_batch_size": int(os.getenv("DEFAULT_BATCH_SIZE", "4")),
        "default_learning_rate": float(os.getenv("DEFAULT_LEARNING_RATE", "2e-5")),
        "max_upload_size_mb": int(os.getenv("MAX_UPLOAD_SIZE_MB", "100")),  # 100MB
    },
    "ui": {
        "theme": os.getenv("UI_THEME", "light"),
        "items_per_page": int(os.getenv("ITEMS_PER_PAGE", "10")),
    },
    "security": {
        "cors_origins": json.loads(os.getenv("CORS_ORIGINS", "[\"*\"]")),
        "rate_limit": os.getenv("RATE_LIMIT", "100/minute"),
    },
}

class Config:
    """Configuration class that loads settings from environment variables with defaults."""
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """Initialize configuration with defaults and override with environment variables.
        
        Args:
            config_dict: Optional dictionary to override default configuration
        """
        # Start with default configuration
        self._config = self._deep_copy(DEFAULT_CONFIG)
        
        # Update with provided dictionary if any
        if config_dict:
            self._update_config(self._config, config_dict)
        
        # Ensure all directories exist
        self._ensure_directories()
    
    def _deep_copy(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deep copy of a nested dictionary."""
        if not isinstance(config, dict):
            return config
        return {k: self._deep_copy(v) for k, v in config.items()}
    
    def _update_config(self, original: Dict[str, Any], updates: Dict[str, Any]) -> None:
        """Update a nested dictionary with values from another dictionary."""
        for key, value in updates.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._update_config(original[key], value)
            else:
                original[key] = value
    
    def _ensure_directories(self) -> None:
        """Ensure that all configured directories exist."""
        for path_key, path_value in self._config["paths"].items():
            try:
                path = Path(path_value)
                path.mkdir(parents=True, exist_ok=True)
                # Update the path to be absolute
                self._config["paths"][path_key] = str(path.absolute())
            except Exception as e:
                logger.warning(f"Failed to create directory {path_value}: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation.
        
        Args:
            key: Dot-separated key (e.g., 'app.name')
            default: Default value if key is not found
            
        Returns:
            The configuration value or default if not found
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def __getitem__(self, key: str) -> Any:
        """Get a configuration value using bracket notation."""
        return self.get(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Set a configuration value using dot notation."""
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the configuration as a dictionary."""
        return self._deep_copy(self._config)
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with a dictionary of updates."""
        self._update_config(self._config, updates)
    
    def reload(self) -> None:
        """Reload configuration from environment variables."""
        # Create a new config and update this instance
        new_config = Config()
        self._config = new_config._config
        self._ensure_directories()

# Create a global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance."""
    return config

def init_config(config_dict: Optional[Dict[str, Any]] = None) -> Config:
    """Initialize the global configuration.
    
    Args:
        config_dict: Optional dictionary to override default configuration
        
    Returns:
        Config: The initialized configuration instance
    """
    global config
    config = Config(config_dict)
    return config

def save_config(file_path: Union[str, Path] = None) -> bool:
    """Save the current configuration to a JSON file.
    
    Args:
        file_path: Path to the output file. If None, uses config["paths"]["config"]/config.json
        
    Returns:
        bool: True if the configuration was saved successfully, False otherwise
    """
    try:
        if file_path is None:
            config_dir = Path(config["paths"]["config"])
            config_dir.mkdir(parents=True, exist_ok=True)
            file_path = config_dir / "config.json"
        else:
            file_path = Path(file_path)
        
        with open(file_path, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        
        logger.info(f"Configuration saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save configuration: {str(e)}")
        return False

def load_config(file_path: Union[str, Path] = None) -> bool:
    """Load configuration from a JSON file.
    
    Args:
        file_path: Path to the configuration file. If None, uses config["paths"]["config"]/config.json
        
    Returns:
        bool: True if the configuration was loaded successfully, False otherwise
    """
    try:
        if file_path is None:
            config_dir = Path(config["paths"]["config"])
            file_path = config_dir / "config.json"
        else:
            file_path = Path(file_path)
        
        if not file_path.exists():
            logger.warning(f"Configuration file not found: {file_path}")
            return False
        
        with open(file_path, 'r') as f:
            loaded_config = json.load(f)
        
        config.update(loaded_config)
        logger.info(f"Configuration loaded from {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to load configuration: {str(e)}")
        return False
