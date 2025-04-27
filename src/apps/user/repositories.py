from src.apps.user.models import UserModel
from src.core.repositories import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel

    