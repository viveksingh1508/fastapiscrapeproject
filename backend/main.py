from fastapi import FastAPI, Depends
from shared.backenddb import get_db, engine
from shared.models import User, Base
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from sqlalchemy.future import select

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


@app.get("/jobs")
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    jobs = result.scalars().all()
    return jobs


@app.get("/health")
async def health():
    return {"status": "ok"}
