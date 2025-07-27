from fastapi import APIRouter
from src.services.hardware_detector import HardwareDetector

router = APIRouter()

@router.get("/detect")
async def detect_hardware():
    """Detect system hardware capabilities."""
    detector = HardwareDetector()
    return await detector.detect_hardware()

@router.get("/config")
async def get_training_config():
    """Get optimal training configuration based on hardware."""
    detector = HardwareDetector()
    await detector.detect_hardware()  # Ensure hardware is detected
    return detector.get_training_config()
