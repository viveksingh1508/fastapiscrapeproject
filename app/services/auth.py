from fastapi import HTTPException
from shared.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from sqlalchemy.future import select


# @app.get("/", response_class=HTMLResponse)
# async def check(request: Request):
#     return templates.TemplateResponse(
#         "index.html", {"request": request, "message": "Welcome to fullstack"}
#     )


async def login_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


async def logout_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Here you might want to implement logic to invalidate the user's session
    return {"message": "User logged out successfully"}
