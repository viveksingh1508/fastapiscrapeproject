from fastapi import APIRouter, Depends
from app.services import auth
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from app.schema.schema import LoginResponse, UserLogin


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(user_login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth.login(user_login_data, db)
