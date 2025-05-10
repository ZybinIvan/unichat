import hashlib
import logging
from datetime import timedelta, timezone, datetime
from typing import List, Any

import jwt
from fastapi import Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import RefreshTokenModel
from src.apps.auth.repositories import RefreshTokenRepository
from src.apps.auth.schemas import AccessTokenPayloadSchema, RefreshTokenPayloadSchema
from src.config import Settings

logger = logging.getLogger(__name__)


class RefreshTokenService:  #
    def __init__(self, repository: RefreshTokenRepository):
        self.repository = repository

    async def get(self, id: int, session: AsyncSession) -> RefreshTokenModel:
        return await self.repository.get_or_none(id, session)

    async def list(
        self, limit: int, skip: int, session: AsyncSession
    ) -> List[RefreshTokenModel]:
        return await self.repository.list(limit, skip, session)

    async def create(
        self, refresh_token: str, session: AsyncSession
    ) -> RefreshTokenModel:
        return await self.repository.create(refresh_token, session)

    async def get_by_field(self, request: Request, **lookup: Any) -> RefreshTokenModel:
        """
        Получить пользователя по любому полю, например:
        await user_service.get_by_field(request, email="user@example.com")
        """
        try:
            user = await self.repository.get_by(session=request.state.session, **lookup)
            return user
        except Exception as e:
            logger.exception(e)
            raise e

    async def delete(self, request: Request, id: int) -> bool:
        return await self.repository.delete(id, request.state.session)


class JWTService:
    def __init__(
        self, refresh_token_repository: RefreshTokenService, settings: Settings
    ):
        self.refresh_token_repository = refresh_token_repository
        self.config = settings.jwt

    def _create_token(self, payload: BaseModel, expire_time) -> str:
        payload_dict = payload.model_dump()
        payload_dict.update({"exp": expire_time})
        encoded_jwt = jwt.encode(
            payload=payload_dict,
            key=self.config.secret_key,
            algorithm=self.config.algorithms[0],
        )
        return encoded_jwt

    @staticmethod
    def get_client_fingerprint(request: Request) -> str:
        user_agent = request.headers.get("User-Agent")
        # TODO: расширить fingerprint
        return str(hashlib.sha256(user_agent.encode()).hexdigest())

    def create_access_token(self, payload: AccessTokenPayloadSchema) -> str:
        new_expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=self.config.access_token_expiration_minutes
        )
        return self._create_token(payload, new_expiration_time)

    async def create_refresh_token(
        self, payload: RefreshTokenPayloadSchema, session: AsyncSession
    ) -> str:
        new_expiration_time = datetime.now(timezone.utc) + timedelta(
            days=self.config.refresh_token_expiration_days
        )
        refresh_token = self._create_token(payload, new_expiration_time)

        await self.refresh_token_repository.create(refresh_token, session)
        return refresh_token

    def encode(self, payload: dict) -> str:
        return jwt.encode(
            payload=payload,
            key=self.config.secret_key,
            algorithm=self.config.algorithms[0],
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(
            jwt=token, key=self.config.secret_key, algorithms=self.config.algorithms
        )
