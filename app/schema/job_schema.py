from pydantic import BaseModel
from datetime import datetime


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    salary: str
    type: str
    description: str
    posted_at: datetime

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    salary: str
    type: str
    description: str

    class Config:
        from_attributes = True


class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary: str | None = None
    type: str | None = None
    description: str | None = None

    class Config:
        from_attributes = True
