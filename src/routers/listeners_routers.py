from typing import Annotated
from fastapi import APIRouter, File, HTTPException, UploadFile

from dependencies import UOWDep
from schemas.listeners_schemas import ListenersCreateSchema
from services.listeners_services import ListenersService

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/listeners"
)


@router.get('/{id}')
async def listener(id: int,  uow: UOWDep):
    try: 
        response = await ListenersService().get_listener(id, uow)
        return response
    except HTTPException as e:
        raise 

    except Exception as e:
        logger.error(e)
        raise HTTPException(500)


@router.post('/add_listeners')
async def add_listeners(user_id: int, listeners_file: Annotated[UploadFile, File(description="Add .csv file with name, phone and email")], uow: UOWDep):
    try:
        await ListenersService().add_listeners(user_id, listeners_file, uow)
        return {"status":"success", "detail":"All listeners was added"}
    except HTTPException as e:
        raise 

    except Exception as e:
        logger.error(e)
        raise HTTPException(500)   
    

@router.get('/')
async def get_listeners(user_id: int, uow: UOWDep, offset: int = 0, limit: int = 30, ):
    try:
        response = await ListenersService().get_listeners(user_id, offset, limit, uow)
        return {'status': 'success', 'data':{'listeners': response}}
    
    except HTTPException as e:
        raise 

    except Exception as e:
        logger.error(e)
        raise HTTPException(500)   
    

@router.delete('/{listener_id}')
async def add(listener_id: int, uow: UOWDep):
    try:
        await ListenersService().delete_listener(listener_id, uow)
        return {'status': 'success', 'detail': f'listener with id {listener_id} was delete'}
        
    except HTTPException as e:
        raise 

    except Exception as e:
        logger.error(e)
        raise HTTPException(500)   


