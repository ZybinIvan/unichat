from typing import Annotated

from fastapi.params import Depends

from src.apps.user.repositories import UserRepository
from src.apps.user.services import UserService


def get_user_repository() -> UserRepository:
    return UserRepository()


UserRepositoryDepends = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDepends) -> UserService:
    return UserService(repository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]
