from fastapi import APIRouter, Depends
from app.services import users
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from app.schema.user_schema import UserCreate, UserResponse, PasswordUpdate
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    return await users.get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def retrieve_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await users.get_user(user_id, db)


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_user(user_data, db)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    return await users.update_user(user_id, user_data, db)


@router.put("/{user_id}/password")
async def update_user_password(
    user_id: int, password_data: PasswordUpdate, db: AsyncSession = Depends(get_db)
):
    return await users.update_user_password(user_id, password_data, db)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await users.delete_user(user_id, db)
