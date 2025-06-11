from fastapi import HTTPException, Request
from shared.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.helper.utils import verify_password
from jose import JWTError, jwt
from sqlalchemy.future import select
from sqlalchemy import or_
from datetime import datetime, timedelta, timezone
from fastapi.responses import RedirectResponse


import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 60))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_token(data: dict, token_type: str, expires_delta=None):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if token_type == "access"
        else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": token_type})
    sigining_key = ACCESS_SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, sigining_key, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str, token_type: str):
    secret_kye = ACCESS_SECRET_KEY if token_type == "access" else REFRESH_SECRET_KEY
    try:
        payload = jwt.decode(token, secret_kye, algorithms=JWT_ALGORITHM)
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
    data = {
        "sub": user.username,
        "user_id": str(user.id),
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "iat": datetime.now(timezone.utc).timestamp(),
    }

    access_token = create_token(data, "access")
    refresh_token = create_token(data, "refresh")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
    }


async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


async def get_current_user_from_cookie(request: Request, db: AsyncSession):
    token = request.cookies.get("access_token")
    if not token:
        return None
    scheme, _, param = token.partition(" ")
    if scheme.lower() != "bearer":
        return None
    payload = None
    try:
        payload = decode_token(param, "access")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    try:
        user = await db.get(User, int(user_id))
    except Exception as e:
        print(f"cookies exception {e}")
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")
    return payload


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def refresh_token(refresh_token: str, db: AsyncSession):
    try:
        payload = decode_token(refresh_token, "refresh")
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user = await get_user(int(payload["user_id"]), db)
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User inactive")

        data = {
            "sub": user.username,
            "user_id": str(user.id),
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "iat": datetime.now(timezone.utc).timestamp(),
        }
        new_access_token = create_token(data, "access")
        new_refresh_token = create_token(data, "refresh")

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
