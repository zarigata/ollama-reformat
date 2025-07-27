import psutil
import torch
import subprocess
import os
import platform
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class HardwareDetector:
    """Detects available hardware for optimal model training configuration."""
    
    def __init__(self):
        self.hardware_info = {}
    
    async def detect_hardware(self) -> Dict[str, Any]:
        """Comprehensive hardware detection for CUDA, CPU, and ZLUDA support."""
        
        info = {
            "cpu": self._detect_cpu(),
            "memory": self._detect_memory(),
            "gpu": await self._detect_gpu(),
            "zluda": await self._detect_zluda(),
            "platform": platform.system(),
            "python_version": platform.python_version()
        }
        
        # Determine optimal backend
        info["recommended_backend"] = self._determine_backend(info)
        
        self.hardware_info = info
        logger.info(f"Hardware detection complete: {info}")
        return info
    
    def _detect_cpu(self) -> Dict[str, Any]:
        """Detect CPU information."""
        return {
            "count": psutil.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False),
            "brand": platform.processor(),
            "architecture": platform.machine(),
            "max_frequency": psutil.cpu_freq().max if psutil.cpu_freq() else None
        }
    
    def _detect_memory(self) -> Dict[str, Any]:
        """Detect system memory."""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "percent_used": memory.percent
        }
    
    async def _detect_gpu(self) -> Dict[str, Any]:
        """Detect GPU information including CUDA support."""
        gpu_info = {
            "cuda_available": torch.cuda.is_available(),
            "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
            "devices": []
        }
        
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                device_props = torch.cuda.get_device_properties(i)
                gpu_info["devices"].append({
                    "id": i,
                    "name": device_props.name,
                    "memory_total_gb": round(device_props.total_memory / (1024**3), 2),
                    "memory_free_gb": round(torch.cuda.memory_reserved(i) / (1024**3), 2),
                    "compute_capability": f"{device_props.major}.{device_props.minor}"
                })
        
        return gpu_info
    
    async def _detect_zluda(self) -> Dict[str, Any]:
        """Detect ZLUDA support for AMD GPUs."""
        zluda_info = {
            "available": False,
            "version": None,
            "path": None
        }
        
        # Check for ZLUDA installation
        possible_paths = [
            os.environ.get('ZLUDA_PATH'),
            'C:\\Program Files\\ZLUDA',
            'C:\\ZLUDA',
            os.path.expanduser('~\\ZLUDA')
        ]
        
        for path in possible_paths:
            if path and os.path.exists(os.path.join(path, 'zluda.dll')):
                zluda_info.update({
                    "available": True,
                    "path": path,
                    "version": "detected"  # Could parse version from DLL
                })
                break
        
        # Check for AMD GPU via ROCm (simplified check)
        try:
            result = subprocess.run(['rocminfo'], capture_output=True, text=True)
            if result.returncode == 0:
                zluda_info["rocm_available"] = True
        except FileNotFoundError:
            zluda_info["rocm_available"] = False
        
        return zluda_info
    
    def _determine_backend(self, info: Dict[str, Any]) -> str:
        """Determine the optimal backend based on detected hardware."""
        
        # Priority: CUDA > ZLUDA > CPU
        if info["gpu"]["cuda_available"] and info["gpu"]["devices"]:
            return "cuda"
        elif info["zluda"]["available"]:
            return "zluda"
        else:
            return "cpu"
    
    def get_training_config(self) -> Dict[str, Any]:
        """Generate optimal training configuration based on hardware."""
        if not self.hardware_info:
            return {"backend": "cpu", "batch_size": 1, "learning_rate": 5e-5}
        
        backend = self.hardware_info["recommended_backend"]
        memory_gb = self.hardware_info["memory"]["total_gb"]
        
        config = {
            "backend": backend,
            "batch_size": 4 if backend in ["cuda", "zluda"] else 1,
            "learning_rate": 2e-5 if backend in ["cuda", "zluda"] else 5e-5,
            "gradient_accumulation_steps": 4 if memory_gb < 16 else 1,
            "max_length": 512 if memory_gb < 8 else 1024
        }
        
        # Adjust based on GPU memory
        if backend in ["cuda", "zluda"] and self.hardware_info["gpu"]["devices"]:
            gpu_memory = self.hardware_info["gpu"]["devices"][0]["memory_total_gb"]
            if gpu_memory < 8:
                config["batch_size"] = 2
                config["gradient_accumulation_steps"] = 8
        
        return config
