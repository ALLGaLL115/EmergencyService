import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schemas.listeners_schemas import ListenersShcema
from models.listeners_notifications import listeners_notifications




class Listeners(Base):
    __tablename__="listeners"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False, unique=True)
    phone = Column(String(18), nullable=True)
    email = Column(String(128), nullable=False)

    notifications =  relationship("Notifications", secondary='ListenersNotifications', back_populates="listeners")

    def convert_to_model(self):
        return ListenersShcema(
            id = self.id,
            user_id = self.user_id,
            name = self.name,
            phone = self.phone,
            email = self.email,
        )

