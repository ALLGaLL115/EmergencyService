import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dependencies import UOWDep
from schemas.notifications_schemas import NotificationsCreateSchema
from services.notifications_services import NotificaionService

from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"])



@router.post('/create')
async def create_notification(notification: NotificationsCreateSchema, uow: UOWDep):
    try:
        notify_id = await NotificaionService().create_notification(notification, uow)
        return JSONResponse(content=f"Notification {notify_id} was created")


    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"router error {e}")
        raise HTTPException(500)


@router.post('/send/{id}')
async def send_notification(id: int, uow: UOWDep):
    try:
        await NotificaionService().send_notification(id, uow)

        return JSONResponse(content="Notifications was sended")
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"router error {e}")
        raise HTTPException(500)


@router.get('/{id}')
async def get_notification(id:int, uow: UOWDep):
    try:
        notifycation = await NotificaionService().get_notification(id, uow)
        return notifycation
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"router error {e}")
        raise HTTPException(500)


@router.delete("/{id}")
async def delete_notification(id: int, uow: UOWDep):
    try:
        notify_id = await NotificaionService().delete_notification(id, uow)
        return JSONResponse(content=f"Notification {notify_id}")
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"router error {e}")
        raise HTTPException(500)



