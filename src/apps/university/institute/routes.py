from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Query
from fastapi_filter import FilterDepends
from starlette.requests import Request

from src.apps.university.institute.schemas import InstituteCreateSchema, InstituteResponseSchema, InstituteFilter, \
    InstituteUpdateSchema, InstituteListResponseSchema
from src.apps.university.institute.use_cases import CreateInstituteUseCase, RetrieveInstituteUseCase, \
    ListInstitutesUseCase, UpdateInstituteUseCase, DeleteInstituteUseCase
from src.middleware import AuthMiddlewareDepends

institute_router = APIRouter(route_class=DishkaRoute, tags=["Institute"])


@institute_router.post("/institutes", response_model=int, dependencies=[AuthMiddlewareDepends])
async def create_institute(
        request: Request,
        create_schema: InstituteCreateSchema,
        use_case: FromDishka[CreateInstituteUseCase],
):
    return await use_case(request, create_schema)


@institute_router.get(
    "/institutes/{institute_id}", status_code=204
)
async def get_institute(
        request: Request,
        institute_id: int,
        use_case: FromDishka[RetrieveInstituteUseCase],
):
    return await use_case(request, institute_id)


@institute_router.get("/institutes", response_model=InstituteListResponseSchema, dependencies=[AuthMiddlewareDepends])
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
