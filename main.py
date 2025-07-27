from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pathlib import Path
from src.routers import models, fine_tuning, hardware, data_import
from src.services.hardware_detector import HardwareDetector

app = FastAPI(
    title="Ollama Fine-Tuning Studio",
    description="Modern web interface for fine-tuning Ollama models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(models.router, prefix="/api/models", tags=["models"])
app.include_router(fine_tuning.router, prefix="/api/fine-tune", tags=["fine-tuning"])
app.include_router(hardware.router, prefix="/api/hardware", tags=["hardware"])
app.include_router(data_import.router, prefix="/api/data", tags=["data"])

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path("static/index.html")
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(), status_code=200)
    return HTMLResponse(content="<h1>Ollama Fine-Tuning Studio</h1><p>UI loading...</p>")

@app.on_event("startup")
async def startup_event():
    # Initialize hardware detection
    detector = HardwareDetector()
    hardware_info = await detector.detect_hardware()
    print(f"Hardware detected: {hardware_info}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
