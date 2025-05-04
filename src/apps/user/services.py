import logging

import sqlalchemy

from hmac import compare_digest
from typing import Any

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError
from fastapi import Request

from src.apps.university.schemas import RegisterTeacherSchema, RegisterStudentSchema
from src.apps.user.models import UserModel, TeacherModel, StudentModel
from src.apps.user.repositories import UserRepository, TeacherRepository, StudentRepository
from src.apps.user.schemas import UserRegisterSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create(self, request: Request, register_schema: UserRegisterSchema) -> UserModel:
        if not compare_digest(register_schema.password.encode(), register_schema.password_repeat.encode()):
            raise ValidationError('Пароли не совпадают')

        register_schema.password = pbkdf2_sha256.hash(register_schema.password)

        user: UserModel = UserModel(**register_schema.model_dump(exclude={"password_repeat"}))

        created_user: UserModel = await self.user_repository.create(user, request.state.session)

        return created_user

    async def get_by_field(
            self,
            request: Request,
            **lookup: Any
    ) -> UserModel:
        """
        Получить пользователя по любому полю, например:
        await user_service.get_by_field(request, email="user@example.com")
        """
        try:
            user = await self.user_repository.get_by(
                session=request.state.session,
                **lookup
            )
            return user
        except Exception as e:
            logger.exception(e)
            raise e


class TeacherService:
    def __init__(self, repository: TeacherRepository):
        self.repository = repository

    async def create(self, request: Request, register_schema: RegisterTeacherSchema) -> 'TeacherModel':
        if not compare_digest(register_schema.password, register_schema.password_repeat):
            raise ValidationError('Пароли не совпадают')
        hashed = pbkdf2_sha256.hash(register_schema.password)
        model_data = register_schema.model_dump(exclude={'password_repeat'})
        model_data['password'] = hashed
        teacher = TeacherModel(**model_data)
        return await self.repository.create(teacher, request.state.session)


class StudentService:
    def __init__(self, repository: StudentRepository):
        self.repository = repository

    async def create(self, request: Request, register_schema: RegisterStudentSchema) -> StudentModel:
        if not compare_digest(register_schema.password, register_schema.password_repeat):
            raise ValidationError('Пароли не совпадают')
        hashed = pbkdf2_sha256.hash(register_schema.password)
        model_data = register_schema.model_dump(exclude={'password_repeat'})
        model_data['password'] = hashed
        student = StudentModel(**model_data)
        return await self.repository.create(student, request.state.session)
