# API Gateway - Enhanced Security & Error Handling
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import RequestValidationError
import httpx
import time
import logging
import traceback
from contextlib import asynccontextmanager
from typing import Dict, Any

from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.auth import AuthMiddleware
from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("api-gateway")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🌐 API Gateway starting with enhanced security...")
    yield
    logger.info("🌐 API Gateway shutting down...")

app = FastAPI(
    title="Al-La'eeb API Gateway",
    description="Unified API Gateway with enterprise security",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
    redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
)

# Security Headers Middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(self), camera=(self), microphone=(self)"
    return response

# CORS - Strict in production
allowed_origins = settings.CORS_ALLOWED_ORIGINS.split(",") if settings.CORS_ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOWED_METHODS.split(","),
    allow_headers=["*"],
    max_age=settings.CORS_MAX_AGE,
)

# Rate Limiting
app.add_middleware(RateLimitMiddleware)

# Auth Middleware
app.add_middleware(AuthMiddleware)

SERVICES: Dict[str, str] = {
    "auth": "http://auth-service:8001",
    "player": "http://player-service:8002",
    "ai": "http://ai-engine:8003",
    "coach": "http://nlp-coach:8004",
    "scout": "http://scout-service:8005",
    "video": "http://video-service:8006",
}

# Request timing and logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.time()
    request_id = request.headers.get("X-Request-ID", f"req-{int(time.time() * 1000)}")

    logger.info(f"[{request_id}] {request.method} {request.url.path} from {request.client.host}")

    try:
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{duration:.3f}s"
        response.headers["X-Gateway-Version"] = "1.0.0"

        logger.info(f"[{request_id}] {response.status_code} in {duration:.3f}s")
        return response

    except Exception as e:
        duration = time.time() - start
        logger.error(f"[{request_id}] ERROR in {duration:.3f}s: {str(e)}")
        raise

# Global exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": exc.errors(),
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred" if settings.ENVIRONMENT == "production" else str(exc),
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )

async def proxy_request(
    service: str, 
    path: str, 
    method: str, 
    body: Any = None, 
    headers: Dict = None, 
    params: Dict = None,
    timeout: float = 60.0
) -> httpx.Response:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    async with httpx.AsyncClient(timeout=timeout) as client:
        url = f"{SERVICES[service]}{path}"
        req_headers = {k: v for k, v in (headers or {}).items() 
                      if k.lower() not in ["host", "content-length", "connection"]}

        try:
            if method == "GET":
                r = await client.get(url, headers=req_headers, params=params)
            elif method == "POST":
                r = await client.post(url, json=body, headers=req_headers, params=params)
            elif method == "PUT":
                r = await client.put(url, json=body, headers=req_headers, params=params)
            elif method == "DELETE":
                r = await client.delete(url, headers=req_headers, params=params)
            elif method == "PATCH":
                r = await client.patch(url, json=body, headers=req_headers, params=params)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return r

        except httpx.TimeoutException:
            logger.error(f"Timeout calling {service} at {path}")
            raise HTTPException(status_code=504, detail=f"Service '{service}' timeout")
        except httpx.ConnectError:
            logger.error(f"Cannot connect to {service}")
            raise HTTPException(status_code=503, detail=f"Service '{service}' unavailable")
        except Exception as e:
            logger.error(f"Error proxying to {service}: {e}")
            raise HTTPException(status_code=502, detail=f"Bad gateway to '{service}'")

@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    # Validate service name to prevent path traversal
    if not service.isalnum():
        raise HTTPException(status_code=400, detail="Invalid service name")

    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            body = await request.json()
        except Exception:
            body = await request.body()

    response = await proxy_request(
        service, f"/api/v1/{path}", request.method,
        body=body, headers=dict(request.headers), params=dict(request.query_params)
    )

    content_type = response.headers.get("content-type", "application/json")

    try:
        if "application/json" in content_type:
            return JSONResponse(
                content=response.json(), 
                status_code=response.status_code,
                headers={k: v for k, v in dict(response.headers).items() 
                        if k.lower() not in ["content-length", "transfer-encoding"]}
            )
        return StreamingResponse(
            response.aiter_raw(), 
            status_code=response.status_code, 
            media_type=content_type
        )
    except Exception as e:
        logger.error(f"Error processing response: {e}")
        raise HTTPException(status_code=500, detail="Error processing service response")

@app.get("/health")
async def health():
    return {
        "gateway": "healthy",
        "version": "1.0.0",
        "services": SERVICES,
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT
    }

@app.get("/api/v1/health/all")
async def health_all():
    results = {}
    for name, url in SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                start = time.time()
                r = await client.get(f"{url}/api/v1/health/")
                results[name] = {
                    "status": "healthy" if r.status_code == 200 else "degraded",
                    "response_time_ms": round((time.time() - start) * 1000, 2),
                    "status_code": r.status_code
                }
        except Exception as e:
            results[name] = {"status": "unhealthy", "error": str(e)}

    all_healthy = all(r.get("status") == "healthy" for r in results.values())
    return JSONResponse(
        content={"services": results, "all_healthy": all_healthy},
        status_code=200 if all_healthy else 503
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
