from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"
timezone = "UTC"

beat_schedule = {
    "run-every-minute": {
        "task": "tasks.insert_jobs",
        "schedule": crontab(minute="*/1"),  # Every minute
        # Alternative: 'schedule': 60.0 (seconds)
    }
}
