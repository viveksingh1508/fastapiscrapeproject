from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


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
        orm_mode = True
