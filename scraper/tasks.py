from celery import Celery
from datetime import datetime, timezone
from shared.scraperdb import SessionLocal
from shared.models import Job, User


celery_app = Celery(
    "scraper",
    broker="redis://host.docker.internal:6379/0",
    backend="redis://host.docker.internal:6379/1",
    timezone="UTC",
)

celery_app.config_from_object("celeryconfig")


jobs = [
    {
        "first_name": "Vivek",
        "last_name": "Singh",
        "username": "viveksingh",
        "email": "viveksingh00747@gmail.com",
        "password": "password",
    },
    {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "secret123",
    },
]


# jobs = [
#     {
#         "title": "Python Developer",
#         "company": "Eviden",
#         "location": "Gurgaon, Haryana, India",
#         "description": "We are looking for a Python Developer with experience in building high-performing, scalable, enterprise-grade applications. You will be part of a talented software team that works on mission-critical applications.",
#         "salary": "₹10,00,000 - ₹20,00,000 a year",
#         "posted_at": "2023-10-01",
#         "type": "Full-time",
#     },
#     {
#         "title": "Full Stack Developer",
#         "company": "Microsoft",
#         "location": "Bengaluru, Karnataka, India",
#         "description": "We are looking for a Full Stack Developer with expertise in both front-end and back-end technologies. You will be responsible for developing and maintaining web applications that provide a seamless user experience.",
#         "salary": "₹12,00,000 - ₹22,00,000 a year",
#         "posted_at": "2023-10-02",
#         "type": "Full-time",
#     },
# ]


@celery_app.task
def insert_jobs():
    db = SessionLocal()
    try:
        for job in jobs:
            user = User(
                first_name=job["first_name"],
                last_name=job["last_name"],
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


# @celery_app.task
# def insert_jobs():
#     db = SessionLocal()
#     try:
#         for job in jobs:
#             job = Job(
#                 first_name=job["first_name"],
#                 last_name=job["last_name"],
#                 username=job["username"],
#                 email=job["email"],
#                 password=job["password"],
#                 created_at=datetime.now(timezone.utc),
#                 updated_at=datetime.now(timezone.utc),
#             )
#             db.add(job)
#         db.commit()
#         print("Job inserted")
#     except Exception as e:
#         db.rollback()
#         print(f"Insert failed: {e}")
#     finally:
#         db.close()


@celery_app.task
def process(x, y):
    print(f"Processing {x} and {y}")
    return x + y
