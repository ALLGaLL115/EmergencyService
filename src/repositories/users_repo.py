from models.users_model import Users
from repository import SQLAlchemyRepository


class UsersRepo(SQLAlchemyRepository):
    model = Users