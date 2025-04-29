import logging
import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from src.apps.auth.models import RefreshTokenModel
from src.apps.auth.schemas import TokenSchema, LoginSchema, AccessTokenPayloadSchema, RefreshTokenPayloadSchema
from src.apps.auth.services import JWTService, RefreshTokenService
from src.apps.user.models import UserModel
from src.apps.user.services import UserService

from fastapi import Request, HTTPException, status

logger = logging.getLogger(__name__)


class AuthUseCase:
    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def __call__(self, request: Request, login_schema: LoginSchema) -> TokenSchema:
        try:
            user: UserModel = await self.user_service.get_by_field(request, email=login_schema.email)

            if not pbkdf2_sha256.verify(login_schema.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль"
                )

            fingerprint = JWTService.get_client_fingerprint(request)
            jti = str(uuid.uuid4())

            # Собираем payload для access и refresh
            access_payload = AccessTokenPayloadSchema(user_id=user.id)
            refresh_payload = RefreshTokenPayloadSchema(
                user_id=user.id,
                jti=jti,
                fingerprint=fingerprint
            )

            access_token = self.jwt_service.create_access_token(access_payload)
            refresh_token = await self.jwt_service.create_refresh_token(
                payload=refresh_payload,
                session=request.state.session
            )

            return TokenSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer"
            )

        except Exception as e:
            logger.exception(e)
            raise e


class RotationTokenUseCase:
    def __init__(self, refresh_token_service: RefreshTokenService, user_service: UserService, jwt_service: JWTService):
        self.refresh_token_service = refresh_token_service
        self.user_service = user_service
        self.jwt_service = jwt_service

    async def __call__(self, request: Request, refresh_token: str) -> TokenSchema:
        try:
            refresh_token_from_db: RefreshTokenModel | None = await self.refresh_token_service.get_by_field(
                request, refresh_token=refresh_token)
            if not refresh_token_from_db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token not found",

                )

            token_payload: dict = self.jwt_service.decode(refresh_token)
            user: UserModel = await self.user_service.get_by_field(request, id=token_payload['user_id'])

            fingerprint = JWTService.get_client_fingerprint(request)
            jti = str(uuid.uuid4())

            access_payload = AccessTokenPayloadSchema(user_id=user.id)
            refresh_payload = RefreshTokenPayloadSchema(
                user_id=user.id,
                jti=jti,
                fingerprint=fingerprint
            )

            access_token = self.jwt_service.create_access_token(access_payload)
            refresh_token = await self.jwt_service.create_refresh_token(
                payload=refresh_payload,
                session=request.state.session
            )

            await self.refresh_token_service.delete(request, refresh_token_from_db.id)

            return TokenSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer"
            )
        except Exception as e:
            logger.exception(e)
            raise e
