from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ModelInfo(BaseModel):
    """Information about an Ollama model."""
    name: str
    size: int
    modified_at: datetime
    digest: str

class ModelSearchResult(BaseModel):
    """Search result from Ollama library."""
    name: str
    description: str
    size: str
    tags: List[str]
    pulls: str

class FineTuneRequest(BaseModel):
    """Request for fine-tuning a model."""
    model_name: str
    method: str  # "jailbreak", "data_import", "general"
    parameters: Dict[str, Any]
    dataset_path: Optional[str] = None
    output_model_name: str

class FineTuneStatus(BaseModel):
    """Status of a fine-tuning job."""
    job_id: str
    model_name: str
    status: str  # "pending", "running", "completed", "failed"
    progress: float
    message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

class JailbreakPrompt(BaseModel):
    """Jailbreak prompt configuration."""
    name: str
    prompt: str
    description: str
    source: str
    last_updated: datetime

class DataImportRequest(BaseModel):
    """Request for importing training data."""
    files: List[str]
    format: str  # "pdf", "txt", "json", "csv"
    preprocessing: Dict[str, Any] = {}

class HardwareInfo(BaseModel):
    """Hardware detection results."""
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    gpu: Dict[str, Any]
    zluda: Dict[str, Any]
    recommended_backend: str
