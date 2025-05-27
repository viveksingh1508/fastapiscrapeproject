from fastapi import APIRouter, Depends, Request
from app.services import auth
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from app.schema.auth_schema import LoginResponse, UserLogin
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(user_login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await auth.login(user_login_data, db)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return await auth.login_page(request)
