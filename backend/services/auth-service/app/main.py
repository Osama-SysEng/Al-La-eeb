# Auth Service - Enterprise Scale
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.routers import auth, verification, health
from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("auth-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔐 Auth Service starting - Enterprise Mode")
    logger.info(f"Pool size: {settings.DATABASE_POOL_SIZE}, Max overflow: {settings.DATABASE_MAX_OVERFLOW}")
    yield
    logger.info("🔐 Auth Service shutting down...")

app = FastAPI(
    title="Al-La'eeb Auth Service",
    description="Enterprise Authentication & Biometric Verification",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(verification.router, prefix="/api/v1/verification", tags=["Biometric Verification"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])

@app.get("/")
async def root():
    return {
        "service": "Al-La'eeb Auth Service",
        "version": "2.0.0",
        "status": "operational",
        "capacity": "1M+ users",
        "features": ["JWT", "Biometric", "RBAC", "Audit"]
    }

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8001,
        workers=8,
        limit_concurrency=1000,
        backlog=2048
    )
