import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Integer, Table, func, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from schemas.notifications_schemas import NotificationsShcema





class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    time_updated = Column(DateTime, onupdate=func.now())
    time_created = Column(DateTime, server_default=func.now())

    def convert_to_model(self):
        return NotificationsShcema(
            id = self.id,
            name = self.name,
            time_updated = self.time_updated,
            time_created = self.time_created,
        )