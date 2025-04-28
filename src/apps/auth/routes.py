from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.auth.depends import RefreshTokenServiceDepends, AuthUseCaseDepends
from src.apps.auth.schemas import TokenSchema, LoginSchema
from src.apps.user.depends import UserServiceDepends
from src.apps.user.schemas import UserRegisterSchema, UserResponseSchema
from src.core.depends import SessionDepends

auth_routes = APIRouter()


@auth_routes.post("/register")
async def register_user(request: Request, register_schema: UserRegisterSchema,
                 service: UserServiceDepends) -> UserResponseSchema:
    return await service.create(request, register_schema)


@auth_routes.post('/login', response_model=TokenSchema)
async def login(request: Request, authenticate_use_case: AuthUseCaseDepends,
                form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    try:
        user_credentials: LoginSchema = LoginSchema(email=form_data.username, password=form_data.password)
        return await authenticate_use_case(request, user_credentials)
    except Exception as e:
        print(e)
        raise e


