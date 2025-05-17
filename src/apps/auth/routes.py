from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Request, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from dishka.integrations.fastapi import DishkaRoute

from src.apps.auth.schemas import TokenSchema, LoginSchema, InviteSchema
from src.apps.university.schemas import (
    RegisterUniversitySchema,
    RegisterTeacherSchema,
    RegisterStudentSchema,
    UniversityResponseSchema,
)

from src.apps.user.schemas import (
    TeacherResponseSchema,
    StudentResponseSchema,
)
from src.apps.auth.use_cases import (
    AuthUseCase,
    RotationTokenUseCase,
    StudentRegisterUseCase,
    TeacherRegisterUseCase,
    UniversityRegisterUseCase, InviteUseCase, InviteInfoUseCase,
)

auth_routes = APIRouter(route_class=DishkaRoute)


@auth_routes.post("/login", response_model=TokenSchema)
async def login(
        request: Request,
        authenticate_use_case: FromDishka[AuthUseCase],
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
):
    user_credentials = LoginSchema(
        email=form_data.username,
        password=form_data.password,
    )
    return await authenticate_use_case(request, user_credentials)


@auth_routes.post("/refresh", response_model=TokenSchema)
async def rotate_token(
        request: Request,
        refresh_token: str,
        use_case: FromDishka[RotationTokenUseCase],
):
    return await use_case(request, refresh_token)


@auth_routes.post("/register_university", response_model=UniversityResponseSchema, status_code=201)
async def register_university(
        request: Request,
        register_university_schema: RegisterUniversitySchema,
        use_case: FromDishka[UniversityRegisterUseCase],
):
    return await use_case(request, register_university_schema)


@auth_routes.post("/register_teacher", response_model=TeacherResponseSchema, status_code=201)
async def register_teacher(
        request: Request,
        register_teacher_schema: RegisterTeacherSchema,
        use_case: FromDishka[TeacherRegisterUseCase],
        invite_id: str = Query(...),
):
    return await use_case(request, register_teacher_schema, invite_id)


@auth_routes.post("/register_student", response_model=StudentResponseSchema, status_code=201)
async def register_student(
        request: Request,
        register_student_schema: RegisterStudentSchema,
        use_case: FromDishka[StudentRegisterUseCase],
        invite_id: str = Query(...),
):
    return await use_case(request, register_student_schema, invite_id)


@auth_routes.post("/invite", response_model=str | None, status_code=201)
async def invite(
        request: Request,
        invite_schema: InviteSchema,
        use_case: FromDishka[InviteUseCase],
):
    return await use_case(request, invite_schema)


@auth_routes.get("/invite_info/{invite_id}", response_model=dict | None, status_code=200)
async def invite_info(
        invite_id: str,
        use_case: FromDishka[InviteInfoUseCase],
):
    return await use_case(invite_id)
