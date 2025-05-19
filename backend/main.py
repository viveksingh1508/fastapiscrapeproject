from fastapi import FastAPI, Depends
from backend.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


app = FastAPI()


@app.get("/jobs")
async def get_jobs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM users"))
    jobs = result.mappings().all()
    return jobs


@app.get("/health")
async def health():
    return {"status": "ok"}
