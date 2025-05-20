from starlette.requests import Request

from src.apps.university.group.repositories import GroupRepository
from src.apps.university.group.schemas import GroupCreateSchema, GroupDetailSchema, GroupFilter, GroupUpdateSchema, \
    GroupListResponseSchema
from src.apps.university.models import GroupModel


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
        return GroupDetailSchema(id=group.id, name=group.name, institute=group.department.institute,
                                 department=group.department)

    async def list(self, request: Request, limit: int, skip: int, filters: GroupFilter) -> GroupListResponseSchema:
        items, count = await self.group_repository.list(
            limit, skip, request.state.session, filters, department__institute__university_id=request.user.university_id
        )
        return GroupListResponseSchema(total_count=count, data=items)

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
