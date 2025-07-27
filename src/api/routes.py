"""
API Routes for Ollama Model Fine-Tuning UI

This module defines the API endpoints for the Ollama Model Fine-Tuning UI.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List, Optional, Dict, Any
import json
import logging
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

from ...src.models.ollama_models import ollama_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@router.get("/models")
async def get_models():
    """Get list of installed models"""
    try:
        models = ollama_manager.list_models()
        return {"status": "success", "data": {"models": models}}
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get models: {str(e)}"
        )

@router.get("/models/search")
async def search_models(query: str = Query(..., min_length=2)):
    """Search for models in the Ollama library"""
    try:
        results = ollama_manager.search_models(query)
        return {"status": "success", "data": results}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching models: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search models: {str(e)}"
        )

@router.post("/models/pull/{model_name}")
async def pull_model(model_name: str):
    """Pull a model from the Ollama library"""
    try:
        # This will return a generator that yields progress updates
        def generate():
            for progress in ollama_manager.pull_model(model_name):
                yield f"data: {json.dumps(progress)}\n\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error pulling model {model_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to pull model: {str(e)}"
        )

@router.delete("/models/{model_name}")
async def delete_model(model_name: str):
    """Delete a model from the local Ollama installation"""
    try:
        result = ollama_manager.delete_model(model_name)
        return {"status": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting model {model_name}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete model: {str(e)}"
        )

@router.get("/system/info")
async def get_system_info():
    """Get system information including hardware and Ollama status"""
    try:
        system_info = ollama_manager.get_system_info()
        return {"status": "success", "data": system_info}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting system info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system information: {str(e)}"
        )

@router.post("/fine-tune/upload")
async def upload_training_data(
    files: List[UploadFile] = File(...),
    model_name: str = Form(...),
    training_config: str = Form("{}"),
):
    """Upload training data for fine-tuning"""
    try:
        # Parse training config
        try:
            config = json.loads(training_config)
            if not isinstance(config, dict):
                raise ValueError("Training config must be a JSON object")
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid training config: {str(e)}"
            )
        
        # Create a temporary directory for the uploaded files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            uploaded_files = []
            
            # Save uploaded files
            for file in files:
                file_path = temp_dir_path / file.filename
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                uploaded_files.append({
                    "filename": file.filename,
                    "size": file_path.stat().st_size,
                    "path": str(file_path)
                })
            
            # Here you would typically process the files and start the fine-tuning process
            # For now, we'll just return the file info
            
            return {
                "status": "success",
                "data": {
                    "model_name": model_name,
                    "config": config,
                    "uploaded_files": uploaded_files,
                    "message": "Files uploaded successfully. Ready to start fine-tuning."
                }
            }
            
    except Exception as e:
        logger.error(f"Error uploading training data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload training data: {str(e)}"
        )

@router.post("/fine-tune/start")
async def start_fine_tuning(
    model_name: str,
    base_model: str,
    training_data: dict,
    config: dict = {}
):
    """Start the fine-tuning process"""
    try:
        # This is where you would integrate with your fine-tuning pipeline
        # For now, we'll just return a success response
        
        # Simulate fine-tuning process
        def simulate_training():
            steps = 10
            for i in range(steps + 1):
                progress = {
                    "step": i,
                    "total_steps": steps,
                    "progress": (i / steps) * 100,
                    "metrics": {
                        "loss": 1.0 - (i / steps) * 0.9,  # Simulated loss
                        "accuracy": 0.0 + (i / steps) * 0.8  # Simulated accuracy
                    },
                    "status": "training" if i < steps else "completed",
                    "message": f"Training step {i}/{steps}"
                }
                yield f"data: {json.dumps(progress)}\n\n"
                import time
                time.sleep(0.5)  # Simulate processing time
        
        return StreamingResponse(
            simulate_training(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except Exception as e:
        logger.error(f"Error starting fine-tuning: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start fine-tuning: {str(e)}"
        )

@router.get("/fine-tune/status/{job_id}")
async def get_fine_tune_status(job_id: str):
    """Get the status of a fine-tuning job"""
    try:
        # In a real implementation, you would check the status of the job with the given ID
        # For now, we'll return a mock response
        return {
            "status": "success",
            "data": {
                "job_id": job_id,
                "status": "completed",
                "progress": 100,
                "metrics": {
                    "final_loss": 0.1234,
                    "final_accuracy": 0.8765
                },
                "started_at": "2023-01-01T00:00:00Z",
                "completed_at": "2023-01-01T01:30:00Z",
                "model_name": f"fine-tuned-{job_id[:8]}"
            }
        }
    except Exception as e:
        logger.error(f"Error getting fine-tuning status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get fine-tuning status: {str(e)}"
        )
