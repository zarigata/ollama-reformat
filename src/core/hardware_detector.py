"""
Hardware detection and optimization for CPU/GPU training
"""

import os
import psutil
import torch
import platform
from typing import Dict, Any

class HardwareDetector:
    """Detects and optimizes hardware configuration for training"""
    
    def __init__(self):
        self.device = self._detect_device()
        self.threads = self._optimize_threads()
        self.memory = self._get_memory_info()
        self.gpu_info = self._get_gpu_info()
        
    def _detect_device(self) -> str:
        """Detect the optimal device for training"""
        if torch.cuda.is_available():
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _optimize_threads(self) -> int:
        """Optimize CPU thread count for training"""
        cpu_count = os.cpu_count() or 1
        # Use 75% of available cores, max 8 for stability
        optimal = max(1, min(int(cpu_count * 0.75), 8))
        return optimal
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get system memory information"""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "percent_used": memory.percent
        }
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information if available"""
        if self.device == "cuda":
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            return {
                "available": True,
                "count": gpu_count,
                "name": gpu_name,
                "memory_gb": round(gpu_memory, 2)
            }
        return {"available": False}
    
    def print_specs(self):
        """Print hardware specifications"""
        print("=" * 50)
        print("🔧 HARDWARE DETECTION")
        print("=" * 50)
        print(f"💻 Platform: {platform.system()} {platform.release()}")
        print(f"🧠 CPU Cores: {os.cpu_count()}")
        print(f"🎯 Optimal Threads: {self.threads}")
        print(f"💾 RAM: {self.memory['total_gb']} GB")
        print(f"💾 Available RAM: {self.memory['available_gb']} GB")
        
        if self.gpu_info["available"]:
            print(f"🎮 GPU: {self.gpu_info['name']}")
            print(f"🎮 GPU Memory: {self.gpu_info['memory_gb']} GB")
        else:
            print("🖥️  GPU: Not available - using CPU")
        
        print(f"⚡ Training Device: {self.device.upper()}")
        print("=" * 50)
    
    def get_training_config(self) -> Dict[str, Any]:
        """Get optimized training configuration"""
        config = {
            "device": self.device,
            "threads": self.threads,
            "batch_size": self._calculate_optimal_batch_size(),
            "gradient_accumulation_steps": 1,
            "fp16": self.device == "cuda",
            "bf16": self.device == "cuda" and torch.cuda.is_bf16_supported(),
        }
        
        if self.device == "cpu":
            config.update({
                "fp16": False,
                "bf16": False,
                "use_cpu_amp": False,
                "dataloader_num_workers": min(self.threads, 4)
            })
        
        return config
    
    def _calculate_optimal_batch_size(self) -> int:
        """Calculate optimal batch size based on hardware"""
        if self.device == "cuda" and self.gpu_info["available"]:
            gpu_memory = self.gpu_info["memory_gb"]
            if gpu_memory >= 12:
                return 4
            elif gpu_memory >= 8:
                return 2
            else:
                return 1
        else:
            # CPU training - smaller batch sizes
            available_ram = self.memory["available_gb"]
            if available_ram >= 16:
                return 2
            elif available_ram >= 8:
                return 1
            else:
                return 1
