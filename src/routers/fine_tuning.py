from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
import asyncio
from datetime import datetime
from src.models.ollama_models import FineTuneRequest, FineTuneStatus, JailbreakPrompt
from src.services.jailbreak_service import JailbreakService
from src.services.fine_tuning_service import FineTuningService

router = APIRouter()

# In-memory storage for jobs (in production, use Redis or database)
active_jobs = {}

@router.post("/start")
async def start_fine_tuning(
    request: FineTuneRequest,
    background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """Start a new fine-tuning job."""
    job_id = str(uuid.uuid4())
    
    job = FineTuneStatus(
        job_id=job_id,
        model_name=request.model_name,
        status="pending",
        progress=0.0,
        started_at=datetime.now(),
        message="Starting fine-tuning process..."
    )
    
    active_jobs[job_id] = job
    
    # Start background task
    background_tasks.add_task(_run_fine_tuning, job_id, request)
    
    return {"job_id": job_id, "status": "started"}

@router.get("/status/{job_id}")
async def get_job_status(job_id: str) -> FineTuneStatus:
    """Get the status of a fine-tuning job."""
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return active_jobs[job_id]

@router.get("/jailbreak-prompts")
async def get_jailbreak_prompts() -> list[JailbreakPrompt]:
    """Get latest jailbreak prompts from web sources."""
    service = JailbreakService()
    prompts = await service.fetch_latest_prompts()
    return prompts

@router.get("/jobs")
async def get_all_jobs() -> Dict[str, FineTuneStatus]:
    """Get all active and recent jobs."""
    return {job_id: job for job_id, job in active_jobs.items()}

@router.delete("/jobs/{job_id}")
async def cancel_job(job_id: str) -> Dict[str, str]:
    """Cancel a running fine-tuning job."""
    if job_id not in active_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    active_jobs[job_id].status = "cancelled"
    active_jobs[job_id].message = "Job cancelled by user"
    
    return {"status": "cancelled", "job_id": job_id}

async def _run_fine_tuning(job_id: str, request: FineTuneRequest):
    """Background task for fine-tuning."""
    job = active_jobs[job_id]
    
    try:
        service = FineTuningService()
        
        if request.method == "jailbreak":
            await _run_jailbreak_fine_tuning(job, request, service)
        elif request.method == "data_import":
            await _run_data_import_fine_tuning(job, request, service)
        elif request.method == "general":
            await _run_general_fine_tuning(job, request, service)
        else:
            raise ValueError(f"Unknown fine-tuning method: {request.method}")
            
    except Exception as e:
        job.status = "failed"
        job.message = str(e)
        job.completed_at = datetime.now()

async def _run_jailbreak_fine_tuning(job: FineTuneStatus, request: FineTuneRequest, service: FineTuningService):
    """Run jailbreak fine-tuning."""
    job.status = "running"
    job.message = "Fetching latest jailbreak prompts..."
    job.progress = 10
    
    # Simulate processing
    await asyncio.sleep(2)
    
    jailbreak_service = JailbreakService()
    prompts = await jailbreak_service.fetch_latest_prompts()
    
    job.progress = 30
    job.message = "Applying jailbreak prompts..."
    
    # Simulate fine-tuning process
    for i in range(30, 100, 10):
        job.progress = i
        job.message = f"Fine-tuning with jailbreak prompts... ({i}%)"
        await asyncio.sleep(1)
    
    job.status = "completed"
    job.progress = 100.0
    job.message = "Jailbreak fine-tuning completed successfully"
    job.completed_at = datetime.now()

async def _run_data_import_fine_tuning(job: FineTuneStatus, request: FineTuneRequest, service: FineTuningService):
    """Run data import fine-tuning."""
    job.status = "running"
    job.message = "Processing imported data..."
    job.progress = 20
    
    # Simulate data processing
    await asyncio.sleep(3)
    
    job.progress = 50
    job.message = "Training model with custom data..."
    
    # Simulate training
    for i in range(50, 100, 10):
        job.progress = i
        job.message = f"Training with custom data... ({i}%)"
        await asyncio.sleep(1.5)
    
    job.status = "completed"
    job.progress = 100.0
    job.message = "Data import fine-tuning completed successfully"
    job.completed_at = datetime.now()

async def _run_general_fine_tuning(job: FineTuneStatus, request: FineTuneRequest, service: FineTuningService):
    """Run general fine-tuning with user feedback."""
    job.status = "running"
    job.message = "Preparing training data..."
    job.progress = 15
    
    # Simulate data preparation
    await asyncio.sleep(2)
    
    job.progress = 40
    job.message = "Training with user feedback..."
    
    # Simulate training with feedback
    for i in range(40, 100, 10):
        job.progress = i
        job.message = f"Training with user feedback... ({i}%)"
        await asyncio.sleep(1.2)
    
    job.status = "completed"
    job.progress = 100.0
    job.message = "General fine-tuning completed successfully"
    job.completed_at = datetime.now()
