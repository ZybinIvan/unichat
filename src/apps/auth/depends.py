from typing import Annotated

from fastapi import Depends

from src.apps.auth.repositories import RefreshTokenRepository
from src.apps.auth.services import RefreshTokenService, JWTService
from src.apps.auth.use_cases import AuthUseCase, RotationTokenUseCase
from src.apps.user.depends import UserServiceDepends
from src.config import SettingsDepends


def get_refresh_token_repository() -> RefreshTokenRepository:
    return RefreshTokenRepository()


RefreshTokenRepositoryDepends = Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)]


def get_refresh_token_service(repository: RefreshTokenRepositoryDepends) -> RefreshTokenService:
    return RefreshTokenService(repository)


RefreshTokenServiceDepends = Annotated[RefreshTokenService, Depends(get_refresh_token_service)]


def get_jwt_service(refresh_token_service: RefreshTokenServiceDepends,
                    settings: SettingsDepends) -> JWTService:
    return JWTService(refresh_token_service, settings)


JWTServiceDepends = Annotated[JWTService, Depends(get_jwt_service)]


def get_auth_use_case(jwt_service: JWTServiceDepends, user_service: UserServiceDepends) -> AuthUseCase:
    return AuthUseCase(jwt_service, user_service)


AuthUseCaseDepends = Annotated[AuthUseCase, Depends(get_auth_use_case)]


def get_rotate_token_use_case(refresh_token_service: RefreshTokenServiceDepends, user_service: UserServiceDepends,
                              jwt_service: JWTServiceDepends) -> RotationTokenUseCase:
    return RotationTokenUseCase(refresh_token_service, user_service, jwt_service)


RotateTokenUseCaseDepends = Annotated[RotationTokenUseCase, Depends(get_rotate_token_use_case)]
