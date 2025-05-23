from fastapi import APIRouter, Depends
from app.services import users
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from shared.schema import UserCreate, UserResponse


router = APIRouter()


@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    return await users.get_users(db)


@router.get("/users/{user_id}")
async def retrieve_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await users.get_user(user_id, db)


@router.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await users.create_user(user_data, db)


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    return await users.update_user(user_id, user_data, db)


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await users.delete_user(user_id, db)


# @router.post("/auth/login")
# async def login(user: auth.UserLogin):
#     return await auth.login(user)


# @router.post("/auth/register")
# async def register(user: auth.UserRegister):
#     return await auth.register(user)


# @router.get("/auth/me")
# async def get_current_user():
#     return await auth.get_current_user()


# @router.get("/auth/logout")
# async def logout():
#     return await auth.logout()


# @router.get("/auth/refresh")
# async def refresh_token():
#     return await auth.refresh_token()


# @router.get("/auth/verify")
# async def verify_token():
#     return await auth.verify_token()


# @router.get("/auth/verify/{token}")
# async def verify_token(token: str):
#     return await auth.verify_token(token)


# @router.get("/auth/verify/{token}/refresh")
# async def refresh_token(token: str):
#     return await auth.refresh_token(token)


# @router.get("/auth/verify/{token}/logout")
# async def logout(token: str):
#     return await auth.logout(token)


# @router.get("/auth/verify/{token}/me")
# async def get_current_user(token: str):
#     return await auth.get_current_user(token)


# @router.get("/auth/verify/{token}/register")
# async def register(token: str):
#     return await auth.register(token)
