from fastapi import APIRouter, Depends, Request
from app.views import auth_view
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: AsyncSession = Depends(get_db)):
    return await auth_view.login_view(request, db)


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    return await auth_view.login_view(request, db)


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    return await auth_view.logout(request)
