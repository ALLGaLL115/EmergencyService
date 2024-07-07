import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Integer, Table, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from schemas.notifications_schemas import NotificationsShcema




class Notifications(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, )
    title = Column(String(64))
    body = Column(String(128))
    time_updated = Column(DateTime,  server_default=func.now(), onupdate=func.now())
    time_created = Column(DateTime, server_default=func.now())

    listeners = relationship(
        "Listeners",
        secondary="listeners_notifications",
        back_populates="notifications"
    )

    def convert_to_model(self):
        return NotificationsShcema(
            id = self.id,
            user_id = self.user_id,
            title = self.title,
            body = self.body,
            time_updated = self.time_updated,
            time_created = self.time_created,
        )


