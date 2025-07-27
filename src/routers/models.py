from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import httpx
import ollama
import asyncio
from src.models.ollama_models import ModelInfo, ModelSearchResult

router = APIRouter()

@router.get("/installed")
async def get_installed_models() -> List[ModelInfo]:
    """Get all locally installed Ollama models."""
    try:
        models = await ollama.list()
        return [
            ModelInfo(
                name=model["name"],
                size=model["size"],
                modified_at=model["modified_at"],
                digest=model["digest"]
            )
            for model in models.get("models", [])
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")

@router.get("/popular")
async def get_popular_models() -> List[Dict[str, Any]]:
    """Get popular models from Ollama library."""
    popular_models = [
        {
            "name": "llama2",
            "description": "Llama 2 is a collection of pretrained and fine-tuned large language models",
            "size": "3.8GB",
            "tags": ["7b", "13b", "70b"],
            "pulls": "10M+"
        },
        {
            "name": "mistral",
            "description": "Mistral AI's language model",
            "size": "4.1GB",
            "tags": ["7b"],
            "pulls": "5M+"
        },
        {
            "name": "codellama",
            "description": "Code Llama is a code-specialized version of Llama 2",
            "size": "3.8GB",
            "tags": ["7b", "13b", "34b", "70b"],
            "pulls": "3M+"
        },
        {
            "name": "llava",
            "description": "Large language and vision assistant",
            "size": "4.5GB",
            "tags": ["7b", "13b"],
            "pulls": "2M+"
        },
        {
            "name": "neural-chat",
            "description": "Neural Chat 7B is a fine-tuned model based on Mistral-7B",
            "size": "4.1GB",
            "tags": ["7b"],
            "pulls": "1M+"
        }
    ]
    return popular_models

@router.get("/search")
async def search_models(query: str) -> List[ModelSearchResult]:
    """Search models on Ollama website."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://ollama.ai/api/search?q={query}",
                timeout=10.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return [
                    ModelSearchResult(
                        name=model.get("name", ""),
                        description=model.get("description", ""),
                        size=model.get("size", ""),
                        tags=model.get("tags", []),
                        pulls=model.get("pulls", "0")
                    )
                    for model in data.get("results", [])
                ]
            else:
                # Fallback to mock search
                return await _mock_search_models(query)
    except Exception as e:
        # Fallback to mock search if API fails
        return await _mock_search_models(query)

async def _mock_search_models(query: str) -> List[ModelSearchResult]:
    """Mock search for offline development."""
    all_models = [
        ModelSearchResult(
            name="llama2",
            description="Llama 2 is a collection of pretrained and fine-tuned large language models",
            size="3.8GB",
            tags=["7b", "13b", "70b"],
            pulls="10M+"
        ),
        ModelSearchResult(
            name="mistral",
            description="Mistral AI's language model",
            size="4.1GB",
            tags=["7b"],
            pulls="5M+"
        ),
        ModelSearchResult(
            name="codellama",
            description="Code Llama is a code-specialized version of Llama 2",
            size="3.8GB",
            tags=["7b", "13b", "34b", "70b"],
            pulls="3M+"
        )
    ]
    
    query_lower = query.lower()
    return [model for model in all_models if query_lower in model.name.lower() or query_lower in model.description.lower()]

@router.post("/pull/{model_name}")
async def pull_model(model_name: str):
    """Download and install a model from Ollama."""
    try:
        result = await ollama.pull(model_name)
        return {"status": "success", "message": f"Model {model_name} downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to pull model: {str(e)}")

@router.delete("/remove/{model_name}")
async def remove_model(model_name: str):
    """Remove a locally installed model."""
    try:
        await ollama.delete(model_name)
        return {"status": "success", "message": f"Model {model_name} removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove model: {str(e)}")

@router.get("/info/{model_name}")
async def get_model_info(model_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific model."""
    try:
        info = await ollama.show(model_name)
        return info
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")
