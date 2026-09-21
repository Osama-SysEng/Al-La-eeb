# Player Service - Enterprise Scale with Caching
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager
import logging
import uvicorn

from shared.models.domain import PlayerProfileResponse, PlayerPosition
from shared.config.settings import get_settings
from shared.utils.redis_client import get_redis

settings = get_settings()
logger = logging.getLogger("player-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("👤 Player Service starting - Enterprise Mode")
    redis = await get_redis()
    FastAPICache.init(RedisBackend(redis), prefix="allaeeb-cache")
    yield
    logger.info("👤 Player Service shutting down...")

app = FastAPI(title="Al-La'eeb Player Service", version="2.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"service": "Player Service", "version": "2.0.0", "status": "operational", "cache": "redis"}

@app.get("/api/v1/players/search")
@cache(expire=300)  # 5 minute cache
async def search_players(
    query: str = Query(None, description="Search by name or club"),
    position: PlayerPosition = Query(None),
    country: str = Query(None),
    min_score: float = Query(0, ge=0, le=100),
    max_age: int = Query(None),
    is_scoutable: bool = Query(True),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Search players with full-text search, filters, and pagination
    Cached for 5 minutes
    """
    # Mock results - in production query PostgreSQL with pg_trgm
    total = 1247
    players = [
        {
            "id": "player-" + str(i),
            "full_name": f"Player {i}",
            "age": 17 + (i % 5),
            "position": position.value if position else "MID",
            "overall_score": 75.0 + (i % 15),
            "country": country or "UAE",
            "club": f"Club {i % 20}",
            "is_verified": True
        }
        for i in range((page - 1) * page_size, page * page_size)
    ]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "players": players,
        "filters_applied": {
            "query": query,
            "position": position.value if position else None,
            "country": country,
            "min_score": min_score
        }
    }

@app.get("/api/v1/players/{player_id}")
@cache(expire=600)  # 10 minute cache for profiles
async def get_player(player_id: str):
    """Get player profile with caching"""
    return PlayerProfileResponse(
        id=uuid.UUID(player_id) if "-" in player_id else uuid.uuid4(),
        user_id=uuid.uuid4(),
        height_cm=182.5,
        weight_kg=78.0,
        dominant_foot="right",
        primary_position=PlayerPosition.MIDFIELDER,
        secondary_positions=[PlayerPosition.ATTACKING_MIDFIELDER, PlayerPosition.WINGER],
        current_club="Al-Ahli FC",
        current_academy="Elite Youth Academy",
        jersey_number=10,
        biography="Dynamic midfielder with excellent vision and passing range. Known for creating chances from deep positions.",
        achievements=["U-17 National Champion 2024", "Best Midfielder - Youth League", "Most Assists 2024"],
        video_highlight_url="https://cdn.allaeeb.com/highlights/player123.mp4",
        overall_score=78.5,
        potential_score=86.2,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

@app.get("/api/v1/players/{player_id}/stats")
@cache(expire=300)
async def get_player_stats(player_id: str):
    """Get comprehensive player statistics"""
    return {
        "player_id": player_id,
        "career_summary": {
            "matches_analyzed": 47,
            "total_minutes": 4230,
            "avg_rating": 78.5,
            "best_rating": 89.2,
            "trend": "improving",
            "consistency": 82.3
        },
        "physical": {
            "avg_speed_kmh": 7.8,
            "max_speed_kmh": 32.4,
            "total_distance_km": 324.5,
            "sprints_per_match": 16.2,
            "jump_height_cm": 58.3
        },
        "technical": {
            "pass_accuracy": 87.3,
            "passes_per_match": 42.5,
            "shot_accuracy": 48.2,
            "shots_per_match": 3.1,
            "dribble_success": 72.1,
            "touches_per_match": 67.8
        },
        "tactical": {
            "positioning_score": 78.5,
            "tactical_awareness": 74.2,
            "defensive_actions_per_match": 8.3,
            "interceptions_per_match": 4.1,
            "pressing_efficiency": 68.5
        },
        "recent_matches": [
            {"match": "vs Al-Hilal", "rating": 84.2, "date": "2024-07-28", "minutes": 90},
            {"match": "vs Al-Nassr", "rating": 81.5, "date": "2024-07-21", "minutes": 85},
            {"match": "vs Al-Ittihad", "rating": 79.8, "date": "2024-07-14", "minutes": 90},
            {"match": "vs Al-Shabab", "rating": 83.1, "date": "2024-07-07", "minutes": 78},
            {"match": "vs Al-Fateh", "rating": 80.5, "date": "2024-06-30", "minutes": 90}
        ]
    }

@app.get("/api/v1/players/{player_id}/timeline")
@cache(expire=180)
async def get_player_timeline(player_id: str, limit: int = Query(50, ge=1, le=200)):
    """Get player career timeline"""
    return {
        "player_id": player_id,
        "events": [
            {"date": "2024-07-28", "type": "match", "title": "vs Al-Hilal", "rating": 84.2},
            {"date": "2024-07-25", "type": "training", "title": "Sprint Training", "improvement": "+2.3%"},
            {"date": "2024-07-21", "type": "match", "title": "vs Al-Nassr", "rating": 81.5},
            {"date": "2024-07-18", "type": "milestone", "title": "1000 Passes Completed", "icon": "trophy"},
            {"date": "2024-07-14", "type": "match", "title": "vs Al-Ittihad", "rating": 79.8},
        ]
    }

import uuid
from datetime import datetime

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, workers=6)
