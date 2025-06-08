from fastapi import HTTPException, Request
from shared.models import Job
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schema.job_schema import JobCreate, JobUpdate
from sqlalchemy import func
import ast
import json


# Uncomment the following function if you want to implement pagination for job listings

# async def get_jobs(
#     request: Request,
#     db: AsyncSession,
#     page: int,
#     limit: int,
# ):

#     offset = (page - 1) * limit
#     total_jobs = await db.scalar(select(func.count()).select_from(Job))
#     result = await db.execute(select(Job).offset(offset).limit(limit))
#     jobs = result.scalars().all()
#     total_pages = (total_jobs + limit - 1) // limit
#     return templates.TemplateResponse(
#         "jobs.html",
#         {
#             "request": request,
#             "jobs": jobs,
#             "page": page,
#             "total_pages": total_pages,
#             "total_jobs": total_jobs,
#         },
#     )


async def get_job(request: Request, job_id: int, db: AsyncSession):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        return None
    try:
        benefits_value = ast.literal_eval(job.benefits)
        if isinstance(benefits_value, set):
            # Convert set to string by joining its elements
            benefits_str = ", ".join(str(b) for b in benefits_value)
        elif isinstance(benefits_value, str):
            benefits_str = benefits_value
        else:
            benefits_str = str(benefits_value)
        benefits = [b.strip() for b in benefits_str.split(",") if b.strip()]
    except Exception as e:
        benefits = []
        print(f"Error parsing benefits: {e}")

    try:
        company_profile = json.loads(job.company_profile)
    except json.JSONDecodeError:
        company_profile = {}
        print("Error parsing company profile, using empty dictionary.")
    return {
        "request": request,
        "job": job,
        "benefits": benefits,
        "company_profile": company_profile,
    }


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


async def search_jobs(
    request: Request,
    keyword: str,
    location: str,
    db: AsyncSession,
    page: int,
    limit: int,
):
    if not keyword.strip() and not location.strip():
        return None

    if not isinstance(page, int) or page < 1:
        raise HTTPException(status_code=400, detail="Page must be a positive integer")
    if not isinstance(limit, int) or limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be a positive integer")

    offset = (page - 1) * limit
    query = select(Job)
    count_query = select(func.count()).select_from(Job)

    if keyword:
        query = query.where(Job.job_title.ilike(f"%{keyword}%"))
        count_query = count_query.where(Job.job_title.ilike(f"%{keyword}%"))
    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))
        count_query = count_query.where(Job.location.ilike(f"%{location}%"))

    result = await db.execute(query.offset(offset).limit(limit))
    jobs = result.scalars().all()

    total_jobs = await db.scalar(count_query)
    total_pages = (total_jobs + limit - 1) // limit if total_jobs else 1

    return {
        "request": request,
        "jobs": jobs,
        "page": page,
        "total_pages": total_pages,
        "total_jobs": total_jobs,
    }
