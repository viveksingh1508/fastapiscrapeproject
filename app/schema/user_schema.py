from pydantic import BaseModel, EmailStr, field_validator
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
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 50:
            raise ValueError("Username must not exceed 50 characters")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, v):
        if len(v) < 8:
            raise ValueError("Confirm password must be at least 8 characters long")
        return v

    @field_validator("confirm_password")
    @classmethod
    def check_password_match(cls, v, info):
        if info.data.get("password") and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
