import csv
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from schemas.listeners_schemas import ListenersCreateSchema
from uow import IUnitOfWork

import os
import pandas as pd

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)




class ListenersService:

    async def get_listener(self, id: int, uow: IUnitOfWork):
        async with uow:
            logging.debug('Запрос на получение listener')
            try:
                listener = await uow.listeners.get(id=id)
                logger.info("Данные полученны успешно")
                return JSONResponse(content=listener)
            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise

            except Exception as e:
                await uow.rollback()
                logger.error(e)
                raise HTTPException(500)
    

    async def get_listeners(self, user_id: int, offset: int, limit: int, uow: IUnitOfWork):
        async with uow:
            logging.debug('Запрос на получение listener')
            try:
                listeners = await uow.listeners.get_multiple(user_id=user_id, limit=limit, offset=offset)
                logger.info("Данные полученны успешно")
                return listeners
            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise

            except Exception as e:
                await uow.rollback()
                logger.error(e)
                raise HTTPException(500)

                
    async def add_listeners(self, listeners_file: UploadFile, uow: IUnitOfWork) -> None:
        async with uow:
            try:
                if os.path.splitext(listeners_file.filename)[1] != ".csv":
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This file have not .csv extension")
                
                logger.debug("Обработка входного файла")
                df = pd.read_csv(listeners_file.read())
                handled_listeners: list = df.values.tolist()
                del handled_listeners
                print(handled_listeners)
                
                logging.debug('Запрос на созранение пользователей в бд')
                await uow.listeners.create_multiple(listeners=handled_listeners)
                await uow.commit()
                logger.info("Запрос отработал успешно")

            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise  
            
            except Exception as e :
                await uow.rollback()
                logger.error(e)
                raise HTTPException(500)
            
    
    async def delete_listener(self, id: int, uow: IUnitOfWork):
        async with uow:
            try:
                logging.debug('Запрос на удаление пользователей в бд')
                await uow.listeners.delete(id=id)
                await uow.commit()
                logger.info("Запрос отработал успешно")

            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise  
            
            except Exception as e :
                await uow.rollback()
                logger.error(e)
                raise HTTPException(500)
            
    
            
    
 