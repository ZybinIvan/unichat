from starlette.requests import Request

from src.apps.university.institute.repositories import InstituteRepository
from src.apps.university.models import InstituteModel
from src.apps.university.schemas import InstituteCreateSchema, InstituteFilter, InstituteUpdateSchema


class InstituteService:
    def __init__(self, institute_repository: InstituteRepository):
        self.institute_repository = institute_repository

    async def create(
            self, request: Request, create_schema: InstituteCreateSchema
    ) -> InstituteModel:
        institute = InstituteModel(university_id=request.user.university_id,
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
