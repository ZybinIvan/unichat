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
    RetrieveDepartmentUseCase,
    RetrieveGroupUseCase,
    RetrieveInstituteUseCase,
    UpdateDepartmentUseCase,
    UpdateGroupUseCase,
    UpdateInstituteUseCase,
)


university_router = APIRouter(route_class=DishkaRoute)

institute_router = APIRouter(route_class=DishkaRoute, tags=["Institute"])


@institute_router.post("/institutes", response_model=InstituteResponseSchema)
async def create_institute(
    request: Request,
    create_schema: InstituteCreateSchema,
    use_case: FromDishka[CreateInstituteUseCase],
):
    return await use_case(request, create_schema)


@institute_router.get(
    "/institutes/{institute_id}", response_model=InstituteResponseSchema
)
async def get_institute(
    request: Request,
    institute_id: int,
    use_case: FromDishka[RetrieveInstituteUseCase],
):
    return await use_case(request, institute_id)


@institute_router.get("/institutes", response_model=list[InstituteResponseSchema])
async def list_institutes(
    request: Request,
    use_case: FromDishka[ListInstitutesUseCase],
    limit: int = Query(lte=100, gte=5, default=5),
    skip: int = 0,
    filters: InstituteFilter = FilterDepends(InstituteFilter),
):
    return await use_case(request, limit, skip, filters)


@institute_router.patch(
    "/institutes/{institute_id}", response_model=InstituteResponseSchema
)
async def update_institute(
    request: Request,
    institute_id: int,
    update_schema: InstituteUpdateSchema,
    use_case: FromDishka[UpdateInstituteUseCase],
):
    return await use_case(request, institute_id, update_schema)


@institute_router.delete("/institutes/{institute_id}", status_code=204)
async def delete_institute(
    request: Request,
    institute_id: int,
    use_case: FromDishka[DeleteInstituteUseCase],
):
    await use_case(request, institute_id)


university_router.include_router(institute_router)

department_router = APIRouter(route_class=DishkaRoute, tags=["Department"])


@department_router.post("/departments", response_model=DepartmentResponseSchema)
async def create_department(
    request: Request,
    create_schema: DepartmentCreateSchema,
    use_case: FromDishka[CreateDepartmentUseCase],
):
    return await use_case(request, create_schema)


@department_router.get(
    "/departments/{department_id}", response_model=DepartmentResponseSchema
)
async def get_department(
    request: Request,
    department_id: int,
    use_case: FromDishka[RetrieveDepartmentUseCase],
):
    return await use_case(request, department_id)


@department_router.get("/departments", response_model=list[DepartmentResponseSchema])
async def list_departments(
    request: Request,
    use_case: FromDishka[ListDepartmentsUseCase],
    limit: int = Query(lte=100, gte=5, default=5),
    skip: int = 0,
    filters: DepartmentFilter = FilterDepends(DepartmentFilter),
):
    return await use_case(request, limit, skip, filters)


@department_router.patch(
    "/departments/{department_id}", response_model=DepartmentResponseSchema
)
async def update_department(
    request: Request,
    department_id: int,
    update_schema: DepartmentUpdateSchema,
    use_case: FromDishka[UpdateDepartmentUseCase],
):
    return await use_case(request, department_id, update_schema)


@department_router.delete("/departments/{department_id}", status_code=204)
async def delete_department(
    request: Request,
    department_id: int,
    use_case: FromDishka[DeleteDepartmentUseCase],
):
    await use_case(request, department_id)


university_router.include_router(department_router)

group_router = APIRouter(route_class=DishkaRoute, tags=["Group"])


@group_router.post("/groups", response_model=GroupResponseSchema)
async def create_group(
    request: Request,
    create_schema: GroupCreateSchema,
    use_case: FromDishka[CreateGroupUseCase],
):
    return await use_case(request, create_schema)


@group_router.get("/groups/{group_id}", response_model=GroupResponseSchema)
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


university_router.include_router(group_router)
