from abc import ABC

from fastapi import HTTPException, status
from database import Base
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError

import logging
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class SQLAlchemyRepositoryAbstract(ABC):


    async def get():
        raise NotImplemented
    

    async def get_all():
        raise NotImplemented


    async def create():
        raise NotImplemented
    

    async def update():
        raise NotImplemented
    

    async def delete():
        raise NotImplemented
    

class SQLAlchemyRepository(SQLAlchemyRepositoryAbstract):


    model = None


    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self, id: int):
        try: 
            logger.debug("start get request")
            stmt = select(self.model).filter_by(id=id)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res.convert_to_model()
        
        except InvalidRequestError as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This listener is not exists")
        
        except SQLAlchemyError as e:
            logger.error(e.args)
            logger.error(e._message)
            logger.error(e._sql_message)
            logger.error(e)
            raise

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)


    async def get_all(self, **filters):
        try:
            stmt = select(self.model).filter_by(**filters)
            res = await self.session.execute(stmt)
            res = res.scalars().all()
            return [i.convert_to_model() for i in res]
        
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)


    async def create(self, **data):
        try:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res
        
        except SQLAlchemyError as e:
            logger.error(e._message)
            raise HTTPException(500)

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)
            
        

    async def create_multiple(self, values: list[dict]):
        try:
            stmt = insert(self.model).values(values)
            await self.session.execute(stmt)
            
        
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)


    async def update(self, id: int, **data):
        try:
            stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res
        
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)


    async def delete(self, id:int):
        try:
            stmt = delete(self.model).filter_by(id=id).returning(self.model.id)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
            return res 
        
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(500)

        except Exception as e:
            logger.error(e)
            raise HTTPException(500)

    