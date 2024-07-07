from datetime import datetime
from pydantic import BaseModel

class NotificationsCreateSchema(BaseModel):
    user_id: int
    title: str
    body: str


class NotificationsShcema(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    time_updated: datetime
    time_created: datetime


