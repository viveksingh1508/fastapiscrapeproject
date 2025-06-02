from fastapi import HTTPException, Request
from shared.models import Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schema.job_schema import JobCreate, JobUpdate
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

templates = Jinja2Templates(directory="app/templates")


async def get_jobs(
    request: Request,
    db: AsyncSession,
    page: int,
    limit: int,
):

    offset = (page - 1) * limit
    total_jobs = await db.scalar(select(func.count()).select_from(Job))
    result = await db.execute(select(Job).offset(offset).limit(limit))
    jobs = result.scalars().all()
    total_pages = (total_jobs + limit - 1) // limit
    return templates.TemplateResponse(
        "jobs.html",
        {
            "request": request,
            "jobs": jobs,
            "page": page,
            "total_pages": total_pages,
            "total_jobs": total_jobs,
        },
    )


async def get_job(request: Request, job_id: int, db: AsyncSession):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    return templates.TemplateResponse(
        "job_details.html", {"request": request, "job": job}
    )


async def create_job(job_data: JobCreate, db: AsyncSession):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        location=job_data.location,
        salary=job_data.salary,
        type=job_data.type,
        description=job_data.description,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


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
