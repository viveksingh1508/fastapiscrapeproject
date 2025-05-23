from celery.schedules import crontab

broker_url = "redis://host.docker.internal:6379/0"
result_backend = "redis://host.docker.internal:6379/1"
redbeat_redis_url = "redis://host.docker.internal:6379/2"
timezone = "UTC"

# RedBeat settings
beat_scheduler = "redbeat.RedBeatScheduler"
redbeat_redis_url = broker_url
redbeat_key_prefix = "redbeat:"
redbeat_lock_timeout = 300  # 5 minutes
redbeat_lock_refresh = 270  # Refresh after 4.5 minutes
redbeat_max_retries = 3  # Retry up to 3 times

# Critical for lock stability
# Redis Persistence Configuration (Add to transport options)
broker_transport_options = {
    "visibility_timeout": 600,  # 10 minutes
    "socket_keepalive": True,
    "retry_on_timeout": True,
    "health_check_interval": 30,
    # Persistence control
    "socket_timeout": 30,
    "max_connections": 100,
    "persistence": False,  # Disable Redis persistence for Celery
}

# Task settings
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
task_track_started = True
task_acks_late = True  # Better for idempotent tasks
worker_prefetch_multiplier = 1  # Fair task distribution

# Task Configuration
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
task_track_started = True
task_acks_late = True
worker_prefetch_multiplier = 1  # Disable prefetching for fairness
task_default_queue = "default"
task_default_priority = 5
task_reject_on_worker_lost = True  # Important for at-least-once delivery

# Monitoring and Events
worker_send_task_events = True
event_queue_expires = 60
worker_proc_alive_timeout = 30
beat_max_loop_interval = 5  # More frequent scheduler checks

beat_schedule = {
    "run-every-ten-minute": {
        "task": "tasks.insert_jobs",
        "schedule": crontab(minute="*/10"),
        "options": {
            "expires": 180,  # Increased to 3 minutes
            "priority": 5,
            "queue": "scheduled",
            "retry": True,  # Explicit retry
            "retry_policy": {
                "max_retries": 3,
                "interval_start": 10,
                "interval_step": 10,
                "interval_max": 60,
            },
        },
        "args": (),
    }
}
