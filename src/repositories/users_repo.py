from models.users_model import Users
from utils.repository import SQLAlchemyRepository


class UsersRepo(SQLAlchemyRepository):
    model = Users