from fastapi import HTTPException
from shared.models import User
from app.schema.schema import UserCreate, PasswordUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.helper.utils import hash_password, verify_password

# @app.get("/", response_class=HTMLResponse)
# async def check(request: Request):
#     return templates.TemplateResponse(
#         "index.html", {"request": request, "message": "Welcome to fullstack"}
#     )


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def get_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_user(user_data: UserCreate, db: AsyncSession):
    existing_user = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        password=hash_password(user_data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(user_id: int, user_data: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        return HTTPException(status_code=404, detail="User not found")
    existing_user.first_name = user_data.first_name
    existing_user.last_name = user_data.last_name
    existing_user.username = user_data.username
    existing_user.email = user_data.email
    await db.commit()
    await db.refresh(existing_user)
    return existing_user


async def update_user_password(
    user_id: int, password_data: PasswordUpdate, db: AsyncSession
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password_data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    user.password = hash_password(password_data.new_password)
    await db.commit()
    await db.refresh(user)
    return {"message": "Password updated successfully"}


async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}
