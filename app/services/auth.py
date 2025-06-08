from fastapi import HTTPException, Request
from shared.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.helper.utils import verify_password
from jose import JWTError, jwt
from sqlalchemy.future import select
from sqlalchemy import or_
from datetime import datetime, timedelta, timezone
from fastapi.responses import RedirectResponse


# from fastapi.security import OAuth2PasswordRequestForm


import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def authenticate_user(username: str, password: str, db: AsyncSession):
    try:
        result = await db.execute(
            select(User).where(or_(User.username == username, User.email == username))
        )
        user = result.scalars().first()
        if not user or not verify_password(password, user.password):
            return None
        return user
    except Exception:
        return None


# async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
async def login(username: str, password: str, db: AsyncSession):
    user = await authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "iat": datetime.now(timezone.utc).timestamp(),
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response


async def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    scheme, _, param = token.partition(" ")
    if scheme.lower() != "bearer":
        return None
    payload = None
    try:
        payload = decode_access_token(param)
    except HTTPException:
        return None
    return payload
