from fastapi import HTTPException
from shared.models import Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schema.job_schema import JobCreate, JobUpdate


async def get_jobs(db: AsyncSession):
    result = await db.execute(select(Job))
    jobs = result.scalars().all()
    return jobs


async def get_job(job_id: int, db: AsyncSession):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        return HTTPException(status_code=404, detail="Job not found")
    return job


async def create_job(job_data: JobCreate, db: AsyncSession):
    db.add(job_data)
    await db.commit()
    await db.refresh(job_data)
    return job_data


async def update_job(job_id: int, job_data: JobUpdate, db: AsyncSession):
    result = await db.execute(select(Job).where(Job.id == job_id))
    existing_job = result.scalars().first()
    if not existing_job:
        raise HTTPException(status_code=404, detail="Job not found")
    existing_job.title = job_data.title
    existing_job.company = job_data.company
    existing_job.location = job_data.location
    existing_job.salary = job_data.salary
    existing_job.type = job_data.type
    existing_job.description = job_data.description
    await db.commit()
    await db.refresh(existing_job)
    return existing_job


async def delete_job(job_id: int, db: AsyncSession):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    await db.delete(job)
    await db.commit()
    return {"message": "Job deleted"}
