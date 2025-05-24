from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path("/.env")
load_dotenv(dotenv_path=env_path)

BACKEND_DATABASE_URL = os.getenv("BACKEND_DATABASE_URL")
print(f"Connecting to database at {BACKEND_DATABASE_URL}")

engine = create_async_engine(BACKEND_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
