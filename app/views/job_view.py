from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.jobs import search_jobs, get_job
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from app.views import custom_render_templates


async def search_jobs_view(
    request: Request,
    keyword: str,
    location: str,
    db: AsyncSession,
    page: int,
    limit: int,
):
    response = await search_jobs(request, keyword, location, db, page, limit)
    if not response:
        return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

    return custom_render_templates(request, "jobs.html", context={**response})


async def get_job_view(request: Request, job_id: int, db: AsyncSession):
    response = await get_job(request, job_id, db)
    if not response:
        return custom_render_templates(request, "404.html", {...})
    return custom_render_templates(request, "job_details.html", context={**response})
