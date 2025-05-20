from starlette.requests import Request

from src.apps.university.department.schemas import DepartmentFilter, DepartmentCreateSchema, DepartmentUpdateSchema
from src.apps.university.department.services import DepartmentService
from src.apps.university.models import DepartmentModel


class RetrieveDepartmentUseCase:
    def __init__(self, service: DepartmentService):
        self.service = service

    async def __call__(self, request: Request, department_id: int):
        return await self.service.get(request, department_id)


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
    ) -> int:
        department: DepartmentModel = await self.department_service.create(
            request, create_schema
        )
        return department.id
