from abc import ABC, abstractmethod
from typing import Type
from database import async_session_maker
from repositories.listeners_notifications_repository import ListenersNotificationsRepo
from repositories.listeners_repositories import ListenersRepository
from repositories.notifications_repositories import NotificationsRepository
from repositories.users_repo import UsersRepo



class IUnitOfWork(ABC):
    users: Type[UsersRepo]
    listeners: Type[ListenersRepository]
    notifications: Type[NotificationsRepository]
    listeners_notifications: Type[ListenersNotificationsRepo]
    
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
        self.listeners_notifications = ListenersNotificationsRepo(self.session)
        self.users = UsersRepo(self.session)
        return self

    
    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    
    async def rollback(self):
        await self.session.rollback()
      

    async def commit(self):
        await self.session.commit()
        
        

