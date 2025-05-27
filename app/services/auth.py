from fastapi import HTTPException
from shared.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.helper.utils import verify_password
from jose import JWTError, jwt
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import Request

import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# @app.get("/", response_class=HTMLResponse)
# async def check(request: Request):
#     return templates.TemplateResponse(
#         "index.html", {"request": request, "message": "Welcome to fullstack"}
#     )

templates = Jinja2Templates(directory="app/templates")


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def authenticate_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    try:
        if not user or not verify_password(password, user.password):
            return None
        return user
    except Exception:
        return None


async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )


async def logout(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Here you might want to implement logic to invalidate the user's session
    return {"message": "User logged out successfully"}
