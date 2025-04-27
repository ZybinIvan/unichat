from typing import Annotated

from fastapi import Depends

from src.apps.auth.repositories import RefreshTokenRepository
from src.apps.auth.services import RefreshTokenService


def get_refresh_token_repository() -> RefreshTokenRepository:
    return RefreshTokenRepository()


RefreshTokenRepositoryDepends = Annotated[RefreshTokenRepository, Depends(get_refresh_token_repository)]


def get_refresh_token_service(repository: RefreshTokenRepositoryDepends) -> RefreshTokenService:
    return RefreshTokenService(repository)


RefreshTokenServiceDepends = Annotated[RefreshTokenService, Depends(get_refresh_token_service)]
