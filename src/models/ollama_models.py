"""
Ollama Models Module

This module provides functionality to interact with Ollama models,
including listing, downloading, and managing models.
"""
import os
import json
import logging
import subprocess
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import requests
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaManager:
    """Manager for Ollama model operations."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama manager.
        
        Args:
            base_url: Base URL for the Ollama API
        """
        self.base_url = base_url
        self.timeout = 60  # seconds
    
    def list_models(self) -> List[Dict]:
        """List all installed Ollama models.
        
        Returns:
            List of installed models with their details
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json().get("models", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing models: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list models: {str(e)}"
            )
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get detailed information about a specific model.
        
        Args:
            model_name: Name of the model to get info for
            
        Returns:
            Dictionary containing model information
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/show",
                json={"name": model_name},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting model info for {model_name}: {str(e)}")
            raise HTTPException(
                status_code=404 if response.status_code == 404 else 500,
                detail=f"Failed to get model info: {str(e)}"
            )
    
    def pull_model(self, model_name: str) -> Dict:
        """Pull a model from the Ollama library.
        
        Args:
            model_name: Name of the model to pull
            
        Returns:
            Dictionary containing pull status and details
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300  # Longer timeout for model downloads
            )
            
            # Stream the response to show progress
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        yield data
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode JSON: {line}")
                        continue
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error pulling model {model_name}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to pull model: {str(e)}"
            )
    
    def delete_model(self, model_name: str) -> Dict:
        """Delete a model from the local Ollama installation.
        
        Args:
            model_name: Name of the model to delete
            
        Returns:
            Dictionary containing deletion status
        """
        try:
            response = requests.delete(
                f"{self.base_url}/api/delete",
                json={"name": model_name},
                timeout=self.timeout
            )
            response.raise_for_status()
            return {"status": "success", "message": f"Model {model_name} deleted successfully"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting model {model_name}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete model: {str(e)}"
            )
    
    def search_models(self, query: str) -> List[Dict]:
        """Search for models in the Ollama library.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching models with their details
        """
        try:
            # First, get all available models
            response = requests.get("https://ollama.ai/library")
            response.raise_for_status()
            
            # This is a simplified example - in a real implementation, you would parse the HTML
            # to extract model information based on the query
            # For now, we'll return some mock data
            
            # Mock data - replace with actual implementation
            mock_models = [
                {
                    "name": "llama2",
                    "description": "Meta's LLaMA 2 large language model",
                    "size": "3.8 GB",
                    "downloads": 1000000,
                    "last_updated": "2023-07-18"
                },
                {
                    "name": "mistral",
                    "description": "Mistral 7B large language model",
                    "size": "4.1 GB",
                    "downloads": 500000,
                    "last_updated": "2023-09-27"
                },
                {
                    "name": "codellama",
                    "description": "Code generation model based on LLaMA",
                    "size": "3.5 GB",
                    "downloads": 750000,
                    "last_updated": "2023-08-24"
                },
                {
                    "name": "vicuna",
                    "description": "Chat model fine-tuned from LLaMA",
                    "size": "4.2 GB",
                    "downloads": 300000,
                    "last_updated": "2023-04-28"
                },
                {
                    "name": "wizard",
                    "description": "WizardLM language model",
                    "size": "4.0 GB",
                    "downloads": 250000,
                    "last_updated": "2023-06-15"
                }
            ]
            
            # Filter based on query (case-insensitive)
            query = query.lower()
            return [
                model for model in mock_models
                if (query in model["name"].lower() or 
                    query in model["description"].lower())
            ]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching for models: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to search for models: {str(e)}"
            )
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed and running.
        
        Returns:
            bool: True if Ollama is installed and running, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def start_ollama_service(self) -> bool:
        """Attempt to start the Ollama service.
        
        Returns:
            bool: True if the service was started successfully, False otherwise
        """
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["ollama", "serve"], check=True, capture_output=True)
            else:  # Unix-like
                subprocess.run(["systemctl", "start", "ollama"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Failed to start Ollama service: {str(e)}")
            return False
    
    def get_system_info(self) -> Dict:
        """Get system information including hardware and Ollama status.
        
        Returns:
            Dictionary containing system information
        """
        try:
            import torch
            import platform
            import psutil
            
            system_info = {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor(),
                },
                "cpu": {
                    "cores": psutil.cpu_count(logical=False),
                    "threads": psutil.cpu_count(logical=True),
                    "usage": psutil.cpu_percent(interval=1),
                },
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "used": psutil.virtual_memory().used,
                    "percent": psutil.virtual_memory().percent,
                },
                "gpu": {
                    "available": torch.cuda.is_available() if torch.cuda.is_available() else False,
                    "count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
                    "devices": []
                },
                "ollama": {
                    "installed": self.check_ollama_installed(),
                    "version": "unknown"
                }
            }
            
            # Get GPU details if available
            if system_info["gpu"]["available"]:
                for i in range(torch.cuda.device_count()):
                    system_info["gpu"]["devices"].append({
                        "id": i,
                        "name": torch.cuda.get_device_name(i),
                        "memory": {
                            "total": torch.cuda.get_device_properties(i).total_memory,
                            "allocated": torch.cuda.memory_allocated(i),
                            "reserved": torch.cuda.memory_reserved(i),
                        }
                    })
            
            # Get Ollama version if available
            if system_info["ollama"]["installed"]:
                try:
                    response = requests.get(f"{self.base_url}/api/version", timeout=5)
                    if response.status_code == 200:
                        system_info["ollama"]["version"] = response.json().get("version", "unknown")
                except:
                    pass
            
            return system_info
            
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get system information: {str(e)}"
            )

# Create a singleton instance
ollama_manager = OllamaManager()
