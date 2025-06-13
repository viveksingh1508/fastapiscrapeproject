from fastapi import HTTPException, Request
from shared.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.helper.utils import verify_password
from sqlalchemy.future import select
from sqlalchemy import or_
from fastapi.responses import RedirectResponse
from app.helper.redis import clear_session
from app.helper.redis import SESSION_COOKIE_NAME


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

    return user


async def logout(request: Request):
    session_id = request.state.session

    # Delete session from Redis
    if session_id:
        await clear_session(session_id)

    # Redirect to login or home and delete the cookie
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


async def get_current_user_from_session(request: Request, db: AsyncSession):
    session = request.state.session
    user_id = session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        user = await db.get(User, int(user_id))
    except Exception as e:
        print(f"fetch user exception {e}")
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive or not found")
    return user.username


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
