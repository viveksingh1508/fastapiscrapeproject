from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
# Ideally store in .env and load with dotenv or pydantic
# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/app_db"
BACKEND_DATABASE_URL = os.getenv("BACKEND_DATABASE_URL")
print(f"Connecting to database at {BACKEND_DATABASE_URL}")

engine = create_async_engine(BACKEND_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
