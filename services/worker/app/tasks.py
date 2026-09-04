from datetime import UTC, date, datetime

from celery.utils.log import get_task_logger
from packages.shared.ids import daily_report_run_key
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.celery_app import celery_app
from app.config import get_settings

logger = get_task_logger(__name__)


def _engine():
    return create_engine(get_settings().database_url, pool_pre_ping=True)


@celery_app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    max_retries=3,
)
def generate_daily_report(self) -> dict[str, str]:
    """Idempotent orchestration entry point; pipeline stages are added incrementally."""
    settings = get_settings()
    run_key = daily_report_run_key(date.today(), settings.pipeline_version)
    with Session(_engine()) as db:
        try:
            db.execute(
                text(
                    """INSERT INTO job_runs (job_name, run_key, status, retry_count, started_at)
                       VALUES (:job_name, :run_key, :status, :retry_count, :started_at)"""
                ),
                {
                    "job_name": "daily-report",
                    "run_key": run_key,
                    "status": "running",
                    "retry_count": self.request.retries,
                    "started_at": datetime.now(UTC),
                },
            )
            db.commit()
        except IntegrityError:
            db.rollback()
            return {"status": "already-running-or-complete", "run_key": run_key}
    logger.info("Accepted daily report run %s", run_key)
    return {"status": "accepted", "run_key": run_key}
