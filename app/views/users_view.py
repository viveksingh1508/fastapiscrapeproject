from app.services import users
from app.schema.user_schema import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi import Request, HTTPException
from pydantic import ValidationError
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND


templates = Jinja2Templates(directory="app/templates")


async def register_form(request: Request):
    return templates.TemplateResponse(
        "user_register_form.html", {"request": request, "errors": {}, "form_data": {}}
    )


async def create_user_view(request: Request, db: AsyncSession):
    form = await request.form()
    try:
        user_data = UserCreate(**form)
        await users.create_user(user_data, db)
    except ValidationError as e:
        error_dict = {}
        for err in e.errors():
            field = err["loc"][-1]
            msg = err["msg"]

            if msg.lower().startswith("value error"):
                msg = msg.partition(",")[2].strip()

            error_dict.setdefault(field, []).append(msg)

        return templates.TemplateResponse(
            "user_register_form.html",
            {
                "request": request,
                "errors": error_dict,
                "form_data": form,
            },
            status_code=400,
        )

    except HTTPException as e:
        error_dict = {"non_field": [e.detail]}
        return templates.TemplateResponse(
            "user_register_form.html",
            {
                "request": request,
                "errors": error_dict,
                "form_data": form,
            },
            status_code=400,
        )
    return RedirectResponse(url="/auth/login", status_code=HTTP_302_FOUND)
