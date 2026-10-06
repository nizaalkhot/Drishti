"""
Database Engine Configuration for Cloud SQL, AlloyDB, and Local Dev.
"""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.database.models import Base

# Database URL configuration:
# 1. CLOUD_SQL_CONNECTION_NAME or DATABASE_URL (PostgreSQL / AlloyDB)
# 2. Local fallback to async SQLite
def get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url
    
    # Check Cloud SQL / AlloyDB environment flags
    cloud_sql_instance = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    alloydb_cluster = os.getenv("ALLOYDB_CLUSTER_IP")
    db_user = os.getenv("DB_USER", "drishti_app")
    db_pass = os.getenv("DB_PASS", "drishti_secure_2026")
    db_name = os.getenv("DB_NAME", "drishti_db")

    if alloydb_cluster:
        return f"postgresql+asyncpg://{db_user}:{db_pass}@{alloydb_cluster}:5432/{db_name}"
    
    if cloud_sql_instance:
        # Cloud SQL Unix Socket / Proxy mode
        return f"postgresql+asyncpg://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{cloud_sql_instance}"
    
    # High-performance local async SQLite
    return "sqlite+aiosqlite:///drishti_local.db"

DATABASE_URL = get_database_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def init_db():
    """Initializes database schema tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency helper providing managed transactional sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
