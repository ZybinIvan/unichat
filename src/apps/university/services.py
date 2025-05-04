from hmac import compare_digest

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError

from src.apps.university.models import UniversityModel, InstituteModel, DepartmentModel, GroupModel
from src.apps.university.repositories import DepartmentRepository, UniversityRepository, InstituteRepository, \
    GroupRepository
from fastapi import Request

from src.apps.university.schemas import RegisterUniversitySchema, UniversityResponseSchema, InstituteCreateSchema, \
    DepartmentCreateSchema, GroupCreateSchema


class UniversityService:
    def __init__(self, university_repository: UniversityRepository):
        self.university_repository = university_repository

    async def create(self, request: Request, register_schema: RegisterUniversitySchema) -> UniversityModel:
        if not compare_digest(register_schema.password.encode(), register_schema.password_repeat.encode()):
            raise ValidationError('Пароли не совпадают')

        register_schema.password = pbkdf2_sha256.hash(register_schema.password)

        university: UniversityModel = UniversityModel(**register_schema.model_dump(exclude={"password_repeat"}))

        return await self.university_repository.create(university, request.state.session)


class InstituteService:
    def __init__(self, institute_repository: InstituteRepository):
        self.institute_repository = institute_repository

    async def create(self, request: Request, create_schema: InstituteCreateSchema) -> InstituteModel:
        institute: InstituteModel = InstituteModel(**create_schema.model_dump())
        return await self.institute_repository.create(institute, request.state.session)


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    async def create(self, request: Request, create_schema: DepartmentCreateSchema) -> DepartmentModel:
        department: DepartmentModel = DepartmentModel(**create_schema.model_dump())
        return await self.department_repository.create(department, request.state.session)


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def create(self, request: Request, create_schema: GroupCreateSchema) -> GroupModel:
        group: GroupModel = GroupModel(**create_schema.model_dump())
        return await self.group_repository.create(group, request.state.session)
