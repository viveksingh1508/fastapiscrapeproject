from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from app.services.jobs import search_jobs, get_job
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND


templates = Jinja2Templates(directory="app/templates")


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

    return templates.TemplateResponse("jobs.html", context={**response})


async def get_job_view(request: Request, job_id: int, db: AsyncSession):
    response = await get_job(request, job_id, db)
    if not response:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    return templates.TemplateResponse("job_details.html", context={**response})
