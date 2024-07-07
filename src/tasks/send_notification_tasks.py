

# import logging
# from config.logging_config import setup_logging
# from utils.email_sender import EmailSender
# from celery import shared_task

# setup_logging()
# logger = logging.getLogger(__name__)

# @shared_task
# async def send_email_task(self, to_email, subject, body):
#     email_sender = EmailSender()
#     try:
#         await email_sender.send_email(to_email, subject, body)
#     except  Exception as e:
#         raise send_email_task.retry(exc=e, countdown=60) # Повторить через 60 секунд
    
# @shared_task
# async def send_bulk_email_task(to_emails, subject, body):
#     for email in to_emails:
#         logging.debug("Отправка сообщений ")
#         await send_email_task(email, subject, body)



