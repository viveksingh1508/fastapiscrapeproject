from celery import Celery
import requests
from bs4 import BeautifulSoup
import asyncpg
import os
import asyncio
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


celery_app = Celery(
    "scraper",
    broker="redis://localhost:6379/0",  # Replace with your Redis URL
    backend="redis://localhost:6379/0",  # Optional: Specify backend too
)

print(f"broker_url{celery_app.conf.broker_url}")
print(f"backend{celery_app.conf.result_backend}")

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


# @celery_app.task
# def scrape():
#     url = "https://example.com/jobs"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     jobs = []
#     for job in soup.find_all("div", class_="job"):
#         title = job.find("h2").text
#         description = job.find("p").text
#         link = job.find("a")["href"]
#         jobs.append({"title": title, "description": description, "link": link})


# Insert into DB
@celery_app.task
def insert_jobs():
    asyncio.run(_insert_jobs_async())


async def _insert_jobs_async():
    conn = await asyncpg.connect(DATABASE_URL)
    for job in jobs:
        try:
            await conn.execute(
                """
                INSERT INTO users (username, email, password, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (username) DO NOTHING
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


#     # Call the insert_jobs function to start the scraping process
#     insert_jobs.delay()
