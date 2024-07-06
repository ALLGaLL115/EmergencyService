from repository import SQLAlchemyRepository
from models.listeners_notifications import listeners_notifications

class ListenersNotificationsRepo(SQLAlchemyRepository):
    model = listeners_notifications