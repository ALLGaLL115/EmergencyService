from datetime import datetime
from pydantic import BaseModel

class NotificationsShcema(BaseModel):
    id: int
    owner_id: int
    content: str
    listeners_link: str
    time_updated: datetime
    time_created: datetime


