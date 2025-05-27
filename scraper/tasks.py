from celery import Celery
from datetime import datetime, timezone
from shared.scraperdb import SessionLocal
from shared.models import Job


celery_app = Celery(
    "scraper",
    broker="redis://host.docker.internal:6379/0",
    backend="redis://host.docker.internal:6379/1",
    timezone="UTC",
)

celery_app.config_from_object("celeryconfig")


jobs = [
    {
        "title": "Python Developer",
        "company": "Eviden",
        "location": "Gurgaon, Haryana, India",
        "description": "We are looking for a Python Developer with experience in building high-performing, scalable, enterprise-grade applications. You will be part of a talented software team that works on mission-critical applications.",
        "salary": "₹10,00,000 - ₹20,00,000 a year",
        "type": "Full-time",
    },
    {
        "title": "Full Stack Developer",
        "company": "Microsoft",
        "location": "Bengaluru, Karnataka, India",
        "description": "We are looking for a Full Stack Developer with expertise in both front-end and back-end technologies. You will be responsible for developing and maintaining web applications that provide a seamless user experience.",
        "salary": "₹12,00,000 - ₹22,00,000 a year",
        "type": "Full-time",
    },
]


@celery_app.task
def insert_jobs():
    db = SessionLocal()
    try:
        for job in jobs:
            job = Job(
                title=job["title"],
                company=job["company"],
                location=job["location"],
                description=job["description"],
                salary=job["salary"],
                type=job["type"],
                posted_at=datetime.now(timezone.utc),
                # updated_at=datetime.now(timezone.utc), created a created_at field in the model
            )
            db.add(job)
        db.commit()
        print("Job inserted")
    except Exception as e:
        db.rollback()
        print(f"Insert failed: {e}")
    finally:
        db.close()


@celery_app.task
def process(x, y):
    print(f"Processing {x} and {y}")
    return x + y
