from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True