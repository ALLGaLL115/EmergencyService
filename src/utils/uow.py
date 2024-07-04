from abc import ABC, abstractmethod
from typing import Type
from database import async_session_maker
from repositories.listeners_repositories import ListenersRepository
from repositories.notifications_repositories import NotificationsRepository



class IUnitOfWork(ABC):
    listeners: Type[ListenersRepository]
    notifications: Type[NotificationsRepository]

    
    def __init__(self):
        raise NotImplemented
    
    
    async def __aenter__(self):
        raise NotImplemented


    async def __aexit__(self, *args):
        raise NotImplemented


    async def rollback(self):
        raise NotImplemented


    async def commit(self):
        raise NotImplemented



class UnitOfWork(IUnitOfWork):


    def __init__(self, ):
        self.session_factory = async_session_maker

    
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
        
        

