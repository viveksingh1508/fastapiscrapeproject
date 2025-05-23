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


class Job(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: str
    type: str
    description: str
    posted_at: str

    class Config:
        from_attributes = True
