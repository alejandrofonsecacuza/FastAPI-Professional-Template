from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(email=user_in.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    # La sintaxis 2.0 usa execute + select
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()