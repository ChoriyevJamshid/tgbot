import asyncio
from typing import Any

from celery import Celery, signals
from celery.schedules import crontab


celery_event_loop = asyncio.new_event_loop()


celery_app = Celery(main="telegram_bot", broker="redis://localhost:6379/")
celery_app.autodiscover_tasks()
# celery_app.conf.beat_schedule = {
#     "add-every-30-seconds": {
#         "task": "src.worker.tasks.test_task",
#         "schedule": crontab(minute="*/5", hour="6-23"),
#     },
# }
celery_app.conf.update(timezone="Asia/Tashkent")
