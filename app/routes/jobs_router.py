from fastapi import APIRouter, Depends
from app.services import jobs
from sqlalchemy.ext.asyncio import AsyncSession
from shared.backenddb import get_db
from app.schema.job_schema import JobResponse, JobCreate, JobUpdate
from typing import List

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    return await jobs.get_jobs(db)


@router.get("/{job_id}", response_model=JobResponse)
async def retrieve_job(job_id: int, db: AsyncSession = Depends(get_db)):
    return await jobs.get_job(job_id, db)


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
