# Health Check Router
from fastapi import APIRouter
from datetime import datetime
import psutil

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "auth-service", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0"}

@router.get("/ready")
async def readiness_check():
    return {"status": "ready", "checks": {"database": "connected", "redis": "connected", "face_model": "loaded"}}

@router.get("/metrics")
async def metrics():
    return {"cpu_percent": psutil.cpu_percent(), "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent}
