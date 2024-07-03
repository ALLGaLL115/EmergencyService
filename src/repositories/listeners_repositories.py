from models.listener_models import Listeners
from repository import SQLAlchemyRepository


class ListenersRepository(SQLAlchemyRepository):
    model: Listeners