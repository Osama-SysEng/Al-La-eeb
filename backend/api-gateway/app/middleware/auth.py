# Auth Middleware
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from shared.config.settings import get_settings

settings = get_settings()

class AuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS = ["/api/v1/auth/login", "/api/v1/auth/register", "/health", "/docs", "/openapi.json"]

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in self.PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authentication token")

        token = auth_header.replace("Bearer ", "")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            request.state.user = payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
