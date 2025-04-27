from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import RefreshTokenModel
from src.apps.auth.repositories import RefreshTokenRepository


class RefreshTokenService:
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    async def get(self, id: int, session: AsyncSession) -> RefreshTokenModel:
        return await self.repository.get(id, session)

    async def list(self, limit: int, skip: int, session: AsyncSession) -> List[RefreshTokenModel]:
        return await self.repository.list(limit, skip, session)

    async def create(self, refresh_token: str, session: AsyncSession) -> RefreshTokenModel:
        return await self.repository.create(refresh_token,session)