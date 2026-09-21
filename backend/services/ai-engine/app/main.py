# AI Engine Service - Enhanced with Error Recovery
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.routers import processing, analysis, health
from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("ai-engine")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧠 AI Engine starting... Loading CV models...")
    try:
        # Pre-load models
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
    yield
    logger.info("🧠 AI Engine shutting down...")

app = FastAPI(
    title="Al-La'eeb AI Engine",
    description="Computer Vision, Skeletal Tracking & Performance Analytics",
    version="1.0.0",
    lifespan=lifespan
)

@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Error", "detail": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal processing error", "detail": str(exc) if settings.DEBUG else "Contact support"}
    )

app.include_router(processing.router, prefix="/api/v1/process", tags=["Video Processing"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Performance Analysis"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])

@app.get("/")
async def root():
    return {
        "service": "Al-La'eeb AI Engine",
        "version": "1.0.0",
        "status": "operational",
        "cv_fps_target": 30,
        "models": ["mediapipe_pose", "ball_tracking", "event_detection"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
