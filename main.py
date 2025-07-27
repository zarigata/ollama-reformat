import os
import sys
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from typing import Optional
import subprocess
import platform
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="Ollama Model Fine-Tuning UI",
              description="A modern UI for fine-tuning Ollama models",
              version="0.1.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Detect hardware capabilities
def detect_hardware():
    hardware_info = {
        "os": platform.system(),
        "cpu_cores": os.cpu_count(),
        "cuda_available": False,
        "zluda_available": False
    }
    
    # Check for CUDA
    try:
        import torch
        hardware_info["cuda_available"] = torch.cuda.is_available()
        if hardware_info["cuda_available"]:
            hardware_info["gpu_name"] = torch.cuda.get_device_name(0)
    except ImportError:
        pass
    
    # Check for ZLUDA (simplified check)
    try:
        import ctypes
        zluda_lib = ctypes.util.find_library('zluda')
        hardware_info["zluda_available"] = zluda_lib is not None
    except:
        pass
    
    return hardware_info

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the main page"""
    hardware_info = detect_hardware()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "hardware_info": hardware_info
    })

@app.get("/api/models")
async def get_models():
    """Get list of installed models"""
    try:
        import ollama
        models = ollama.list()
        return {"status": "success", "data": models}
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/models/popular")
async def get_popular_models():
    """Get list of popular models from Ollama"""
    try:
        import requests
        response = requests.get("https://ollama.ai/library")
        # This is a simplified example - you'll need to parse the actual response
        return {"status": "success", "data": ["llama2", "mistral", "codellama"]}
    except Exception as e:
        logger.error(f"Error getting popular models: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
