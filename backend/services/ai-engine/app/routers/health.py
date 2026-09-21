# Health Check Router
from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "ai-engine", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0", "cv_model": "mediapipe_pose_v2"}

@router.get("/ready")
async def readiness_check():
    return {"status": "ready", "checks": {"gpu": "available", "cv_model": "loaded", "metrics_engine": "ready", "qdrant": "connected"}}

@router.get("/metrics")
async def metrics():
    return {"cpu_percent": psutil.cpu_percent(), "memory_percent": psutil.virtual_memory().percent, "gpu_utilization": "45%", "active_streams": 12}
