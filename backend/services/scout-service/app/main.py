# Scout Service - Enterprise Discovery Engine
from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
import logging
import uvicorn

from shared.models.domain import PlayerDiscoveryCard, PlayerPosition
from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("scout-service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔍 Scout Service starting - Discovery Engine")
    yield
    logger.info("🔍 Scout Service shutting down...")

app = FastAPI(title="Al-La'eeb Scout Service", version="2.0.0", lifespan=lifespan)

@app.get("/")
async def root():
    return {"service": "Scout Service", "version": "2.0.0", "status": "operational", "vector_db": "qdrant"}

@app.post("/api/v1/scout/search")
async def search_players(
    positions: list[PlayerPosition] = Query(default=[]),
    age_min: int = Query(14, ge=14, le=35),
    age_max: int = Query(21, ge=14, le=35),
    country: str = Query(None),
    min_overall_score: float = Query(70, ge=0, le=100),
    max_overall_score: float = Query(100, ge=0, le=100),
    dominant_foot: str = Query(None),
    verified_only: bool = Query(True),
    sort_by: str = Query("overall_score", enum=["overall_score", "potential_score", "age", "recent_activity"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """
    Advanced player discovery with vector similarity search
    """
    import uuid
    from datetime import datetime

    total = 347

    # Mock vector search results
    players = [
        PlayerDiscoveryCard(
            player_id=uuid.uuid4(),
            full_name="Omar Al-Farsi",
            age=17,
            primary_position=PlayerPosition.MIDFIELDER,
            overall_score=81.2,
            potential_score=89.5,
            country="UAE",
            club="Al-Ain FC",
            highlight_video_url="https://cdn.allaeeb.com/omar.mp4",
            match_count=32,
            last_active=datetime.utcnow(),
            similarity_to_search=0.92
        ),
        PlayerDiscoveryCard(
            player_id=uuid.uuid4(),
            full_name="Khalid Al-Mansouri",
            age=16,
            primary_position=PlayerPosition.STRIKER,
            overall_score=76.8,
            potential_score=88.1,
            country="Saudi Arabia",
            club="Al-Hilal Youth",
            highlight_video_url="https://cdn.allaeeb.com/khalid.mp4",
            match_count=28,
            last_active=datetime.utcnow(),
            similarity_to_search=0.87
        ),
        PlayerDiscoveryCard(
            player_id=uuid.uuid4(),
            full_name="Youssef Benali",
            age=18,
            primary_position=PlayerPosition.WINGER,
            overall_score=79.3,
            potential_score=87.2,
            country="Morocco",
            club="Wydad AC",
            highlight_video_url="https://cdn.allaeeb.com/youssef.mp4",
            match_count=45,
            last_active=datetime.utcnow(),
            similarity_to_search=0.84
        ),
        PlayerDiscoveryCard(
            player_id=uuid.uuid4(),
            full_name="Ahmed Hassan",
            age=17,
            primary_position=PlayerPosition.CENTER_BACK,
            overall_score=74.5,
            potential_score=85.3,
            country="Egypt",
            club="Zamalek SC",
            highlight_video_url="https://cdn.allaeeb.com/ahmed.mp4",
            match_count=38,
            last_active=datetime.utcnow(),
            similarity_to_search=0.81
        ),
        PlayerDiscoveryCard(
            player_id=uuid.uuid4(),
            full_name="Faisal Al-Rashid",
            age=19,
            primary_position=PlayerPosition.GOALKEEPER,
            overall_score=77.1,
            potential_score=84.9,
            country="Qatar",
            club="Al-Sadd SC",
            highlight_video_url="https://cdn.allaeeb.com/faisal.mp4",
            match_count=41,
            last_active=datetime.utcnow(),
            similarity_to_search=0.79
        ),
    ]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "players": players,
        "search_params": {
            "positions": [p.value for p in positions] if positions else None,
            "age_range": [age_min, age_max],
            "country": country,
            "min_score": min_overall_score,
            "sort_by": sort_by
        }
    }

@app.get("/api/v1/scout/player/{player_id}/detailed")
async def get_detailed_profile(player_id: str):
    """Get comprehensive player profile for scouts"""
    return {
        "player_id": player_id,
        "detailed_metrics": {
            "physical": {"speed": 85, "strength": 72, "agility": 88, "endurance": 79, "jump": 76},
            "technical": {"passing": 91, "shooting": 76, "dribbling": 84, "first_touch": 89, "heading": 71},
            "tactical": {"positioning": 82, "awareness": 87, "vision": 90, "decisions": 78, "anticipation": 85},
            "mental": {"composure": 75, "leadership": 68, "work_rate": 85, "consistency": 80, "aggression": 72}
        },
        "radar_chart_data": {
            "labels": ["Speed", "Passing", "Shooting", "Dribbling", "Defense", "Physical"],
            "values": [85, 91, 76, 84, 78, 79]
        },
        "scout_notes": [
            {"scout": "Ahmed Hassan", "club": "Man City Academy", "note": "Exceptional vision, needs to improve defensive work rate", "date": "2024-07-15", "rating": 8.5},
            {"scout": "John Smith", "club": "Liverpool FC", "note": "Premier League potential, recommend trial immediately", "date": "2024-07-20", "rating": 9.0},
            {"scout": "Carlos Mendez", "club": "Real Madrid", "note": "Great technique but needs more physical development", "date": "2024-07-25", "rating": 7.8}
        ],
        "similar_players": [
            {"name": "Mohamed Salah", "similarity": 0.87, "position": "RW", "club": "Liverpool"},
            {"name": "Riyad Mahrez", "similarity": 0.82, "position": "RW", "club": "Al-Ahli"},
            {"name": "Sadio Mane", "similarity": 0.79, "position": "LW", "club": "Al-Nassr"}
        ],
        "video_analysis_available": True,
        "contact_status": "available_for_contact"
    }

@app.post("/api/v1/scout/favorite/{player_id}")
async def favorite_player(player_id: str, scout_id: str):
    """Add player to scout favorites"""
    return {"player_id": player_id, "scout_id": scout_id, "action": "favorited", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/v1/scout/recommendations")
async def get_recommendations(scout_id: str, limit: int = Query(10, ge=1, le=50)):
    """AI-powered player recommendations for scouts"""
    return {
        "scout_id": scout_id,
        "recommendations": [
            {"player_id": "rec-1", "reason": "Matches your search history for creative midfielders", "confidence": 0.94},
            {"player_id": "rec-2", "reason": "Rising star in your target region", "confidence": 0.89},
            {"player_id": "rec-3", "reason": "Similar profile to players you've contacted", "confidence": 0.87}
        ],
        "generated_at": datetime.utcnow().isoformat()
    }

from datetime import datetime

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005, workers=4)
