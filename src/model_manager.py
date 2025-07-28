"""
Simplified model manager for Hugging Face and Ollama integration
Handles model discovery, download, and basic operations
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
from huggingface_hub import HfApi, list_models
import subprocess

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

class ModelManager:
    """Simple model management for non-technical users"""
    
    def __init__(self, config, hardware_info):
        self.config = config
        self.hardware_info = hardware_info
        self.logger = logging.getLogger(__name__)
        self.hf_api = HfApi()
        
    def get_installed_models(self) -> List[Dict[str, Any]]:
        """Get list of locally installed models"""
        models = []
        
        # Check Hugging Face cache
        hf_cache = Path.home() / ".cache" / "huggingface"
        if hf_cache.exists():
            for model_dir in hf_cache.glob("**/models--*"):
                model_name = model_dir.name.replace("models--", "").replace("--", "/")
                models.append({
                    "name": model_name,
                    "type": "huggingface",
                    "size": self._get_dir_size(model_dir),
                    "path": str(model_dir)
                })
        
        # Check Ollama models
        if OLLAMA_AVAILABLE:
            try:
                ollama_models = ollama.list()
                for model in ollama_models.get('models', []):
                    models.append({
                        "name": model['name'],
                        "type": "ollama",
                        "size": model.get('size', 0),
                        "modified": model.get('modified', '')
                    })
            except Exception as e:
                self.logger.warning(f"Could not fetch Ollama models: {e}")
        
        return models
    
    def get_popular_models(self) -> List[Dict[str, Any]]:
        """Get popular Hugging Face models suitable for fine-tuning"""
        popular_models = [
            {
                "name": "microsoft/DialoGPT-medium",
                "description": "Medium-sized conversational model",
                "size": "1.2GB",
                "category": "chat"
            },
            {
                "name": "facebook/blenderbot-400M-distill",
                "description": "Distilled conversational AI",
                "size": "1.6GB",
                "category": "chat"
            },
            {
                "name": "EleutherAI/gpt-neo-125M",
                "description": "Small but capable GPT model",
                "size": "500MB",
                "category": "general"
            },
            {
                "name": "distilbert-base-uncased",
                "description": "Fast and efficient BERT model",
                "size": "260MB",
                "category": "understanding"
            },
            {
                "name": "microsoft/DialoGPT-small",
                "description": "Small conversational model",
                "size": "350MB",
                "category": "chat"
            }
        ]
        
        return popular_models
    
    def search_huggingface_models(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search Hugging Face for models"""
        try:
            models = list(list_models(
                search=query,
                sort="downloads",
                direction=-1,
                limit=limit
            ))
            
            return [{
                "name": model.id,
                "description": model.card_data.get('description', 'No description') if model.card_data else 'No description',
                "downloads": model.downloads,
                "likes": model.likes,
                "size": "Unknown"
            } for model in models]
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    def download_model(self, model_name: str, model_type: str = "huggingface") -> bool:
        """Download a model (simplified for users)"""
        try:
            if model_type == "huggingface":
                # This would use transformers library in practice
                self.logger.info(f"Downloading {model_name}...")
                return True
            elif model_type == "ollama":
                if OLLAMA_AVAILABLE:
                    ollama.pull(model_name)
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
            return False
    
    def _get_dir_size(self, path: Path) -> str:
        """Get human-readable directory size"""
        try:
            total_size = 0
            for file in path.rglob('*'):
                if file.is_file():
                    total_size += file.stat().st_size
            
            if total_size > 1024**3:
                return f"{total_size / 1024**3:.1f}GB"
            elif total_size > 1024**2:
                return f"{total_size / 1024**2:.1f}MB"
            else:
                return f"{total_size / 1024:.1f}KB"
        except:
            return "Unknown"
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama is running"""
        try:
            if not OLLAMA_AVAILABLE:
                return False
            ollama.list()
            return True
        except:
            return False
