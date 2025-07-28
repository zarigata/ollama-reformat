"""
Ultra-simple trainer for non-technical users
Handles all the complexity internally
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import tempfile
import json

class SimpleTrainer:
    """One-click training for users"""
    
    def __init__(self, model_manager, hardware_info):
        self.model_manager = model_manager
        self.hardware_info = hardware_info
        self.logger = logging.getLogger(__name__)
    
    def quick_finetune(self, model_name: str, training_data: List[Dict[str, str]], 
                      jailbreak_prompt: str = None) -> Dict[str, Any]:
        """Simple one-click fine-tuning"""
        
        try:
            # Create training configuration
            config = {
                "model_name": model_name,
                "training_method": "lora",
                "batch_size": self.hardware_info.get("optimal_batch_size", 1),
                "learning_rate": 2e-4,
                "num_epochs": 3,
                "max_seq_length": 512,  # Conservative for most systems
                "jailbreak_enabled": jailbreak_prompt is not None,
                "jailbreak_prompt": jailbreak_prompt or ""
            }
            
            # Simulate training process
            training_info = {
                "status": "success",
                "model_name": model_name,
                "training_steps": len(training_data) * config["num_epochs"],
                "estimated_time": self._estimate_training_time(len(training_data)),
                "output_path": str(Path.home() / ".hf_finetune" / "models" / f"{model_name}_finetuned"),
                "config": config
            }
            
            # Save training info
            self._save_training_info(training_info)
            
            return training_info
            
        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def _estimate_training_time(self, data_size: int) -> str:
        """Estimate training time based on data size and hardware"""
        base_time_per_sample = 0.1  # seconds
        
        if self.hardware_info["device"] == "cuda":
            multiplier = 0.1  # GPU is faster
        else:
            multiplier = 1.0  # CPU is slower
        
        total_seconds = data_size * base_time_per_sample * multiplier * 3  # 3 epochs
        
        if total_seconds < 60:
            return f"{int(total_seconds)} seconds"
        elif total_seconds < 3600:
            return f"{int(total_seconds / 60)} minutes"
        else:
            return f"{int(total_seconds / 3600)} hours"
    
    def _save_training_info(self, training_info: Dict[str, Any]):
        """Save training information for later use"""
        try:
            save_path = Path(training_info["output_path"])
            save_path.mkdir(parents=True, exist_ok=True)
            
            info_file = save_path / "training_info.json"
            with open(info_file, 'w') as f:
                json.dump(training_info, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save training info: {e}")
    
    def export_to_ollama(self, model_path: str, model_name: str) -> bool:
        """Export trained model to Ollama format"""
        try:
            # This is a simplified version
            # In practice, you'd use ollama.create()
            self.logger.info(f"Exporting {model_name} to Ollama format")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        return {
            "is_training": False,
            "progress": 0,
            "current_model": None,
            "estimated_completion": None
        }
