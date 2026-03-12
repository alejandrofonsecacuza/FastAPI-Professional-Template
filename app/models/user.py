from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, BaseModel

class User(BaseModel, Base):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)