from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query
from fastapi_filter import FilterDepends
from starlette.requests import Request

from src.apps.university.department.use_cases import CreateDepartmentUseCase, RetrieveDepartmentUseCase, \
    ListDepartmentsUseCase, UpdateDepartmentUseCase, DeleteDepartmentUseCase
from src.apps.university.schemas import DepartmentCreateSchema, DepartmentDetailSchema, DepartmentResponseSchema, \
    DepartmentFilter, DepartmentUpdateSchema

department_router = APIRouter(route_class=DishkaRoute, tags=["Department"])


@department_router.post("/departments", response_model=int)
async def create_department(
        request: Request,
        create_schema: DepartmentCreateSchema,
        use_case: FromDishka[CreateDepartmentUseCase],
):
    return await use_case(request, create_schema)


@department_router.get(
    "/departments/{department_id}", response_model=DepartmentDetailSchema
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
