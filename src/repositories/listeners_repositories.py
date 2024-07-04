from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from models.listener_models import Listeners
from utils.repository import SQLAlchemyRepository
from schemas.listeners_schemas import ListenersCreateSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class ListenersRepository(SQLAlchemyRepository):
    model= Listeners

    async def create_multiple(self, listeners: list[dict]):
        try:
            logger.debug("Отправка данных в бд")
            stmt = insert(self.model).values(listeners)
            stmt = stmt.on_conflict_do_update(
                index_elements=['name'],
                set_={'phone': stmt.excluded.phone, 'email': stmt.excluded.email}
            )
            await self.session.execute(stmt)

        except IntegrityError as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This user is already exists")

        except SQLAlchemyError as e:
            logger.error(e)
            logger.error(e._message)
            raise HTTPException(500)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(500)

    
    # async def get_multiple(self, user_id: int, limit: int, offset: int):
    async def get_multiple(self, limit: int, offset: int):
        try:
            logger.debug("Запрос на получение данных из бд")
            # stmt = select(self.model).filter_by(owner_id=user_id).limit(limit).offset(offset)
            stmt = select(self.model).limit(limit).offset(offset)
            respnonse = await self.session.execute(stmt)
            listeners = respnonse.scalars().all()
            return [i.convert_to_model() for i in listeners]

        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)
        
        except Exception as e:
            logger.error(e)
            raise HTTPException(500)