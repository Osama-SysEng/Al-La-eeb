# Al-La'eeb Shared Configuration - Enhanced Security Edition
import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Al-La'eeb"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Security - Hardened
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ISSUER: str = "allaeeb-auth"
    JWT_AUDIENCE: str = "allaeeb-api"

    # Password Policy
    MIN_PASSWORD_LENGTH: int = 10
    REQUIRE_SPECIAL_CHAR: bool = True
    REQUIRE_NUMBER: bool = True
    REQUIRE_UPPERCASE: bool = True
    BCRYPT_ROUNDS: int = 12

    # Rate Limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Database
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "allaeeb")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "allaeeb")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30

    # Vector Database (Qdrant)
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "qdrant")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "player_embeddings")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

    # AI/ML
    MEDIAPIPE_MODEL_PATH: str = os.getenv("MEDIAPIPE_MODEL_PATH", "/models/pose_landmarker.task")
    FACE_RECOGNITION_MODEL: str = os.getenv("FACE_RECOGNITION_MODEL", "buffalo_l")
    NLP_MODEL: str = os.getenv("NLP_MODEL", "gpt-4o")

    # Streaming
    RTMP_INGEST_URL: str = os.getenv("RTMP_INGEST_URL", "rtmp://localhost:1935/live")
    STREAM_SEGMENT_DURATION: int = 4
    MAX_CONCURRENT_STREAMS: int = 1000
    STREAM_BITRATE_LIMIT_KBPS: int = 8000

    # Object Storage
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "allaeeb-videos")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "")
    S3_REGION: str = os.getenv("S3_REGION", "us-east-1")
    S3_PRESIGNED_URL_EXPIRY: int = 3600

    # Geofencing
    GEOFENCE_MAX_DISTANCE_METERS: float = 50.0
    GPS_ACCURACY_THRESHOLD: float = 10.0
    GEOFENCE_MAX_ACCURACY_METERS: float = 20.0

    # Performance
    MAX_UPLOAD_SIZE_MB: int = 2048
    VIDEO_PROCESSING_TIMEOUT: int = 240
    CV_FPS_TARGET: int = 30
    CV_KEYPOINTS: int = 33
    MAX_VIDEO_DURATION_MINUTES: int = 120
    VIDEO_RETENTION_DAYS: int = 90
    VIDEO_MAX_RETRIES: int = 3
    REQUIRE_VIDEO_ANALYSIS_CONSENT: bool = True
    REQUIRE_SIGNED_UPLOAD_URLS_IN_PRODUCTION: bool = True

    # Audit Logging
    AUDIT_LOG_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 90

    # CORS
    CORS_ALLOWED_ORIGINS: str = os.getenv("CORS_ALLOWED_ORIGINS", "https://allaeeb.com")
    CORS_ALLOWED_METHODS: str = "GET,POST,PUT,DELETE,PATCH,OPTIONS"
    CORS_MAX_AGE: int = 86400

    # Content Security
    ALLOWED_FILE_TYPES: List[str] = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/webm"]
    MAX_FILE_NAME_LENGTH: int = 255

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
