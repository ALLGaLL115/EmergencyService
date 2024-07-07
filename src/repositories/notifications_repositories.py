
from utils.repository import SQLAlchemyRepository

from models.notifications_models import Notifications


class NotificationsRepository(SQLAlchemyRepository):
    model = Notifications