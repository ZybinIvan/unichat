from src.apps.auth.schemas import TokenSchema
from src.apps.auth.services import JWTService
from src.apps.user.services import UserService

from fastapi import Request


class AuthUseCase:
    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def __call__(self, reqeust: Request) -> TokenSchema:
        ...
