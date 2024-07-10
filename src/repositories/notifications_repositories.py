
import logging
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from config.logging_config import setup_logging
from utils.repository import SQLAlchemyRepository
from models.notifications_models import Notifications

setup_logging()
logger = logging.getLogger(__name__)

class NotificationsRepository(SQLAlchemyRepository):
    model = Notifications

    async def get(self, id: int):
        try:
            stmt = select(self.model).filter_by(id=id).options(selectinload(self.model.listeners))  
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res.convert_to_model()
        except InvalidRequestError as e:
            logger.error(e)
            raise HTTPException(status_code=404, detail="This listener is not exists")
        
        except SQLAlchemyError as e:
            logger.error(e.args)
            logger.error(e._message)
            logger.error(e._sql_message)
            logger.error(e)
            raise

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)