from hmac import compare_digest
from fastapi import Request
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from pydantic import ValidationError

from src.apps.university.models import (
    UniversityModel,
    InstituteModel,
    DepartmentModel,
    GroupModel,
)
from src.apps.university.repositories import (
    DepartmentRepository,
    UniversityRepository,
    InstituteRepository,
    GroupRepository,
)

from src.apps.university.schemas import (
    DepartmentDetailSchema,
    DepartmentFilter,
    DepartmentUpdateSchema,
    GroupFilter,
    GroupUpdateSchema,
    RegisterUniversitySchema,
    InstituteCreateSchema,
    DepartmentCreateSchema,
    GroupCreateSchema,
    InstituteFilter,
    InstituteUpdateSchema, GroupDetailSchema,
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


class InstituteService:
    def __init__(self, institute_repository: InstituteRepository):
        self.institute_repository = institute_repository

    async def create(
            self, request: Request, create_schema: InstituteCreateSchema
    ) -> InstituteModel:
        institute: InstituteModel = InstituteModel(university_id=request.state.user.university_id,
                                                   **create_schema.model_dump())
        return await self.institute_repository.create(institute, request.state.session)

    async def get(self, request: Request, institute_id: int) -> InstituteModel:
        return await self.institute_repository.get_by(
            request.state.session, id=institute_id
        )

    async def list(
            self, request: Request, limit: int, skip: int, filters: InstituteFilter
    ):
        return await self.institute_repository.list(
            limit, skip, request.state.session, filters
        )

    async def update(
            self, request: Request, institute_id: int, update_schema: InstituteUpdateSchema
    ):
        instance = await self.institute_repository.get_by(
            request.state.session, id=institute_id
        )
        for key, value in update_schema.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        return await self.institute_repository.update(instance, request.state.session)

    async def delete(self, request: Request, institute_id: int):
        await self.institute_repository.delete(
            institute_id,
            request.state.session,
        )


class DepartmentService:
    def __init__(self, department_repository: DepartmentRepository):
        self.department_repository = department_repository

    async def create(
            self, request: Request, create_schema: DepartmentCreateSchema
    ) -> DepartmentModel:
        department: DepartmentModel = DepartmentModel(**create_schema.model_dump())
        return await self.department_repository.create(
            department, request.state.session
        )

    async def get(self, request: Request, department_id: int) -> DepartmentDetailSchema:
        department = await self.department_repository.get_detail(
            department_id, request.state.session,
        )
        return DepartmentDetailSchema(
            id=department.id,
            name=department.name,
            institute=department.institute
        )

    async def list(
            self, request: Request, limit: int, skip: int, filters: DepartmentFilter
    ):
        return await self.department_repository.list(
            limit, skip, request.state.session, filters
        )

    async def update(
            self,
            request: Request,
            department_id: int,
            update_schema: DepartmentUpdateSchema,
    ):
        instance = await self.department_repository.get_by(
            request.state.session, id=department_id
        )
        for key, value in update_schema.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        return await self.department_repository.update(instance, request.state.session)

    async def delete(self, request: Request, department_id: int):
        await self.department_repository.delete(department_id, request.state.session)


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def create(
            self, request: Request, create_schema: GroupCreateSchema
    ) -> GroupModel:
        group: GroupModel = GroupModel(**create_schema.model_dump())
        return await self.group_repository.create(group, request.state.session)

    async def get(self, request: Request, group_id: int) -> GroupDetailSchema:
        group = await self.group_repository.get_detail(group_id, request.state.session)
        return GroupDetailSchema(id=group.id, name=group.name, institute_name=group.department.institute.name,
                                 department_name=group.department.name)

    async def list(self, request: Request, limit: int, skip: int, filters: GroupFilter):
        return await self.group_repository.list(
            limit, skip, request.state.session, filters
        )

    async def update(
            self, request: Request, group_id: int, update_schema: GroupUpdateSchema
    ):
        instance = await self.group_repository.get_by(
            request.state.session, id=group_id
        )
        for key, value in update_schema.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)
        return await self.group_repository.update(instance, request.state.session)

    async def delete(self, request: Request, group_id: int):
        await self.group_repository.delete(group_id, request.state.session)
