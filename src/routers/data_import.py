from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
import os
import uuid
from pathlib import Path
import shutil
from src.models.ollama_models import DataImportRequest

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)) -> Dict[str, Any]:
    """Upload files for training data."""
    uploaded_files = []
    
    for file in files:
        if file.size > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=413, detail=f"File {file.filename} too large")
        
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
        
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append({
                "id": file_id,
                "filename": file.filename,
                "size": file.size,
                "path": str(file_path)
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload {file.filename}: {str(e)}")
    
    return {"uploaded_files": uploaded_files}

@router.get("/files")
async def list_uploaded_files() -> List[Dict[str, Any]]:
    """List all uploaded files."""
    files = []
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            stat = file_path.stat()
            files.append({
                "filename": file_path.name,
                "size": stat.st_size,
                "modified": stat.st_mtime
            })
    return files

@router.delete("/files/{filename}")
async def delete_file(filename: str) -> Dict[str, str]:
    """Delete an uploaded file."""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        file_path.unlink()
        return {"status": "success", "message": f"File {filename} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@router.post("/process")
async def process_uploaded_data(request: DataImportRequest) -> Dict[str, Any]:
    """Process uploaded data for fine-tuning."""
    # This would implement actual data processing
    # For now, return a mock response
    
    processed_files = []
    for file_path in request.files:
        if os.path.exists(file_path):
            processed_files.append({
                "file": file_path,
                "format": request.format,
                "processed": True,
                "samples": 100  # Mock sample count
            })
    
    return {
        "processed_files": processed_files,
        "total_samples": sum(f["samples"] for f in processed_files),
        "ready_for_training": True
    }
