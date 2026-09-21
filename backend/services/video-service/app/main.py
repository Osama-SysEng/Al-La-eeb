# Video Service
from fastapi import FastAPI, UploadFile, File, Form
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🎥 Video Service starting...")
    yield
    print("🎥 Video Service shutting down...")

app = FastAPI(title="Al-La'eeb Video Service", version="1.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"service": "Video Service", "status": "operational"}

@app.post("/api/v1/videos/upload")
async def upload_video(
    file: UploadFile = File(...),
    player_id: str = Form(...),
    title: str = Form(...)
):
    return {
        "message": "Video uploaded successfully",
        "filename": file.filename,
        "player_id": player_id,
        "title": title,
        "status": "processing"
    }

@app.get("/api/v1/videos/{video_id}/stream")
async def get_stream(video_id: str):
    return {
        "video_id": video_id,
        "hls_url": f"https://cdn.allaeeb.com/stream/{video_id}/playlist.m3u8",
        "dash_url": f"https://cdn.allaeeb.com/stream/{video_id}/manifest.mpd",
        "rtmp_ingest": f"rtmp://live.allaeeb.com/live/{video_id}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
