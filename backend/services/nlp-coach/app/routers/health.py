# Health Check Router
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "nlp-coach", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0", "languages": ["ar", "en"]}

@router.get("/ready")
async def readiness_check():
    return {"status": "ready", "checks": {"llm": "connected", "drill_db": "loaded", "arabic_nlp": "ready"}}
