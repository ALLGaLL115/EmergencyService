import csv
from fastapi import HTTPException, UploadFile, status
from fastapi.responses import JSONResponse

from schemas.listeners_schemas import ListenersCreateSchema
from utils.uow import UnitOfWork, IUnitOfWork

import os
import pandas as pd
from io import StringIO

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
                # listeners = await uow.listeners.get_multiple(limit=limit, offset=offset)
                logger.info("Данные полученны успешно")
                await uow.commit()
                return listeners
            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise

            except Exception as e:
                await uow.rollback()
                logger.error(e)
                raise HTTPException(500)

                
    async def add_listeners(self, user_id: int, listeners_file: UploadFile, uow: IUnitOfWork) -> None:
        async with uow:
            try:
                if os.path.splitext(listeners_file.filename)[1] != ".csv":
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This file have not .csv extension")
                
                logger.info("Обработка входного файла")
                bytes_string = str(await listeners_file.read(), 'utf-8')
                df = pd.read_csv(StringIO(bytes_string))
                columns_to_check = ListenersCreateSchema.model_fields.keys()

                if not set(columns_to_check).issubset(df.columns):
                    missing_columns = set(columns_to_check) - set(df.columns)
                    raise HTTPException(status_code=400, detail="Отсутствуют следующие столбцы: {missing_columns}")
                
                df['phone'] = df['phone'].astype(str)
                df['phone'] = df['phone'].fillna('').astype(str)
                handled_listeners: list[dict] = df.filter(columns_to_check).to_dict(orient='records')

                for i in handled_listeners:
                    i["user_id"]=user_id

                logger.info('Запрос на созранение пользователей в бд')
                await uow.listeners.create_multiple(listeners=handled_listeners)
                await uow.commit()
                logger.info("Запрос отработал успешно")

                # Можно добавлять csv файлы с разными столбцами сервис получит только нужные столбцы

            except HTTPException as e:
                await uow.rollback()
                logger.error(e)
                raise  
            
            except Exception as e :
                await uow.rollback()
                logger.error(e)
                logger.error(e.args)
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
            
    
            
    
 