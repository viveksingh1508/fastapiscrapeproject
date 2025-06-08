from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
from app.services.auth import login, get_current_user_from_cookie
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

templates = Jinja2Templates(directory="app/templates")


async def login_view(request: Request, db: AsyncSession):
    if request.method != "POST":
        return templates.TemplateResponse(
            "login.html",
            {"request": request},
        )
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if not username or not password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Username and password are required.",
                "username": username,
            },
            status_code=400,
        )
    try:
        login_response = await login(username=username, password=password, db=db)
        response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {login_response['access_token']}",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return response
    except HTTPException:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid credentials. Please try again.",
                "username": username,
            },
            status_code=401,
        )


async def get_user(request: Request):
    user = await get_current_user_from_cookie(request)
    return user
