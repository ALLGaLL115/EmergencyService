from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict

celery_app = Celery('email_tasks', broker='pyamqp://guest@localhost//', backend='rpc://')



celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],  
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


class Settings(BaseSettings):
    SMTP_USER: str
    SMTP_PASSWORD: str

model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
