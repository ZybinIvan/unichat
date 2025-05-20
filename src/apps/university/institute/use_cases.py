from starlette.requests import Request

from src.apps.university.institute.schemas import InstituteCreateSchema, InstituteFilter, InstituteUpdateSchema
from src.apps.university.institute.services import InstituteService
from src.apps.university.models import InstituteModel


class CreateInstituteUseCase:
    def __init__(self, institute_service: InstituteService):
        self.institute_service = institute_service

    async def __call__(
            self, request: Request, create_schema: InstituteCreateSchema
    ) -> int:
        created_institute: InstituteModel = await self.institute_service.create(
            request, create_schema
        )
        return created_institute.id


class RetrieveInstituteUseCase:
    def __init__(self, service: InstituteService):
        self.service = service

    async def __call__(self, request: Request, institute_id: int):
        return await self.service.get(request, institute_id)


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
