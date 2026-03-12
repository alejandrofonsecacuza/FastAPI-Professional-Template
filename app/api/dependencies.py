from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, AsyncSessionLocal

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()