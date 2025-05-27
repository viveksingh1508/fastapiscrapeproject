from pydantic import BaseModel
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
