"""
Ollama Model Scraper - Scrapes latest models from Ollama registry
"""

import requests
import json
from typing import List, Dict, Any
import re
from datetime import datetime

class OllamaModelScraper:
    """Scrapes and formats Ollama models from registry"""
    
    def __init__(self):
        self.base_url = "https://registry.ollama.ai"
        self.models_cache = []
        self.last_update = None
    
    def scrape_models(self) -> List[Dict[str, Any]]:
        """Scrape latest models from Ollama registry"""
        try:
            # Get library page
            response = requests.get(f"{self.base_url}/library", timeout=10)
            response.raise_for_status()
            
            # Parse models from the page content
            models = self._parse_models_from_html(response.text)
            
            # Enhance with additional info
            enhanced_models = self._enhance_model_info(models)
            
            self.models_cache = enhanced_models
            self.last_update = datetime.now()
            
            return enhanced_models
            
        except Exception as e:
            print(f"Error scraping models: {e}")
            return self._get_fallback_models()
    
    def _parse_models_from_html(self, html: str) -> List[str]:
        """Parse model names from HTML content"""
        # Extract model names using regex patterns
        patterns = [
            r'library/([^"\s>]+)',  # library/model-name pattern
            r'>([^<]+)</a>',        # Link text pattern
            r'model[":\s]+([^"\s,]+)'  # JSON-like model references
        ]
        
        models = []
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if match and len(match) > 2 and not match.startswith('http'):
                    # Clean up model names
                    model = match.strip('/').split('/')[-1]
                    if model and model not in models:
                        models.append(model)
        
        return models[:50]  # Limit to top 50
    
    def _enhance_model_info(self, model_names: List[str]) -> List[Dict[str, Any]]:
        """Enhance model info with categories and descriptions"""
        enhanced = []
        
        # Categorize models
        categories = {
            "llama": {
                "pattern": r'llama|llama2|llama3',
                "category": "Llama Family",
                "description": "Meta's Llama models - versatile and powerful"
            },
            "mistral": {
                "pattern": r'mistral|mixtral',
                "category": "Mistral AI",
                "description": "European AI models with excellent performance"
            },
            "phi": {
                "pattern": r'phi|phi3|phi4',
                "category": "Microsoft Phi",
                "description": "Small but powerful models from Microsoft"
            },
            "gemma": {
                "pattern": r'gemma|gemma2',
                "category": "Google Gemma",
                "description": "Google's open-source language models"
            },
            "qwen": {
                "pattern": r'qwen|qwen2',
                "category": "Alibaba Qwen",
                "description": "Chinese AI models with multilingual support"
            },
            "vision": {
                "pattern": r'vision|llava|moondream',
                "category": "Vision Models",
                "description": "Multimodal models with vision capabilities"
            },
            "code": {
                "pattern": r'code|coder|programming',
                "category": "Code Models",
                "description": "Specialized for programming and development"
            },
            "embed": {
                "pattern": r'embed|embedding',
                "category": "Embedding Models",
                "description": "For text embeddings and semantic search"
            }
        }
        
        for model_name in model_names:
            model_info = {
                "name": model_name,
                "full_name": f"{model_name}:latest",
                "size": self._estimate_model_size(model_name),
                "category": self._categorize_model(model_name, categories),
                "description": self._get_model_description(model_name),
                "tags": self._get_model_tags(model_name),
                "popularity": self._estimate_popularity(model_name),
                "last_updated": datetime.now().isoformat()
            }
            enhanced.append(model_info)
        
        return sorted(enhanced, key=lambda x: x["popularity"], reverse=True)
    
    def _categorize_model(self, model_name: str, categories: Dict) -> str:
        """Categorize model based on name patterns"""
        for cat_key, cat_info in categories.items():
            if re.search(cat_info["pattern"], model_name.lower()):
                return cat_info["category"]
        return "General Purpose"
    
    def _get_model_description(self, model_name: str) -> str:
        """Get description for model"""
        descriptions = {
            "llama3.1": "Meta's latest Llama 3.1 with improved reasoning",
            "llama3.2": "Llama 3.2 with vision capabilities",
            "mistral": "Mistral 7B - excellent general performance",
            "mistral-small": "Mistral Small - efficient and fast",
            "phi3": "Microsoft Phi-3 - small but powerful",
            "phi4": "Microsoft Phi-4 - latest reasoning model",
            "gemma2": "Google Gemma 2 - open-source excellence",
            "qwen2.5": "Alibaba Qwen 2.5 - multilingual powerhouse",
            "deepseek-coder": "DeepSeek specialized for coding",
            "llava": "Large Vision Language Model",
            "moondream": "Compact vision model",
            "nomic-embed-text": "Text embedding model"
        }
        
        for key, desc in descriptions.items():
            if key.lower() in model_name.lower():
                return desc
        
        return f"{model_name} - Ollama model"
    
    def _get_model_tags(self, model_name: str) -> List[str]:
        """Get tags for model"""
        tags = []
        
        if "llama" in model_name.lower():
            tags.extend(["meta", "open-source", "general-purpose"])
        if "mistral" in model_name.lower():
            tags.extend(["european", "efficient", "high-quality"])
        if "phi" in model_name.lower():
            tags.extend(["microsoft", "small", "efficient"])
        if "gemma" in model_name.lower():
            tags.extend(["google", "open-source", "lightweight"])
        if "vision" in model_name.lower() or "llava" in model_name.lower():
            tags.extend(["multimodal", "vision", "image"])
        if "code" in model_name.lower() or "coder" in model_name.lower():
            tags.extend(["programming", "code", "development"])
        if "embed" in model_name.lower():
            tags.extend(["embedding", "search", "semantic"])
        
        return tags
    
    def _estimate_model_size(self, model_name: str) -> str:
        """Estimate model size based on name"""
        if "1b" in model_name.lower():
            return "~1GB"
        elif "3b" in model_name.lower() or "phi" in model_name.lower():
            return "~2-4GB"
        elif "7b" in model_name.lower():
            return "~4-8GB"
        elif "13b" in model_name.lower():
            return "~8-16GB"
        elif "70b" in model_name.lower():
            return "~40-80GB"
        else:
            return "~2-8GB"
    
    def _estimate_popularity(self, model_name: str) -> int:
        """Estimate model popularity (1-10 scale)"""
        popular_models = {
            "llama3.1": 10,
            "llama3.2": 9,
            "mistral": 9,
            "phi3": 8,
            "gemma2": 8,
            "qwen2.5": 7,
            "deepseek-coder": 7,
            "llava": 6,
            "nomic-embed-text": 6
        }
        
        for key, score in popular_models.items():
            if key.lower() in model_name.lower():
                return score
        
        return 5  # Default score
    
    def _get_fallback_models(self) -> List[Dict[str, Any]]:
        """Fallback models if scraping fails"""
        return [
            {
                "name": "llama3.1",
                "full_name": "llama3.1:latest",
                "size": "~8GB",
                "category": "Llama Family",
                "description": "Meta's latest Llama 3.1 with improved reasoning",
                "tags": ["meta", "open-source", "general-purpose"],
                "popularity": 10,
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "mistral",
                "full_name": "mistral:latest",
                "size": "~4GB",
                "category": "Mistral AI",
                "description": "Mistral 7B - excellent general performance",
                "tags": ["european", "efficient", "high-quality"],
                "popularity": 9,
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "phi3",
                "full_name": "phi3:latest",
                "size": "~2GB",
                "category": "Microsoft Phi",
                "description": "Microsoft Phi-3 - small but powerful",
                "tags": ["microsoft", "small", "efficient"],
                "popularity": 8,
                "last_updated": datetime.now().isoformat()
            },
            {
                "name": "gemma2",
                "full_name": "gemma2:latest",
                "size": "~5GB",
                "category": "Google Gemma",
                "description": "Google Gemma 2 - open-source excellence",
                "tags": ["google", "open-source", "lightweight"],
                "popularity": 8,
                "last_updated": datetime.now().isoformat()
            }
        ]
    
    def get_models_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get models by category"""
        if not self.models_cache:
            self.scrape_models()
        
        return [m for m in self.models_cache if m["category"] == category]
    
    def get_top_models(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top models by popularity"""
        if not self.models_cache:
            self.scrape_models()
        
        return self.models_cache[:limit]
    
    def search_models(self, query: str) -> List[Dict[str, Any]]:
        """Search models by name or description"""
        if not self.models_cache:
            self.scrape_models()
        
        query = query.lower()
        return [
            m for m in self.models_cache
            if query in m["name"].lower() or 
               query in m["description"].lower() or
               any(query in tag.lower() for tag in m["tags"])
        ]
