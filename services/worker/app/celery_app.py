from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()
celery_app = Celery("global-news-digest", broker=settings.redis_url, backend=settings.redis_url)
celery_app.conf.update(
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "daily-report": {
            "task": "app.tasks.generate_daily_report",
            "schedule": crontab(hour=7, minute=50),
        }
    },
)
celery_app.autodiscover_tasks(["app"])
