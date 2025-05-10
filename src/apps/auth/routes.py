from typing import Annotated
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dishka.integrations.fastapi import DishkaRoute

from src.apps.auth.schemas import TokenSchema, LoginSchema
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
    UniversityRegisterUseCase,
)

auth_routes = APIRouter(route_class=DishkaRoute)


@auth_routes.post("/login", response_model=TokenSchema)
async def login(
    request: Request,
    authenticate_use_case: Annotated[AuthUseCase, FromDishka()],
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
    use_case: Annotated[RotationTokenUseCase, FromDishka()],
):
    return await use_case(request, refresh_token)


@auth_routes.post("/register_university", response_model=UniversityResponseSchema)
async def register_university(
    request: Request,
    register_university_schema: RegisterUniversitySchema,
    use_case: Annotated[UniversityRegisterUseCase, FromDishka()],
):
    return await use_case(request, register_university_schema)


@auth_routes.post("/register_teacher", response_model=TeacherResponseSchema)
async def register_teacher(
    request: Request,
    register_teacher_schema: RegisterTeacherSchema,
    use_case: Annotated[TeacherRegisterUseCase, FromDishka()],
):
    return await use_case(request, register_teacher_schema)


@auth_routes.post("/register_student", response_model=StudentResponseSchema)
async def register_student(
    request: Request,
    register_student_schema: RegisterStudentSchema,
    use_case: Annotated[StudentRegisterUseCase, FromDishka()],
):
    return await use_case(request, register_student_schema)
