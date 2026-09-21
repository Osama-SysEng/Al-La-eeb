# NLP Coach Service - FastAPI Application
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from app.routers import coach, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🗣️ NLP Coach Service starting... Loading language models...")
    yield
    print(f"🗣️ NLP Coach Service shutting down...")

app = FastAPI(
    title="Al-La'eeb NLP Virtual Coach",
    description="Arabic/English AI Coach with 500+ Drill Library",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(coach.router, prefix="/api/v1/coach", tags=["Virtual Coach"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Health"])

@app.get("/")
async def root():
    return {"service": "Al-La'eeb NLP Virtual Coach", "version": "1.0.0", "languages": ["ar", "en"], "drill_library": 500}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
