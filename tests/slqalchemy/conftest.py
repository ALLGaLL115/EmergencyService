import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database import Base
from models.listener_models import Listeners
from config.app_config import settings
from utils.uow import IUnitOfWork, UnitOfWork


async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)
async_session_maker = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def set_up_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
 

@pytest.fixture()
async def tuow():
    class TestUOW(UnitOfWork):
        def __init__(self):
            self.session_factory = async_session_maker
    
    yield TestUOW()




