from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_async_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_db)):
    return await user_service.create_user(db=db, user_in=user_in)

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    return await user_service.get_users(db, skip=skip, limit=limit)