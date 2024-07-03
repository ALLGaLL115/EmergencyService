import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, Integer, func, String
from sqlalchemy.orm import Mapped, mapped_column

from schemas.listeners_schemas import ListenersShcema



class Listeners(Base):
    __tablename__="listeners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String(18), nullable=True)
    email = Column(String(128), nullable=False)

    def convert_to_model(self):
        return ListenersShcema(
            id = self.id,
            name = self.name,
            phone = self.phone,
            email = self.email,
        )

