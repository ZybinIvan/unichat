from hmac import compare_digest

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.user.models import UserModel
from src.apps.user.repositories import UserRepository
from src.apps.user.schemas import UserRegisterSchema


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, register_schema: UserRegisterSchema, session: AsyncSession) -> UserModel:
        if not compare_digest(register_schema.password.encode(), register_schema.password_repeat.encode()):
            raise ValidationError('Пароли не совпадают')

        register_schema.password = pbkdf2_sha256.hash(register_schema.password)

        user: UserModel = UserModel(**register_schema.model_dump(exclude={"password_repeat"}))

        created_user: UserModel = await self.user_repository.create(user, session)

        return created_user
