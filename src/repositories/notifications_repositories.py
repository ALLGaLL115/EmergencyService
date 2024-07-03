

from database import Base
from models.notifications_models import Notifications


class NotificationsRepository(Base):
    model: Notifications