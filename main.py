"""
Main application entry point.
Features: Dual DB support (Sync/Async), Auto-Logging, 
Environment-based docs, and Database Retry Logic.
"""

import time
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Internal imports
from app.core.config import settings
from app.core.logger import logger
from app.core.database import async_engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and Shutdown logic with database connection retry.
    """
    max_retries = 5
    retry_delay = 5
    connected = False
    
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}...")

    for attempt in range(max_retries):
        try:
            async with async_engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            
            if settings.is_dev:
                logger.info("🛠️  Development Mode: Syncing database tables...")
                async with async_engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            
            connected = True
            logger.info("✅ Database connected successfully.")
            break
        except Exception as e:
            logger.warning(
                f"⚠️  DB connection attempt {attempt + 1}/{max_retries} failed. "
                f"Retrying in {retry_delay}s... (Error: {e})"
            )
            await asyncio.sleep(retry_delay)

    if not connected:
        logger.critical("❌ Could not connect to database. Shutting down application.")
        raise RuntimeError("Database connection failed")
    
    yield  # --- Application is running ---
    
    # Clean shutdown
    await async_engine.dispose()
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")


# --- App Configuration ---

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    # Documentation visible only in development
    openapi_url=f"{settings.API_STR}/openapi.json" if settings.is_dev else None,
    docs_url="/docs" if settings.is_dev else None,
    redoc_url="/redoc" if settings.is_dev else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Automatically logs all incoming requests and their duration."""
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"{request.method} {request.url.path} "
        f"- {response.status_code} "
        f"- {process_time:.2f}ms"
    )
    return response

# --- Router Registration ---

try:
    from app.api.routers.api import api_router
    app.include_router(api_router, prefix=settings.API_STR, tags=["API"])
except ImportError as e:
    logger.warning(f"Could not import one or more routers: {e}")

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring or Docker."""
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.is_dev)