from dishka import FromDishka
from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from starlette.requests import Request
from dishka.integrations.fastapi import DishkaRoute

from src.apps.university.schemas import (
    DepartmentFilter,
    DepartmentUpdateSchema,
    GroupFilter,
    GroupUpdateSchema,
    InstituteFilter,
    InstituteResponseSchema,
    InstituteCreateSchema,
    DepartmentCreateSchema,
    DepartmentResponseSchema,
    GroupResponseSchema,
    GroupCreateSchema,
    InstituteUpdateSchema,
)

from .use_cases import (
    CreateDepartmentUseCase,
    CreateGroupUseCase,
    CreateInstituteUseCase,
    DeleteDepartmentUseCase,
    DeleteGroupUseCase,
    DeleteInstituteUseCase,
    ListDepartmentsUseCase,
    ListGroupsUseCase,
    ListInstitutesUseCase,
    UpdateDepartmentUseCase,
    UpdateGroupUseCase,
    UpdateInstituteUseCase,
)


university_router = APIRouter(route_class=DishkaRoute)


@university_router.post("/institutes", response_model=InstituteResponseSchema)
async def create_institute(
    request: Request,
    create_schema: InstituteCreateSchema,
    use_case: FromDishka[CreateInstituteUseCase],
):
    return await use_case(request, create_schema)


@university_router.post("/departments", response_model=DepartmentResponseSchema)
async def create_department(
    request: Request,
    create_schema: DepartmentCreateSchema,
    use_case: FromDishka[CreateDepartmentUseCase],
):
    return await use_case(request, create_schema)


@university_router.post("/groups", response_model=GroupResponseSchema)
async def create_group(
    request: Request,
    create_schema: GroupCreateSchema,
    use_case: FromDishka[CreateGroupUseCase],
):
    return await use_case(request, create_schema)


# — получение со строковыми фильтрами —
@university_router.get("/institutes", response_model=list[InstituteResponseSchema])
async def list_institutes(
    request: Request,
    use_case: FromDishka[ListInstitutesUseCase],
    limit: int = Query(lte=100, gte=5, default=5),
    skip: int = 0,
    filters: InstituteFilter = FilterDepends(InstituteFilter),
):
    return await use_case(request, limit, skip, filters)


@university_router.get("/departments", response_model=list[DepartmentResponseSchema])
async def list_departments(
    request: Request,
    use_case: FromDishka[ListDepartmentsUseCase],
    limit: int = Query(lte=100, gte=5, default=5),
    skip: int = 0,
    filters: DepartmentFilter = FilterDepends(DepartmentFilter),
):
    return await use_case(request, limit, skip, filters)


@university_router.get("/groups", response_model=list[GroupResponseSchema])
async def list_groups(
    request: Request,
    use_case: FromDishka[ListGroupsUseCase],
    limit: int = Query(lte=100, gte=5, default=5),
    skip: int = 0,
    filters: GroupFilter = FilterDepends(GroupFilter),
):
    return await use_case(request, limit, skip, filters)


# — обновление (PATCH) —
@university_router.patch(
    "/institutes/{institute_id}", response_model=InstituteResponseSchema
)
async def update_institute(
    request: Request,
    institute_id: int,
    update_schema: InstituteUpdateSchema,
    use_case: FromDishka[UpdateInstituteUseCase],
):
    return await use_case(request, institute_id, update_schema)


@university_router.patch(
    "/departments/{department_id}", response_model=DepartmentResponseSchema
)
async def update_department(
    request: Request,
    department_id: int,
    update_schema: DepartmentUpdateSchema,
    use_case: FromDishka[UpdateDepartmentUseCase],
):
    return await use_case(request, department_id, update_schema)


@university_router.patch("/groups/{group_id}", response_model=GroupResponseSchema)
async def update_group(
    request: Request,
    group_id: int,
    update_schema: GroupUpdateSchema,
    use_case: FromDishka[UpdateGroupUseCase],
):
    return await use_case(request, group_id, update_schema)


# — удаление —
@university_router.delete("/institutes/{institute_id}", status_code=204)
async def delete_institute(
    request: Request,
    institute_id: int,
    use_case: FromDishka[DeleteInstituteUseCase],
):
    await use_case(request, institute_id)


@university_router.delete("/departments/{department_id}", status_code=204)
async def delete_department(
    request: Request,
    department_id: int,
    use_case: FromDishka[DeleteDepartmentUseCase],
):
    await use_case(request, department_id)


@university_router.delete("/groups/{group_id}", status_code=204)
async def delete_group(
    request: Request,
    group_id: int,
    use_case: FromDishka[DeleteGroupUseCase],
):
    await use_case(request, group_id)
