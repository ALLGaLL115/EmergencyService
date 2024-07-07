from fastapi import HTTPException
from schemas.listeners_schemas import ListenersShcema
from schemas.notifications_schemas import NotificationsCreateSchema
# from tasks.send_notification_tasks import send_bulk_email_task
from tasks.tasks import send_bulk_email_task, send_email_task
from utils.uow import IUnitOfWork

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class NotificaionService:


    async def create_notification(self, notification: NotificationsCreateSchema, uow: IUnitOfWork):
        async with uow:
            try:
                logger.debug("Создание нотификации")
                notify_id = await uow.notifications.create(**notification.model_dump())

                logger.debug("Получение listeners")
                listeners: list[ListenersShcema] = await uow.listeners.get_all(user_id = notification.user_id)
                if not listeners:
                    raise HTTPException(status_code=404, detail="Firstli you must add listeners")
                
                logging.debug("Создание relationships")
                logger.debug([{notify_id:i.id} for i in listeners])
                await uow.listeners_notifications.create_multiple(values=[{'notification_id':notify_id, 'listener_id':i.id} for i in listeners])
                await uow.commit()
                return notify_id


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
                listeners_id = await uow.listeners_notifications.get_liteners_ids(notification_id=notification_id)
                listeners_emails = await uow.listeners.get_emails_by_id(ids=listeners_id)
                
                logger.debug('Получение notification')
                notification = await uow.notifications.get(id=notification_id)

                logger.debug("Отправка по почте ")
                send_bulk_email_task.delay(listeners_emails, notification.title, notification.body)
                logger.debug("CTOSH")
                

            except HTTPException as e:
                # await uow.rollback()
                logger.error(e)
                raise
            except Exception as e:
                # await uow.rollback()
                logger.error(e)
                raise HTTPException(status_code=500)
            

    async def get_notification(self, id: int, uow: IUnitOfWork):
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
