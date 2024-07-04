import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

from config.app_config import settings
from database import Base
from main import app

from repositories.listeners_repositories import ListenersRepository
from repositories.notifications_repositories import NotificationsRepository
from utils.uow import IUnitOfWork, UnitOfWork
from utils.repository import SQLAlchemyRepository



class TestModel(Base):
    __tablename__ = 'test_model'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    email = Column(String)

    def convert_to_model(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class TestRepository(SQLAlchemyRepository):
    model = TestModel

        

@pytest_asyncio.fixture(scope="module")
async def db_engine():
    engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


class UnitOfWorkOverride(IUnitOfWork):


    def __init__(self, ):
        self.session_factory = async_sessionmaker(db_engine)

    
    async def __aenter__(self):
        self.session = self.session_factory()
        self.listeners = ListenersRepository(self.session)
        self.notifications = NotificationsRepository(self.session)
        return self

    
    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    
    async def rollback(self):
        await self.session.rollback()
      

    async def commit(self):
        await self.session.commit()


app.dependency_overrides[UnitOfWork] = UnitOfWorkOverride

@pytest_asyncio.fixture(scope="module")
async def db_session(db_engine):
    async_session = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def sqlalchemy_repository(db_session):
    return TestRepository(session=db_session)
