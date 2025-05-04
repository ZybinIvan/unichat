from starlette.requests import Request

from src.apps.university.models import InstituteModel, DepartmentModel, GroupModel
from src.apps.university.schemas import InstituteCreateSchema, InstituteResponseSchema, DepartmentCreateSchema, \
    DepartmentResponseSchema, GroupCreateSchema, GroupResponseSchema
from src.apps.university.services import InstituteService, DepartmentService, GroupService


class CreateInstituteUseCase:
    def __init__(self, institute_service: InstituteService):
        self.institute_service = institute_service

    async def __call__(self, request: Request, create_schema: InstituteCreateSchema) -> InstituteResponseSchema:
        created_institute: InstituteModel = await self.institute_service.create(request, create_schema)
        return InstituteResponseSchema.model_validate(created_institute, from_attributes=True)


class CreateDepartmentUseCase:
    def __init__(self, department_service: DepartmentService):
        self.department_service = department_service

    async def __call__(self, request: Request, create_schema: DepartmentCreateSchema) -> DepartmentResponseSchema:
        department: DepartmentModel = await self.department_service.create(request, create_schema)
        return DepartmentResponseSchema.model_validate(department, from_attributes=True)


class CreateGroupUseCase:
    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def __call__(self, request: Request, create_schema: GroupCreateSchema) -> GroupResponseSchema:
        group: GroupModel = await self.group_service.create(request, create_schema)
        return GroupResponseSchema.model_validate(group, from_attributes=True)
