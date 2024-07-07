from utils.email_sender import EmailSender
from .tasks import celery_app

@celery_app.task(bind=True, max_retries=3)
async def send_email_task(self, to_email, subject, body):
    email_sender = EmailSender()
    try:
        await email_sender.send_email(to_email, subject, body)
    except  Exception as e:
        raise self.retry(exc=e, countdown=60) # Повторить через 60 секунд
    
@celery_app.task
async def send_bulk_email_task(to_emails, subject, body):
    for email in to_emails:
        send_email_task(email, subject, body)



