# import asyncio
# import pytest
# from typing import AsyncGenerator

# from sqlalchemy import create_engine
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
# from src.database import Base
# from config.app_config import settings

# from main import app

# @pytest.fixture(scope="module")
# def db_engine():
#     engine = create_engine(settings.DATABASE_URL_asyncpg, echo=True)
#     return engine

# @pytest.fixture(scope="module")
# async def db_session(db_engine):
#     async_session = async_sessionmaker(bind=db_engine)
    

#     # Создаем таблицы в памяти для тестов 
#     async with async_session.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     yield async_session

#     # Очищаем таблицы после тестов
#     async with async_session.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async_session.close()


# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="session")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac