from celery import Celery
import asyncpg
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


celery_app = Celery(
    "scraper",
    broker="redis://host.docker.internal:6379/0",  # Replace with your Redis URL
    backend="redis://host.docker.internal:6379/0",
    timezone="UTC",  # Optional: Specify backend too
)

print(f"broker_url {celery_app.conf.broker_url}")
print(f"backend {celery_app.conf.result_backend}")
print(f"timezone {celery_app.conf.timezone}")

celery_app.config_from_object("celeryconfig")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")
print(f"Database URL: {DATABASE_URL}")

jobs = [
    {
        "username": "viveksingh",
        "email": "viveksingh00747@gmail.com",
        "password": "password",
    },
    {"username": "johndoe", "email": "johndoe@example.com", "password": "secret123"},
    # Add more users as needed
]


# Insert into DB
@celery_app.task
def insert_jobs():
    asyncio.run(_insert_jobs_async())


async def _insert_jobs_async():
    conn = await asyncpg.connect(DATABASE_URL, ssl=False)
    for job in jobs:
        try:
            await conn.execute(
                """
                INSERT INTO users (username, email, password, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                """,
                job["username"],
                job["email"],
                job["password"],
                datetime.utcnow(),
                datetime.utcnow(),
            )
        except Exception as e:
            print(f"Insert error for {job['username']}: {e}")
    await conn.close()


@celery_app.task
def process(x, y):
    """
    Process the given data.
    """
    print(f"Processing {x} and {y}")
    return x + y
