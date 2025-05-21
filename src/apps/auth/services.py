import hashlib
import logging
import uuid
from datetime import timedelta, timezone, datetime
from typing import List, Any, Union
from uuid import UUID

import jwt
from fastapi import Request
from fastapi_mail import MessageSchema, MessageType, FastMail
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.auth.models import RefreshTokenModel
from src.apps.auth.repositories import RefreshTokenRepository, InviteRedisRepository
from src.apps.auth.schemas import AccessTokenPayloadSchema, RefreshTokenPayloadSchema, InviteSchema, \
    TeacherInviteSchema, StudentInviteSchema
from src.apps.university.department.services import DepartmentService
from src.apps.university.group.services import GroupService
from src.apps.user.enums import UserRole
from src.apps.user.repositories import UserRepository
from src.apps.user.services import TeacherService, StudentService
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


class InviteService:
    INVITE_TTL = timedelta(days=7)

    def __init__(self,
                 invite_repository: InviteRedisRepository,
                 user_repository: UserRepository,
                 department_service: DepartmentService,
                 group_service: GroupService,
                 settings: Settings):
        self.invite_repository = invite_repository
        self.user_repository = user_repository
        self.department_service = department_service
        self.group_service = group_service
        self.fm = FastMail(settings.email)

    async def _create_invite(
            self,
            request: Request,
            invite_body: Union[StudentInviteSchema, TeacherInviteSchema]
    ) -> UUID:
        try:
            if await self.user_repository.get_by(session=request.state.session, email=invite_body.email):
                raise ValueError("Пользователь уже зарегистрирован")
        except:
            pass

        invite_id = uuid.uuid4()
        value = None

        if invite_body.role == UserRole.STUDENT:
            value = (await self.group_service.get(request, invite_body.group_id)).model_dump()
        elif invite_body.role == UserRole.TEACHER:
            value = (await self.department_service.get(request, invite_body.department_id)).model_dump()

        value["role"] = invite_body.role
        value["email"] = invite_body.email

        is_set = await self.invite_repository.set(
            key=str(invite_id),
            value=value,
            ttl=self.INVITE_TTL
        )
        if not is_set:
            raise RuntimeError(f"Не удалось сохранить приглашение с id={invite_id}")

        return invite_id

    async def _make_invite_link(self, register_url, invite_id) -> str:
        return f"{register_url}{invite_id}"

    async def _send_email_invite(self, invite_schema: InviteSchema, invite_id: UUID) -> None:
        invite_link = self._make_invite_link(invite_schema.register_url, invite_id)
        message = MessageSchema(
            subject="Приглашение на платформу",
            recipients=[invite_schema.invite_body.email],
            body=f"<p>Перейдите по <a href='{invite_link}'>ссылке</a> {invite_link}, чтобы зарегистрироваться. Ссылка активна в течение 7 дней.</p>",
            subtype=MessageType.html
        )
        print("message", message)
        return await self.fm.send_message(message)

    async def invite(
            self,
            request: Request,
            invite_schema: InviteSchema
    ) -> str | None:
        invite_id = await self._create_invite(request, invite_schema.invite_body)

        # if invite_schema.invite_body.role == UserRole.STUDENT:
        return await self._make_invite_link(invite_schema.register_url, invite_id)

        # await self._send_email_invite(invite_schema, invite_id)

    async def get_invite_info(self, invite_id: str) -> dict | None:
        return await self.invite_repository.get(invite_id)
