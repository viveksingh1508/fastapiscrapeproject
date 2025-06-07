from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
from app.services.auth import login
from sqlalchemy.ext.asyncio import AsyncSession


templates = Jinja2Templates(directory="app/templates")


async def login_view(request: Request, db: AsyncSession):
    if request.method != "POST":
        return templates.TemplateResponse(
            "login.html",
            {"request": request},
        )
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    if not username or not password:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Username and password are required.",
            },
        )
    try:
        login_response = await login(username=username, password=password, db=db)
        if isinstance(login_response, dict):
            # Assuming login returns a dictionary with access_token and token_type
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "access_token": login_response.get("access_token"),
                    "token_type": login_response.get("token_type"),
                },
            )
        else:
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "error": "Invalid credentials. Please try again.",
                },
            )
    except HTTPException:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Invalid credentials. Please try again.",
            },
        )
