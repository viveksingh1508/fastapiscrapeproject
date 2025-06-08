from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.views.home_view import home_view

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return await home_view(request)
