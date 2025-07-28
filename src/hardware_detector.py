"""
Automatic hardware detection for optimal performance
Handles CUDA, CPU, and ZLUDA detection without user input
"""

import torch
import psutil
import logging
from typing import Dict, Any

try:
    import pynvml
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False

class HardwareDetector:
    """Automatically detects best hardware configuration"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def detect_hardware(self) -> Dict[str, Any]:
        """Detect hardware and return optimal configuration"""
        config = {
            "device": "cpu",
            "device_name": "CPU",
            "memory_gb": psutil.virtual_memory().total / (1024**3),
            "cuda_available": torch.cuda.is_available(),
            "zluda_available": False,
            "recommendation": ""
        }
        
        # Check for NVIDIA CUDA
        if torch.cuda.is_available():
            try:
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                config.update({
                    "device": "cuda",
                    "device_name": gpu_name,
                    "gpu_memory_gb": gpu_memory,
                    "recommendation": f"Using NVIDIA GPU: {gpu_name} ({gpu_memory:.1f}GB)"
                })
                return config
            except Exception as e:
                self.logger.warning(f"CUDA detection failed: {e}")
        
        # Check for ZLUDA (AMD GPU with CUDA compatibility)
        zluda_config = self._check_zluda()
        if zluda_config["available"]:
            config.update({
                "device": "cuda",  # ZLUDA appears as CUDA
                "device_name": f"ZLUDA ({zluda_config['gpu_name']})",
                "zluda_available": True,
                "recommendation": f"Using ZLUDA with AMD GPU: {zluda_config['gpu_name']}"
            })
            return config
        
        # Default to CPU
        cpu_count = psutil.cpu_count()
        config.update({
            "recommendation": f"Using CPU ({cpu_count} cores, {config['memory_gb']:.1f}GB RAM)"
        })
        
        return config
    
    def _check_zluda(self) -> Dict[str, Any]:
        """Check if ZLUDA is available"""
        # Simple check for ZLUDA - this is a basic implementation
        # In practice, you'd check for specific ZLUDA indicators
        return {
            "available": False,
            "gpu_name": "AMD GPU (ZLUDA support)"
        }
    
    def get_optimal_batch_size(self, hardware_info: Dict[str, Any]) -> int:
        """Get safe batch size based on hardware"""
        if hardware_info["device"] == "cuda":
            memory_gb = hardware_info.get("gpu_memory_gb", hardware_info.get("memory_gb", 8))
            if memory_gb >= 12:
                return 4
            elif memory_gb >= 8:
                return 2
            else:
                return 1
        else:
            # CPU - conservative approach
            return 1
