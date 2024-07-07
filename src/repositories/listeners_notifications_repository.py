import logging
from sqlalchemy import select
from utils.repository import SQLAlchemyRepository
from models.listeners_notifications import ListenersNotifications

class ListenersNotificationsRepo(SQLAlchemyRepository):
    model = ListenersNotifications

    async def get_liteners_ids(self, notification_id: int):
        query = select(self.model.listener_id).filter_by(notification_id=notification_id)
        res = await self.session.execute(query)
        res = res.scalars().all()
        logging.debug(res)
        return res