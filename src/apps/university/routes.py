from fastapi import APIRouter
from starlette.requests import Request

from src.apps.university.depends import CreateInstituteUseCaseDepends, CreateDepartmentUseCaseDepends, \
    CreateGroupUseCaseDepends
from src.apps.university.schemas import InstituteResponseSchema, InstituteCreateSchema, DepartmentCreateSchema, \
    DepartmentResponseSchema, GroupResponseSchema, GroupCreateSchema

university_router = APIRouter()


@university_router.post("/institutes", response_model=InstituteResponseSchema)
async def create_institute(request: Request, create_schema: InstituteCreateSchema,
                           use_case: CreateInstituteUseCaseDepends):
    return await use_case(request, create_schema)


@university_router.post("/departments", response_model=DepartmentResponseSchema)
async def create_department(request: Request, create_schema: DepartmentCreateSchema,
                            use_case: CreateDepartmentUseCaseDepends):
    return await use_case(request, create_schema)


@university_router.post("/groups", response_model=GroupResponseSchema)
async def create_group(request: Request, create_schema: GroupCreateSchema, use_case: CreateGroupUseCaseDepends):
    return await use_case(request, create_schema)
