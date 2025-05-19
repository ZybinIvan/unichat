from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Query
from fastapi_filter import FilterDepends

from src.apps.university.group.schemas import GroupCreateSchema, GroupResponseSchema, GroupDetailSchema, GroupFilter, \
    GroupUpdateSchema
from src.apps.university.group.use_cases import CreateGroupUseCase, RetrieveGroupUseCase, ListGroupsUseCase, \
    UpdateGroupUseCase, DeleteGroupUseCase

group_router = APIRouter(route_class=DishkaRoute, tags=["Group"])


@group_router.post("/groups", response_model=int)
async def create_group(
        request: Request,
        create_schema: GroupCreateSchema,
        use_case: FromDishka[CreateGroupUseCase],
):
    return await use_case(request, create_schema)


@group_router.get("/groups/{group_id}", response_model=GroupDetailSchema)
async def get_group(
        request: Request,
        group_id: int,
        use_case: FromDishka[RetrieveGroupUseCase],
):
    return await use_case(request, group_id)


@group_router.get("/groups", response_model=list[GroupResponseSchema])
async def list_groups(
        request: Request,
        use_case: FromDishka[ListGroupsUseCase],
        limit: int = Query(lte=100, gte=5, default=5),
        skip: int = 0,
        filters: GroupFilter = FilterDepends(GroupFilter),
):
    return await use_case(request, limit, skip, filters)


@group_router.patch("/groups/{group_id}", response_model=GroupResponseSchema)
async def update_group(
        request: Request,
        group_id: int,
        update_schema: GroupUpdateSchema,
        use_case: FromDishka[UpdateGroupUseCase],
):
    return await use_case(request, group_id, update_schema)


@group_router.delete("/groups/{group_id}", status_code=204)
async def delete_group(
        request: Request,
        group_id: int,
        use_case: FromDishka[DeleteGroupUseCase],
):
    await use_case(request, group_id)
