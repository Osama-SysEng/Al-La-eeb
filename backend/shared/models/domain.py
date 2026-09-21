# Al-La'eeb Domain Models
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, UUID4
from uuid import uuid4

class UserRole(str, Enum):
    PLAYER = "player"
    PARENT = "parent"
    COACH = "coach"
    SCOUT = "scout"
    CLUB = "club"
    ACADEMY = "academy"
    TOURNAMENT_ORGANIZER = "tournament_organizer"
    ADMIN = "admin"

class PlayerPosition(str, Enum):
    GOALKEEPER = "GK"
    DEFENDER = "DEF"
    MIDFIELDER = "MID"
    FORWARD = "FWD"
    WINGER = "WNG"
    FULLBACK = "FB"
    CENTER_BACK = "CB"
    DEFENSIVE_MIDFIELDER = "CDM"
    ATTACKING_MIDFIELDER = "CAM"
    STRIKER = "ST"

class MatchStatus(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class VerificationStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    MANUAL_REVIEW = "manual_review"

# ============== USER MODELS ==============

class UserBase(BaseModel):
    email: str
    phone: Optional[str] = None
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool = True
    is_verified: bool = False
    country: Optional[str] = None
    city: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    profile_image_url: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============== PLAYER MODELS ==============

class PlayerProfileBase(BaseModel):
    user_id: UUID4
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    dominant_foot: Optional[str] = Field(None, pattern="^(left|right|both)$")
    primary_position: Optional[PlayerPosition] = None
    secondary_positions: List[PlayerPosition] = []
    current_club: Optional[str] = None
    current_academy: Optional[str] = None
    jersey_number: Optional[int] = Field(None, ge=1, le=99)
    biography: Optional[str] = None
    achievements: List[str] = []
    video_highlight_url: Optional[str] = None

class PlayerProfileCreate(PlayerProfileBase):
    pass

class PlayerProfileResponse(PlayerProfileBase):
    id: UUID4
    overall_score: Optional[float] = None
    potential_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============== MATCH/VIDEO MODELS ==============

class VideoUploadBase(BaseModel):
    player_id: UUID4
    title: str
    description: Optional[str] = None
    match_type: str = Field(..., pattern="^(full_match|highlights|training|trial)$")
    opponent: Optional[str] = None
    match_date: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    file_size_bytes: Optional[int] = None
    file_format: Optional[str] = None
    resolution: Optional[str] = None
    fps: Optional[int] = None

class VideoUploadCreate(VideoUploadBase):
    pass

class VideoUploadResponse(VideoUploadBase):
    id: UUID4
    status: MatchStatus
    storage_url: Optional[str] = None
    stream_url: Optional[str] = None
    processing_progress: float = 0.0
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============== PERFORMANCE METRICS ==============

class SkeletalKeypoints(BaseModel):
    frame_id: int
    timestamp_ms: float
    keypoints: List[Dict[str, float]]  # 33 keypoints with x,y,z,visibility
    player_id: Optional[str] = None

class PerformanceMetrics(BaseModel):
    video_id: UUID4
    player_id: UUID4

    # Physical
    max_speed_kmh: Optional[float] = None
    avg_speed_kmh: Optional[float] = None
    total_distance_m: Optional[float] = None
    sprint_count: Optional[int] = None
    max_acceleration_ms2: Optional[float] = None
    jump_height_cm: Optional[float] = None
    metabolic_load: Optional[float] = None

    # Technical
    pass_accuracy: Optional[float] = None
    pass_count: Optional[int] = None
    shot_accuracy: Optional[float] = None
    shot_count: Optional[int] = None
    dribble_success_rate: Optional[float] = None
    touch_count: Optional[int] = None

    # Tactical
    positioning_score: Optional[float] = None
    tactical_awareness: Optional[float] = None
    defensive_actions: Optional[int] = None
    interceptions: Optional[int] = None

    # Biomechanical
    strike_biomechanics: Optional[float] = None
    center_of_mass_stability: Optional[float] = None
    limb_symmetry: Optional[float] = None

    # Overall
    overall_rating: Optional[float] = None
    percentile_vs_professionals: Optional[float] = None

    class Config:
        from_attributes = True

# ============== AI COACH MODELS ==============

class DrillRecommendation(BaseModel):
    drill_id: str
    drill_name: str
    category: str
    difficulty: str
    duration_minutes: int
    target_skill: str
    description: str
    video_url: Optional[str] = None
    frequency_per_week: int = 3

class CoachingReport(BaseModel):
    id: UUID4
    player_id: UUID4
    video_id: UUID4
    generated_at: datetime

    # Analysis
    strengths: List[str]
    weaknesses: List[str]
    key_moments: List[Dict[str, Any]]

    # Comparison
    similar_professionals: List[Dict[str, Any]]
    similarity_score: float

    # Recommendations
    drills: List[DrillRecommendation]
    weekly_plan: Dict[str, Any]

    # NLP Output
    coach_feedback_ar: Optional[str] = None
    coach_feedback_en: Optional[str] = None

    class Config:
        from_attributes = True

# ============== SCOUT/CLUB MODELS ==============

class ScoutSearchFilter(BaseModel):
    positions: List[PlayerPosition] = []
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    country: Optional[str] = None
    min_overall_score: Optional[float] = None
    dominant_foot: Optional[str] = None
    verified_only: bool = True

class PlayerDiscoveryCard(BaseModel):
    player_id: UUID4
    full_name: str
    age: Optional[int] = None
    primary_position: PlayerPosition
    overall_score: float
    potential_score: float
    country: str
    club: Optional[str] = None
    highlight_video_url: Optional[str] = None
    match_count: int
    last_active: datetime
    similarity_to_search: Optional[float] = None

# ============== AUTH MODELS ==============

class TokenPayload(BaseModel):
    sub: str  # user_id
    role: UserRole
    exp: datetime
    jti: str = Field(default_factory=lambda: str(uuid4()))

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class FaceVerificationRequest(BaseModel):
    player_id: UUID4
    image_base64: str
    jersey_number: int = Field(..., ge=1, le=99)
    kit_color_primary: str
    kit_color_secondary: Optional[str] = None
    gps_latitude: float
    gps_longitude: float
    gps_accuracy: float

class FaceVerificationResult(BaseModel):
    player_id: UUID4
    face_match_score: float
    kit_match_score: float
    overall_confidence: float
    verification_status: VerificationStatus
    processing_time_ms: float
    anti_fraud_passed: bool
    geofence_valid: bool
    timestamp: datetime
