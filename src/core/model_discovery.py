"""
Model discovery and recommendation system
"""

import subprocess
import json
import requests
from typing import List, Dict, Any
import re
from bs4 import BeautifulSoup

class ModelDiscovery:
    """Discovers and recommends Ollama models"""
    
    def __init__(self):
        self.ollama_models = []
        self.popular_models = [
            {
                "name": "llama3.1",
                "size": "8B",
                "use_case": "General purpose, chat, reasoning",
                "performance": "Excellent",
                "tags": ["general", "chat", "reasoning"]
            },
            {
                "name": "mistral",
                "size": "7B",
                "use_case": "Code generation, technical tasks",
                "performance": "Very Good",
                "tags": ["code", "technical"]
            },
            {
                "name": "phi3",
                "size": "3.8B",
                "use_case": "Fast inference, lightweight",
                "performance": "Good",
                "tags": ["fast", "lightweight"]
            },
            {
                "name": "codellama",
                "size": "7B",
                "use_case": "Code completion, programming",
                "performance": "Excellent",
                "tags": ["code", "programming"]
            },
            {
                "name": "llava",
                "size": "7B",
                "use_case": "Image understanding, vision",
                "performance": "Good",
                "tags": ["vision", "image"]
            }
        ]
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get available models from local Ollama"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                models = []
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            name = parts[0]
                            size = parts[1]
                            modified = " ".join(parts[2:])
                            
                            # Find matching popular model info
                            popular_match = next(
                                (m for m in self.popular_models if name.startswith(m["name"])),
                                None
                            )
                            
                            models.append({
                                "name": name,
                                "size": size,
                                "use_case": popular_match["use_case"] if popular_match else "General",
                                "performance": popular_match["performance"] if popular_match else "Unknown",
                                "available": True,
                                "tags": popular_match["tags"] if popular_match else ["general"]
                            })
                
                return models
            else:
                return self._get_default_models()
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return self._get_default_models()
    
    def _get_default_models(self) -> List[Dict[str, Any]]:
        """Return default models when Ollama is not available"""
        return [
            {**model, "available": False} 
            for model in self.popular_models
        ]
    
    def find_models_for_task(self, task_description: str) -> List[Dict[str, Any]]:
        """Find models best suited for a specific task"""
        task_lower = task_description.lower()
        all_models = self.get_available_models()
        
        # Scoring based on task keywords
        task_keywords = {
            "code": ["code", "programming", "python", "javascript", "development"],
            "chat": ["chat", "conversation", "dialogue", "assistant"],
            "technical": ["technical", "science", "math", "engineering"],
            "creative": ["creative", "writing", "story", "poem"],
            "vision": ["image", "vision", "photo", "picture"],
            "medical": ["medical", "health", "doctor", "diagnosis"],
            "legal": ["legal", "law", "contract", "regulation"],
            "education": ["education", "teaching", "learning", "tutorial"]
        }
        
        scored_models = []
        for model in all_models:
            score = 0
            
            # Check model tags
            for tag in model.get("tags", []):
                if any(keyword in task_lower for keyword in task_keywords.get(tag, [])):
                    score += 2
            
            # Check model name and use case
            model_text = f"{model['name']} {model['use_case']}".lower()
            for category, keywords in task_keywords.items():
                if any(keyword in model_text for keyword in keywords):
                    score += 1
            
            # Boost available models
            if model["available"]:
                score += 1
            
            model["score"] = score
            scored_models.append(model)
        
        # Sort by score and return top matches
        scored_models.sort(key=lambda x: x["score"], reverse=True)
        return scored_models[:10]
    
    def download_model(self, model_name: str) -> Dict[str, str]:
        """Download a model using Ollama"""
        try:
            print(f"Downloading {model_name}...")
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes for large models
            )
            
            if result.returncode == 0:
                return {"status": "success", "message": f"Successfully downloaded {model_name}"}
            else:
                return {"status": "error", "message": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Download timeout"}
        except FileNotFoundError:
            return {"status": "error", "message": "Ollama not found. Please install Ollama first."}
