import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Integer, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from schemas.notifications_schemas import NotificationsShcema


class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False, )
    content = Column(String(128))
    listeners_link = Column(String)
    time_updated = Column(DateTime, onupdate=func.now())
    time_created = Column(DateTime, server_default=func.now())

    def convert_to_model(self):
        return NotificationsShcema(
            id = self.id,
            owner_id = self.owner_id,
            content = self.content,
            listeners_link = self.listeners_link,
            time_updated = self.time_updated,
            time_created = self.time_created,
        )
    