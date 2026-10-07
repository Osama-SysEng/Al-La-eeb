# Redis Client
import redis.asyncio as redis
from shared.config.settings import get_settings

settings = get_settings()

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    max_connections=50,
    protocol=2,  # RESP2: compatible with Redis 5+ (redis-py 5 defaults to RESP3/HELLO)
)

async def get_redis():
    # Fresh client per call: safe across event loops (TestClient portals,
    # workers). For high throughput, replace with a loop-bound pool.
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
        protocol=2,
    )

class CacheKeys:
    @staticmethod
    def user_session(user_id: str) -> str:
        return f"session:{user_id}"

    @staticmethod
    def video_processing(video_id: str) -> str:
        return f"processing:{video_id}"

    @staticmethod
    def player_metrics(player_id: str) -> str:
        return f"metrics:{player_id}"

    @staticmethod
    def rate_limit(ip: str) -> str:
        return f"ratelimit:{ip}"

    @staticmethod
    def stream_stats(stream_id: str) -> str:
        return f"stream:{stream_id}"
