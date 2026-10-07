# Video Service
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from contextlib import asynccontextmanager
from datetime import datetime
import logging
import uvicorn

from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("video-service")

ALLOWED_VIDEO_TYPES = set(settings.ALLOWED_FILE_TYPES)
MAX_UPLOAD_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Video Service starting...")
    yield
    print("Video Service shutting down...")

app = FastAPI(title="Al-La'eeb Video Service", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"service": "Video Service", "status": "operational"}

@app.get("/api/v1/health/")
async def health_check():
    return {"status": "healthy", "service": "video-service", "timestamp": datetime.utcnow().isoformat(), "version": "1.0.0"}

@app.get("/api/v1/health/ready")
async def readiness_check():
    return {"status": "ready", "checks": {"storage": "configured", "cdn": "configured"}}

@app.post("/api/v1/videos/upload")
async def upload_video(
    file: UploadFile = File(...),
    player_id: str = Form(...),
    title: str = Form(...)
):
    if not player_id or not player_id.strip():
        raise HTTPException(status_code=400, detail="player_id is required")
    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="title is required")
    if len(title) > 255:
        raise HTTPException(status_code=400, detail="title too long (max 255 characters)")
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: {sorted(ALLOWED_VIDEO_TYPES)}",
        )
    if not file.filename or len(file.filename) > settings.MAX_FILE_NAME_LENGTH:
        raise HTTPException(status_code=400, detail="Invalid filename")
    try:
        contents = await file.read()
    except Exception as e:
        logger.error(f"Failed reading upload {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to read uploaded file")
    finally:
        await file.seek(0)
    if len(contents) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(contents)} bytes). Max {settings.MAX_UPLOAD_SIZE_MB}MB",
        )
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file upload")
    logger.info(f"Video upload accepted: {file.filename} ({len(contents)} bytes) for player {player_id}")
    return {
        "message": "Video uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "player_id": player_id,
        "title": title,
        "status": "processing"
    }

@app.get("/api/v1/videos/{video_id}/stream")
async def get_stream(video_id: str):
    if not video_id or not video_id.strip():
        raise HTTPException(status_code=400, detail="video_id is required")
    return {
        "video_id": video_id,
        "hls_url": f"https://cdn.allaeeb.com/stream/{video_id}/playlist.m3u8",
        "dash_url": f"https://cdn.allaeeb.com/stream/{video_id}/manifest.mpd",
        "rtmp_ingest": f"rtmp://live.allaeeb.com/live/{video_id}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
