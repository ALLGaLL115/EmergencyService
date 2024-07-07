from celery import Celery
from config.app_config import settings

celery_app = Celery('email_tasks', broker=settings.BROKER, backend='rpc://')



celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)