from datetime import datetime
from pydantic import BaseModel

from schemas.listeners_schemas import ListenersShcema

class NotificationsCreateSchema(BaseModel):
    user_id: int
    title: str
    body: str


class NotificationsShcema(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    listeners: list
    time_updated: datetime
    time_created: datetime


