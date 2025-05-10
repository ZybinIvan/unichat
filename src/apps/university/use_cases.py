from starlette.requests import Request

from src.apps.university.models import InstituteModel, DepartmentModel, GroupModel
from src.apps.university.schemas import (
    DepartmentFilter,
    DepartmentUpdateSchema,
    GroupFilter,
    GroupUpdateSchema,
    InstituteCreateSchema,
    InstituteFilter,
    InstituteResponseSchema,
    DepartmentCreateSchema,
    DepartmentResponseSchema,
    GroupCreateSchema,
    GroupResponseSchema,
    InstituteUpdateSchema,
)
from src.apps.university.services import (
    InstituteService,
    DepartmentService,
    GroupService,
)


class CreateInstituteUseCase:
    def __init__(self, institute_service: InstituteService):
        self.institute_service = institute_service

    async def __call__(
        self, request: Request, create_schema: InstituteCreateSchema
    ) -> InstituteResponseSchema:
        created_institute: InstituteModel = await self.institute_service.create(
            request, create_schema
        )
        return InstituteResponseSchema.model_validate(
            created_institute, from_attributes=True
        )


class ListInstitutesUseCase:
    def __init__(self, service: InstituteService):
        self.service = service

    async def __call__(
        self, request: Request, limit: int, skip: int, filters: InstituteFilter
    ):
        return await self.service.list(request, limit, skip, filters)


class UpdateInstituteUseCase:
    def __init__(self, service: InstituteService):
        self.service = service

    async def __call__(
        self, request: Request, institute_id: int, update_schema: InstituteUpdateSchema
    ):
        return await self.service.update(request, institute_id, update_schema)


class DeleteInstituteUseCase:
    def __init__(self, service: InstituteService):
        self.service = service

    async def __call__(self, request: Request, institute_id: int):
        await self.service.delete(request, institute_id)


class ListDepartmentsUseCase:
    def __init__(self, service: DepartmentService):
        self.service = service

    async def __call__(
        self, request: Request, limit: int, skip: int, filters: DepartmentFilter
    ):
        return await self.service.list(request, limit, skip, filters)


class UpdateDepartmentUseCase:
    def __init__(self, service: DepartmentService):
        self.service = service

    async def __call__(
        self,
        request: Request,
        department_id: int,
        update_schema: DepartmentUpdateSchema,
    ):
        return await self.service.update(request, department_id, update_schema)


class DeleteDepartmentUseCase:
    def __init__(self, service: DepartmentService):
        self.service = service

    async def __call__(self, request: Request, department_id: int):
        await self.service.delete(request, department_id)


class CreateDepartmentUseCase:
    def __init__(self, department_service: DepartmentService):
        self.department_service = department_service

    async def __call__(
        self, request: Request, create_schema: DepartmentCreateSchema
    ) -> DepartmentResponseSchema:
        department: DepartmentModel = await self.department_service.create(
            request, create_schema
        )
        return DepartmentResponseSchema.model_validate(department, from_attributes=True)


class CreateGroupUseCase:
    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def __call__(
        self, request: Request, create_schema: GroupCreateSchema
    ) -> GroupResponseSchema:
        group: GroupModel = await self.group_service.create(request, create_schema)
        return GroupResponseSchema.model_validate(group, from_attributes=True)


class ListGroupsUseCase:
    def __init__(self, service: GroupService):
        self.service = service

    async def __call__(
        self, request: Request, limit: int, skip: int, filters: GroupFilter
    ):
        return await self.service.list(request, limit, skip, filters)


class UpdateGroupUseCase:
    def __init__(self, service: GroupService):
        self.service = service

    async def __call__(
        self, request: Request, group_id: int, update_schema: GroupUpdateSchema
    ):
        return await self.service.update(request, group_id, update_schema)


class DeleteGroupUseCase:
    def __init__(self, service: GroupService):
        self.service = service

    async def __call__(self, request: Request, group_id: int):
        await self.service.delete(request, group_id)
