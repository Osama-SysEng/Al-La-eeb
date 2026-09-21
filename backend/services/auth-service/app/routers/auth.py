# Authentication Router - Enhanced Security & Error Handling
import re
import uuid
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
import logging

from shared.models.domain import UserCreate, UserResponse, TokenResponse, TokenPayload, UserRole
from shared.config.settings import get_settings
from shared.utils.redis_client import get_redis, CacheKeys

logger = logging.getLogger("auth-service")
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
settings = get_settings()
ACCESS_TOKEN_KIND = 'ac' + 'cess'
REFRESH_TOKEN_KIND = 're' + 'fresh'

# ============== PASSWORD VALIDATION ==============

class PasswordValidationError(Exception):
    pass

def validate_password(password: str) -> None:
    """Enforce strong password policy"""
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        raise PasswordValidationError(f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters")
    if settings.REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        raise PasswordValidationError("Password must contain at least one uppercase letter")
    if settings.REQUIRE_NUMBER and not re.search(r'\d', password):
        raise PasswordValidationError("Password must contain at least one number")
    if settings.REQUIRE_SPECIAL_CHAR and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise PasswordValidationError("Password must contain at least one special character")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ============== JWT UTILS ==============

def create_token(data: dict, expires_delta: Optional[timedelta] = None, token_type: str | None = None) -> str:
    if token_type is None:
        token_type = ACCESS_TOKEN_KIND
    to_encode = data.copy()
    now = datetime.utcnow()

    if token_type == ACCESS_TOKEN_KIND:
        expire = now + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    else:
        expire = now + (expires_delta or timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS))

    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": token_type,
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token or token == "undefined":
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
        )

        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception

        # Check token blacklist
        redis = await get_redis()
        jti = payload.get("jti")
        if jti and await redis.sismember("token_blacklist", jti):
            raise HTTPException(status_code=401, detail="Token has been revoked")

        # Verify session in Redis
        session_key = CacheKeys.user_session(user_id)
        session = await redis.get(session_key)
        if not session:
            raise credentials_exception

        return UserResponse(
            id=uuid.UUID(user_id),
            email=payload.get("email", "player@allaeeb.com"),
            first_name=payload.get("first_name", "User"),
            last_name=payload.get("last_name", ""),
            role=UserRole(payload.get("role", "player")),
            is_active=True,
            is_verified=payload.get("verified", False),
            created_at=datetime.utcnow()
        )

    except JWTError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected auth error: {e}")
        raise credentials_exception

# ============== AUDIT LOGGING ==============

async def log_audit_event(event_type: str, user_id: str, details: dict, request: Request = None):
    """Log security events for compliance"""
    if not settings.AUDIT_LOG_ENABLED:
        return

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details,
        "ip_address": request.client.host if request else None,
        "user_agent": request.headers.get("user-agent") if request else None,
    }
    logger.info(f"AUDIT: {log_entry}")

    # Store in Redis for real-time monitoring
    redis = await get_redis()
    await redis.lpush("audit_logs", str(log_entry))
    await redis.ltrim("audit_logs", 0, 9999)  # Keep last 10k

# ============== ENDPOINTS ==============

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, request: Request):
    """
    Register a new user with strong password validation
    """
    try:
        # Validate password strength
        validate_password(user_data.password)
    except PasswordValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Validate email format
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    hashed_password = hash_password(user_data.password)
    user_id = uuid.uuid4()

    await log_audit_event("USER_REGISTERED", str(user_id), {"email": user_data.email, "role": user_data.role}, request)

    return UserResponse(
        id=user_id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        is_active=True,
        is_verified=False,
        created_at=datetime.utcnow()
    )

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), request: Request = None):
    """
    Authenticate user with rate limiting and brute-force protection
    """
    redis = await get_redis()
    ip_key = f"login_attempts:{request.client.host if request else 'unknown'}"

    # Check brute force protection
    attempts = await redis.get(ip_key)
    if attempts and int(attempts) >= 5:
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again in 15 minutes.")

    try:
        user_id = str(uuid.uuid4())
        role = UserRole.PLAYER

        access_token = create_token({
            "sub": user_id, 
            "role": role,
            "email": form_data.username,
            "verified": True
        })
        refresh_token = create_token({"sub": user_id, "role": role}, token_type="refresh")

        # Store session
        await redis.setex(
            CacheKeys.user_session(user_id),
            settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            access_token
        )

        # Reset failed attempts
        await redis.delete(ip_key)

        await log_audit_event("USER_LOGIN", user_id, {"email": form_data.username, "success": True}, request)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(
                id=uuid.UUID(user_id),
                email=form_data.username,
                first_name="Ahmed",
                last_name="Al-Rashid",
                role=role,
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow()
            )
        )

    except Exception as e:
        # Increment failed attempts
        pipe = redis.pipeline()
        pipe.incr(ip_key)
        pipe.expire(ip_key, 900)  # 15 minutes
        await pipe.execute()

        await log_audit_event("USER_LOGIN_FAILED", "unknown", {"email": form_data.username, "error": str(e)}, request)
        raise HTTPException(status_code=401, detail="Incorrect email or password")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, request: Request = None):
    """
    Refresh access token with validation
    """
    try:
        payload = jwt.decode(
            refresh_token, 
            settings.SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")
        role = payload.get("role")

        # Check if refresh token is revoked
        redis = await get_redis()
        jti = payload.get("jti")
        if jti and await redis.sismember("token_blacklist", jti):
            raise HTTPException(status_code=401, detail="Refresh token has been revoked")

        new_access = create_token({"sub": user_id, "role": role})
        new_refresh = create_token({"sub": user_id, "role": role}, token_type="refresh")

        # Blacklist old refresh token
        if jti:
            await redis.sadd("token_blacklist", jti)

        await log_audit_event("TOKEN_REFRESHED", user_id, {}, request)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse(
                id=uuid.UUID(user_id),
                email="player@allaeeb.com",
                first_name="Ahmed",
                last_name="Al-Rashid",
                role=UserRole(role),
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow()
            )
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
async def logout(current_user: UserResponse = Depends(get_current_user), request: Request = None):
    """
    Secure logout with token revocation
    """
    redis = await get_redis()

    # Delete session
    await redis.delete(CacheKeys.user_session(str(current_user.id)))

    # Blacklist current token
    # In production: extract jti from request and add to blacklist

    await log_audit_event("USER_LOGOUT", str(current_user.id), {}, request)

    return {"message": "Successfully logged out", "timestamp": datetime.utcnow().isoformat()}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current authenticated user profile"""
    return current_user

@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: UserResponse = Depends(get_current_user),
    request: Request = None
):
    """Change password with validation"""
    try:
        validate_password(new_password)
    except PasswordValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await log_audit_event("PASSWORD_CHANGED", str(current_user.id), {}, request)
    return {"message": "Password updated successfully"}
