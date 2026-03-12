from celery import Celery

from app.core.config import settings

celery_app = Celery("nexus1", broker=settings.rabbitmq_url, backend=settings.redis_url)


@celery_app.task
def scheduled_watchlist_scan(target: str) -> dict:
    return {
        "target": target,
        "status": "queued",
        "note": "Scheduled public-source scan registered.",
    }
