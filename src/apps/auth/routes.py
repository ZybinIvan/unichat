from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.auth.depends import RefreshTokenServiceDepends
from src.apps.auth.schemas import TokenSchema, LoginSchema
from src.core.depends import SessionDepends

auth_routes = APIRouter()


# @auth_routes.post('/login', response_model=TokenSchema)
# async def login(request: Request, authenticate_use_case: AuthenticationUseCase,
#                 form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
#     try:
#         user_credentials: LoginSchema = LoginSchema(phone=form_data.username, password=form_data.password)
#         return await authenticate_use_case(request, user_credentials)
#     except Exception as e:
#         print(e)
#         raise e

@auth_routes.post('/refresh')
async def create_refresh(request: Request, refresh: str, service: RefreshTokenServiceDepends,
                         session: SessionDepends) -> str:
    return (await service.create(refresh, session)).refresh_token
