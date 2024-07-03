from fastapi import HTTPException
from sqlalchemy import insert, select
from models.listener_models import Listeners
from repository import SQLAlchemyRepository
from schemas.listeners_schemas import ListenersCreateSchema
from sqlalchemy.exc import SQLAlchemyError

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class ListenersRepository(SQLAlchemyRepository):
    model: Listeners

    async def create_multiple(self, listeners: list[dict]):
        try:
            logger.debug("Отправка данных в бд")
            stmt = insert(self.model).values(*listeners)
            await self.session.execute(stmt)

        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(500)

    
    async def get_multiple(self, user_id: int, limit: int, offset: int):
        try:
            logger.debug("Запрос на получение данных из бд")
            stmt = select(self.model).filter_by(owner_id=user_id).limit(limit).offset(offset)
            respnonse = await self.session.execute(stmt)
            listeners = respnonse.scalars().all()
            return [i.convert_to_model for i in listeners]

        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(500)