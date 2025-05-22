from celery import Celery
from datetime import datetime
from shared.scraperdb import SessionLocal
from shared.models import User


celery_app = Celery(
    "scraper",
    broker="redis://host.docker.internal:6379/0",
    backend="redis://host.docker.internal:6379/1",
    timezone="UTC",
)

celery_app.config_from_object("celeryconfig")


jobs = [
    {
        "username": "viveksingh",
        "email": "viveksingh00747@gmail.com",
        "password": "password",
    },
    {"username": "johndoe", "email": "johndoe@example.com", "password": "secret123"},
]


@celery_app.task
def insert_jobs():
    db = SessionLocal()
    try:
        for job in jobs:
            user = User(
                username=job["username"],
                email=job["email"],
                password=job["password"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(user)
        db.commit()
        print("Users inserted")
    except Exception as e:
        db.rollback()
        print(f"Insert failed: {e}")
    finally:
        db.close()


@celery_app.task
def process(x, y):
    print(f"Processing {x} and {y}")
    return x + y
