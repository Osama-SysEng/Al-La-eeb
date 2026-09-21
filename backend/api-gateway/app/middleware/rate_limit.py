# Rate Limiting Middleware - Enhanced
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from shared.utils.redis_client import get_redis, CacheKeys
from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("rate-limiter")

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests_per_minute = settings.RATE_LIMIT_REQUESTS_PER_MINUTE
        self.burst_limit = settings.RATE_LIMIT_BURST
        self.window = settings.RATE_LIMIT_WINDOW_SECONDS

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/api/v1/health/all"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        user_id = getattr(request.state, "user", {}).get("sub", "anonymous")

        redis = await get_redis()

        # Per-IP rate limiting
        ip_key = f"ratelimit:ip:{client_ip}"
        ip_count = await redis.get(ip_key)

        if ip_count and int(ip_count) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": self.requests_per_minute,
                    "window": f"{self.window}s",
                    "retry_after": await redis.ttl(ip_key)
                }
            )

        # Per-user rate limiting (stricter)
        if user_id != "anonymous":
            user_key = f"ratelimit:user:{user_id}"
            user_count = await redis.get(user_key)
            if user_count and int(user_count) >= self.requests_per_minute * 2:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "User rate limit exceeded",
                        "limit": self.requests_per_minute * 2,
                        "retry_after": await redis.ttl(user_key)
                    }
                )

            pipe = redis.pipeline()
            pipe.incr(user_key)
            pipe.expire(user_key, self.window)
            await pipe.execute()

        # Increment IP counter
        pipe = redis.pipeline()
        pipe.incr(ip_key)
        pipe.expire(ip_key, self.window)
        await pipe.execute()

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Window"] = str(self.window)

        return response
