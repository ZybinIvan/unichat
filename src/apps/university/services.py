from hmac import compare_digest

from fastapi import Request
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError

from src.apps.university.models import (
    UniversityModel,
)
from src.apps.university.repositories import (
    UniversityRepository,
)
from src.apps.university.schemas import (
    RegisterUniversitySchema,
)
from src.apps.user.models import UniversityAdminModel
from src.apps.user.repositories import UniversityAdminRepository


class UniversityService:
    def __init__(self, university_repository: UniversityRepository,
                 university_admin_repository: UniversityAdminRepository):
        self.university_repository = university_repository
        self.university_amin_repository = university_admin_repository

    async def create(
            self, request: Request, register_schema: RegisterUniversitySchema
    ) -> UniversityModel:
        if not compare_digest(
                register_schema.password.encode(), register_schema.password_repeat.encode()
        ):
            raise ValidationError("Пароли не совпадают")

        hashed_password = pbkdf2_sha256.hash(register_schema.password)

        university = UniversityModel(
            **register_schema.model_dump(include={"name"})
        )

        await self.university_repository.create(
            university, request.state.session
        )

        admin = UniversityAdminModel(
            password=hashed_password,
            university_id=university.id,
            **register_schema.model_dump(include={"first_name", "last_name", "patronymic", "email"})
        )

        await self.university_amin_repository.create(
            admin, request.state.session
        )

        return university
