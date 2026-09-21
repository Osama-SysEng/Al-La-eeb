# Enhanced Database Configuration with Connection Pooling & Sharding
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import event
import logging

from shared.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("database")

# Primary Database Engine with aggressive pooling for high concurrency
primary_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=QueuePool,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    connect_args={
        "command_timeout": 60,
        "server_settings": {
            "jit": "off",
            "application_name": "allaeeb_primary"
        }
    }
)

# Read Replica Engine (for analytics, scout searches)
read_replica_url = settings.DATABASE_URL.replace("@", "-replica@") if "localhost" in settings.DATABASE_URL else settings.DATABASE_URL
read_engine = create_async_engine(
    read_replica_url,
    echo=False,
    poolclass=QueuePool,
    pool_size=50,
    max_overflow=100,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={"command_timeout": 120, "server_settings": {"application_name": "allaeeb_read"}}
)

AsyncSessionLocal = async_sessionmaker(
    primary_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

ReadOnlySessionLocal = async_sessionmaker(
    read_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

# Connection event listeners for monitoring
@event.listens_for(primary_engine.sync_engine, "connect")
def on_connect(dbapi_conn, connection_record):
    logger.debug("New database connection established")

@event.listens_for(primary_engine.sync_engine, "checkout")
def on_checkout(dbapi_conn, connection_record, connection_proxy):
    logger.debug("Database connection checked out from pool")

async def get_db():
    """Primary database session for writes"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database transaction failed: {e}")
            raise
        finally:
            await session.close()

async def get_read_db():
    """Read-only database session for queries"""
    async with ReadOnlySessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

class DatabaseMetrics:
    """Track database performance metrics"""

    @staticmethod
    async def get_pool_status():
        return {
            "primary_pool_size": primary_engine.pool.size(),
            "primary_checked_in": primary_engine.pool.checkedin(),
            "primary_checked_out": primary_engine.pool.checkedout(),
            "primary_overflow": primary_engine.pool.overflow(),
        }
