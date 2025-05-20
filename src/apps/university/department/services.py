from starlette.requests import Request

from src.apps.university.department.repositories import DepartmentRepository
from src.apps.university.department.schemas import *
from src.apps.university.models import DepartmentModel


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
    ) -> DepartmentListResponseSchema:
        items, count = await self.department_repository.list(
            limit, skip, request.state.session, filters, institute__university_id=request.user.university_id
        )

        return DepartmentListResponseSchema(data=items, total_count=count)

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
