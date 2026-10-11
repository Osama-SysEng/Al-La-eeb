# Scaling — Al-La-eeb backend

## Workers
- All `infrastructure/docker/Dockerfile.*` already run uvicorn with
  `--workers 2–4` (gateway/auth 4, others 2+). No change needed.
- Services are stateless FastAPI; scale replicas behind the gateway.

## Rate limiting
- Already present: `backend/api-gateway/app/middleware/rate_limit.py`
  (`RateLimitMiddleware`, `X-RateLimit-*` headers) wired in
  `backend/api-gateway/app/main.py`. No change needed.

## Pagination
- Already present: player search & scout search (`page/page_size`, max 100),
  recommendations & timeline (`limit`, max 50/200).
- Added: `GET /drills?limit=&offset=` (default 50, max 500) for category
  filtering; unfiltered library response unchanged (small static set).

## Remaining capacity limits (honest)
- AI/video inference is CPU/GPU bound; workers help I/O, not model latency —
  use a task queue (Celery/RQ) + GPU pool for match analysis at scale.
- Redis-backed cache (`fastapi_cache`) is per-service; no shared CDN.
- Mock datasets in search endpoints stand in for Postgres+pg_trgm/Qdrant;
  real stores needed before load testing numbers are meaningful.
