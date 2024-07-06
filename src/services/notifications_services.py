from fastapi import HTTPException
from schemas.listeners_schemas import ListenersShcema
from schemas.notifications_schemas import NotificationsCreateSchema
from tasks.send_notification_tasks import send_bulk_email_task
from uow import IUnitOfWork

import logging
from config.logging_config import setup_logging
from config.celery_config import settings as smtp_settings

setup_logging()
logger = logging.getLogger(__name__)

class NotificaionService:


    async def create_notification(self, notification: NotificationsCreateSchema, uow: IUnitOfWork):
        async with uow:
            try:
                logger.debug("Создание нотификации")
                notify_id = await uow.notifications.create(**notification.model_dump())

                listeners: list[ListenersShcema] = await uow.listeners.get_all(user_id = notification.user_id)
                
                await uow.listeners_notifications.create_multiple(values=[{notify_id:i.id} for i in listeners])
                await uow.commit()

            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise
            except Exception as e:
                await uow.rollback()
                logger.error(e)
                raise HTTPException(status_code=500)


    async def send_notification(self, notification_id: int, uow: IUnitOfWork):
    #    AMAZON ses or  STMP & Twilio or Vonage
        async with uow:
            try:
                logger.debug("Получение listeners")
                listeners_id = await uow.listeners_notifications.get_all(notification_id=notification_id)
                listeners_emails = await uow.listeners.get_multiple_by_id(ids=listeners_id)
                
                logger.debug('Получение notification')
                notification = await uow.notifications.get(id=notification_id)

                logger.debug("Отправка по почте ")
                send_bulk_email_task.delay(listeners_emails, notification.title, notification.content)

            except HTTPException as e:
                # await uow.rollback()
                logger.error(e)
                raise
            except Exception as e:
                # await uow.rollback()
                logger.error(e)
                raise HTTPException(status_code=500)
            

    async def get_notification(self, uow: IUnitOfWork):
        async with uow:
            try:
                logger.debug('Получение notification')
                notification = await uow.notifications.get(id=id)
                return notification
            
            except HTTPException as e:
                # await uow.rollback()
                logger.error(e)
                raise
            except Exception as e:
                # await uow.rollback()
                logger.error(e)
                raise HTTPException(status_code=500)

        


    async def delete_notification(self, id: int, uow: IUnitOfWork):
        async with uow:
            try:
                logger.debug('Удаление notification')
                await uow.notifications.delete(id=id)
                await uow.commit()
            
            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise
            except Exception as e:
                await uow.rollback()
                logger.error(e)
                raise HTTPException(status_code=500)
