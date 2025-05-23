from fastapi import FastAPI, Depends, HTTPException, Request
from shared.backenddb import get_db, engine
from shared.models import User, Base, Job
from shared.schema import UserCreate, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from sqlalchemy.future import select
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    env = os.getenv("ENV", "dev")
    if env == "dev":
        print("Dev mode: Creating tables")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    else:
        print("Prod mode: Expecting Alembic migrations")
    yield


app = FastAPI(lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="backend/static"),
    name="static",
)
templates = Jinja2Templates(directory="backend/templates")


@app.get("/", response_class=HTMLResponse)
async def check(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Welcome to fullstack"}
    )


@app.get("/jobs")
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}
    return user


@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalars().first()
    if not existing_user:
        return HTTPException(status_code=404, detail="User not found")
    existing_user.first_name = user_data.first_name
    existing_user.last_name = user_data.last_name
    existing_user.username = user_data.username
    existing_user.email = user_data.email
    existing_user.password = user_data.password
    await db.commit()
    await db.refresh(existing_user)
    return existing_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        return {"error": "User not found"}
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}


# May be work on this later

#######################################################

# @app.post("/jobs")
# async def create_job(job: Job, db: AsyncSession = Depends(get_db)):
#     db.add(job)
#     await db.commit()
#     await db.refresh(job)
#     return job


# @app.delete("/jobs/{job_id}")
# async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Job).where(Job.id == job_id))
#     job = result.scalars().first()
#     if not job:
#         return {"error": "Job not found"}
#     await db.delete(job)
#     await db.commit()
#     return {"message": "Job deleted"}


# @app.put("/jobs/{job_id}")
# async def update_job(job_id: int, job: Job, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(Job).where(Job.id == job_id))
#     existing_job = result.scalars().first()
#     if not existing_job:
#         return {"error": "Job not found"}
#     existing_job.title = job.title
#     existing_job.company = job.company
#     existing_job.location = job.location
#     existing_job.salary = job.salary
#     existing_job.type = job.type
#     existing_job.description = job.description
#     await db.commit()
#     await db.refresh(existing_job)
#     return existing_job

#######################################################


@app.get("/healthz")
async def health():
    return {"status": "Ok!"}


@app.get("/docs")
async def docs():
    return {"message": "API documentation is available at /docs"}
