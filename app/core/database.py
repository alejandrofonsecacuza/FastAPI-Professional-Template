import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, DateTime, create_engine
from app.core.config import settings

# Async Engine (FastAPI)
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=False,
)

# Sync Engine (Celery / Alembic)
engine = create_engine(
    settings.SYNC_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass

class BaseModel:
    """Base mixin for models, providing id, created_at, and updated_at fields."""
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )