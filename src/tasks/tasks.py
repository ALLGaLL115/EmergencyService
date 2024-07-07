import asyncio
import logging
from celery import Celery
from config.app_config import settings
from utils.email_sender import EmailSender

celery_app = Celery('email_tasks', broker=settings.CELERY_BROKER, backend='rpc://')



celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(bind=True, max_retries=3)
def send_email_task(self, to_email, subject, body):
    email_sender = EmailSender()
    try:
        email_sender.send_email(to_email, subject, body)
    except  Exception as e:
        raise self.retry(exc=e, countdown=60) # Повторить через 60 секунд
    
@celery_app.task
def send_bulk_email_task(to_emails, subject, body):
    try:
        for email in to_emails:
            logging.debug("Отправка сообщений ")
            logging.debug([email, subject, body])
            send_email_task.delay(email, subject, body)
    except Exception as e:
        logging.error(e)
        raise e 
