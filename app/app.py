from fastapi import FastAPI, Request
from shared.backenddb import engine
from shared.models import Base
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import router as api_router
from app.views.auth_view import get_user


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
app.include_router(api_router)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)
templates = Jinja2Templates(directory="app/templates")


@app.get("/healthz")
async def health():
    return {"status": "Ok!"}


@app.get("/docs")
async def docs():
    return {"message": "API documentation is available at /docs"}


@app.get("/")
async def home(request: Request):
    user = await get_user(request)
    if user:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "user": user},
        )
    else:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "user": {}},
        )
