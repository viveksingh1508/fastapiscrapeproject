from fastapi import Request, HTTPException
from app.services.auth import login, get_current_user_from_session, logout
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.views import custom_render_templates


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
                "user": username,
            },
            status_code=400,
        )
    try:
        response = await login(username=username, password=password, db=db)
        request.state.session = {"user_id": response.id}
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

    except HTTPException:
        return custom_render_templates(
            request,
            "login.html",
            {
                "request": request,
                "error": "Invalid credentials. Please try again.",
                "user": username,
            },
            status_code=401,
        )


async def get_user_view(request: Request, db: AsyncSession):
    user = await get_current_user_from_session(request, db)
    return user


async def logout_view(request: Request):
    logout(request)
    return custom_render_templates(
        "index.html",
        {"request": request, "user": {}},
    )
