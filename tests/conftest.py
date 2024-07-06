# import asyncio
# import pytest
# from typing import AsyncGenerator

# from sqlalchemy import create_engine
# from httpx import AsyncClient
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# from src.database import Base
# from config.app_config import settings

# from main import app

# async_engine = create_async_engine(settings.DATABASE_URL_asyncpg)

# async_session_maker = async_sessionmaker(bind=async_engine)



# @pytest.fixture(scope="function", autouse=True)
# async def set_up_db():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     yield
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
 


# @pytest.fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# # @pytest.fixture(scope="session")
# # async def ac() -> AsyncGenerator[AsyncClient, None]:
# #     async with AsyncClient(app=app, base_url="http://test") as ac:
# #         yield ac