import time
from datetime import datetime
from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, func, String
from sqlalchemy.orm import Mapped, mapped_column

from schemas.listeners_schemas import ListenersShcema



class Listeners(Base):
    __tablename__="listeners"
    id = Column(Integer, primary_key=True)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False, unique=True)
    phone = Column(String(18), nullable=True)
    email = Column(String(128), nullable=False)

    def convert_to_model(self):
        return ListenersShcema(
            id = self.id,
            # owner_id = self.owner_id,
            name = self.name,
            phone = self.phone,
            email = self.email,
        )

