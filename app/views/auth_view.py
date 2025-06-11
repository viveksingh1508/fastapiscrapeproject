from fastapi import Request, HTTPException
from app.services.auth import login, get_current_user_from_cookie, logout, refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.status import HTTP_302_FOUND
from app.views import custom_render_templates
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60))


async def login_view(request: Request, db: AsyncSession):
    if request.method != "POST":
        return custom_render_templates(
            request,
            "login.html",
            {"request": request},
        )
    form = await request.form()
    username = form.get("username", "").strip()
    password = form.get("password", "")
    if not username or not password:
        return custom_render_templates(
            request,
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
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {login_response['refresh_token']}",
            httponly=True,
            secure=False,
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            path="auth/refresh",
        )
        return response
    except HTTPException:
        return custom_render_templates(
            "login.html",
            {
                "request": request,
                "error": "Invalid credentials. Please try again.",
                "username": username,
            },
            status_code=401,
        )


async def refresh_token_view(request: Request, db: AsyncSession):
    refresh_token_cookie = request.cookies.get("refresh_token")

    token_value = None
    if refresh_token_cookie and refresh_token_cookie.startswith("Bearer "):
        token_value = refresh_token_cookie[7:]
    if not token_value:
        response = JSONResponse({"details": "No refresh token"}, status_code=401)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    try:
        tokens = await refresh_token(token_value, db)
        response = JSONResponse(content={"message": "Token refreshed"})

        response.set_cookie(
            key="access_token",
            value=f"Bearer {tokens['access_token']}",
            httponly=True,
            secure=False,  # True in production
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return response

    except HTTPException:
        response = JSONResponse({"details": "Refresh failed"}, status_code=401)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


async def get_user_view(request: Request):
    user = await get_current_user_from_cookie(request)
    return user


async def logout_view(request: Request):
    logout(request)
    return custom_render_templates(
        "index.html",
        {"request": request, "user": {}},
    )
