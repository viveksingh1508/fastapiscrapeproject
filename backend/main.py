from fastapi import FastAPI, Depends
from shared.db import get_db, engine
from shared.models import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

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
    result = await db.execute(text("SELECT * FROM users"))
    jobs = result.mappings().all()
    return jobs


@app.get("/health")
async def health():
    return {"status": "ok"}
