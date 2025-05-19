from starlette.requests import Request

from src.apps.university.group.schemas import GroupCreateSchema, GroupFilter, GroupUpdateSchema, GroupResponseSchema
from src.apps.university.group.services import GroupService
from src.apps.university.models import GroupModel


class CreateGroupUseCase:
    def __init__(self, group_service: GroupService):
        self.group_service = group_service

    async def __call__(
            self, request: Request, create_schema: GroupCreateSchema
    ) -> int:
        group: GroupModel = await self.group_service.create(request, create_schema)
        return group.id


class RetrieveGroupUseCase:
    def __init__(self, service: GroupService):
        self.service = service

    async def __call__(self, request: Request, group_id: int):
        return await self.service.get(request, group_id)


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
