import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import logging
from config.app_config import settings
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)




class EmailSender:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD

    
    async def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Sender name', self.username))
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            logger.debug("Начало отправки по почте ")
            smpt_server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            smpt_server.login(self.username, self.password)
            smpt_server.sendmail(self.username, to_email, msg.as_string())
            smpt_server.quit()
            logger.debug("Сообщение отправленно")

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            raise    

