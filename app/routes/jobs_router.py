from fastapi import APIRouter, Depends, Request
from app.services import jobs
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from app.schema.job_schema import JobResponse, JobCreate, JobUpdate
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def list_jobs(
    request: Request, db: AsyncSession = Depends(get_db), page: int = 1, limit: int = 5
):
    return await jobs.get_jobs(request, db, page, limit)


@router.get("/{job_id}", response_model=JobResponse)
async def retrieve_job(
    request: Request, job_id: int, db: AsyncSession = Depends(get_db)
):
    return await jobs.get_job(request, job_id, db)


@router.post("/", response_model=JobResponse)
async def create_job(job_data: JobCreate, db: AsyncSession = Depends(get_db)):
    return await jobs.create_job(job_data, db)


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int, job_data: JobUpdate, db: AsyncSession = Depends(get_db)
):
    return await jobs.update_job(job_id, job_data, db)


@router.delete("/{job_id}")
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db)):
    return await jobs.delete_job(job_id, db)
