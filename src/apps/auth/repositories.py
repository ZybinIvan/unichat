from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import RefreshTokenModel
from src.core.repositories import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshTokenModel]):
    model = RefreshTokenModel

    async def create(self, refresh_token: str, session: AsyncSession) -> RefreshTokenModel:
        """Добавить новый объект в базу"""
        obj = RefreshTokenModel(refresh_token=refresh_token)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj