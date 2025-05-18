import logging
import uuid

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from fastapi import Request, HTTPException, status

from src.apps.auth.models import RefreshTokenModel
from src.apps.auth.schemas import (
    TokenSchema,
    LoginSchema,
    AccessTokenPayloadSchema,
    RefreshTokenPayloadSchema, InviteSchema,
)
from src.apps.auth.services import JWTService, RefreshTokenService, InviteService
from src.apps.university.models import UniversityModel
from src.apps.university.schemas import (
    UniversityResponseSchema,
    RegisterUniversitySchema,
    RegisterTeacherSchema,
    RegisterStudentSchema,
)
from src.apps.university.services import UniversityService
from src.apps.user.enums import UserRole
from src.apps.user.models import UserModel, TeacherModel, StudentModel
from src.apps.user.schemas import TeacherResponseSchema, StudentResponseSchema
from src.apps.user.services import UserService, TeacherService, StudentService

logger = logging.getLogger(__name__)


class AuthUseCase:
    def __init__(self, jwt_service: JWTService, user_service: UserService):
        self.jwt_service = jwt_service
        self.user_service = user_service

    async def __call__(
            self, request: Request, login_schema: LoginSchema
    ) -> TokenSchema:
        try:
            user: UserModel = await self.user_service.get_by_field(
                request, email=login_schema.email
            )

            if not pbkdf2_sha256.verify(login_schema.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный email или пароль",
                )

            fingerprint = JWTService.get_client_fingerprint(request)
            jti = str(uuid.uuid4())

            # Собираем payload для access и refresh
            access_payload = AccessTokenPayloadSchema.model_validate(user)
            refresh_payload = RefreshTokenPayloadSchema(
                user_id=user.id, jti=jti, fingerprint=fingerprint
            )

            access_token = self.jwt_service.create_access_token(access_payload)
            refresh_token = await self.jwt_service.create_refresh_token(
                payload=refresh_payload, session=request.state.session
            )

            return TokenSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
            )

        except Exception as e:
            logger.exception(e)
            raise e


class RotationTokenUseCase:
    def __init__(
            self,
            refresh_token_service: RefreshTokenService,
            user_service: UserService,
            jwt_service: JWTService,
    ):
        self.refresh_token_service = refresh_token_service
        self.user_service = user_service
        self.jwt_service = jwt_service

    async def __call__(self, request: Request, refresh_token: str) -> TokenSchema:
        try:
            refresh_token_from_db: RefreshTokenModel | None = (
                await self.refresh_token_service.get_by_field(
                    request, refresh_token=refresh_token
                )
            )
            if not refresh_token_from_db:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Refresh token not found",
                )

            token_payload: dict = self.jwt_service.decode(refresh_token)
            user: UserModel = await self.user_service.get_by_field(
                request, id=token_payload["user_id"]
            )

            fingerprint = JWTService.get_client_fingerprint(request)
            jti = str(uuid.uuid4())

            access_payload = AccessTokenPayloadSchema.model_validate(user)
            refresh_payload = RefreshTokenPayloadSchema(
                user_id=user.id, jti=jti, fingerprint=fingerprint
            )

            access_token = self.jwt_service.create_access_token(access_payload)
            refresh_token = await self.jwt_service.create_refresh_token(
                payload=refresh_payload, session=request.state.session
            )

            await self.refresh_token_service.delete(request, refresh_token_from_db.id)

            print("request.state.user.university_id", request.state.user.university_id)

            return TokenSchema(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="Bearer",
            )
        except Exception as e:
            logger.exception(e)
            raise e


class UniversityRegisterUseCase:
    def __init__(self, university_service: UniversityService):
        self.university_service = university_service

    async def __call__(
            self, request: Request, register_schema: RegisterUniversitySchema
    ) -> UniversityResponseSchema:
        created_university: UniversityModel = await self.university_service.create(
            request, register_schema
        )
        return UniversityResponseSchema.model_validate(
            created_university, from_attributes=True
        )


class TeacherRegisterUseCase:
    def __init__(self, teacher_service: TeacherService, invite_service: InviteService):
        self.teacher_service = teacher_service
        self.invite_service = invite_service

    async def __call__(
            self, request: Request, register_schema: RegisterTeacherSchema, invite_id: str
    ) -> TeacherResponseSchema:
        invite_info = await self.invite_service.get_invite_info(invite_id)

        if not invite_info or invite_info.get("role", None) != UserRole.TEACHER:
            raise HTTPException(status_code=400, detail="Неверный invite_id")

        setattr(register_schema, "department_id", invite_info.get("department_id"))

        created_teacher: TeacherModel = await self.teacher_service.create(
            request, register_schema
        )
        return TeacherResponseSchema.model_validate(
            created_teacher, from_attributes=True
        )


class StudentRegisterUseCase:
    def __init__(self, student_service: StudentService, invite_service: InviteService):
        self.student_service = student_service
        self.invite_service = invite_service

    async def __call__(
            self, request: Request, register_schema: RegisterStudentSchema, invite_id: str
    ) -> StudentResponseSchema:
        invite_info = await self.invite_service.get_invite_info(invite_id)

        if not invite_info or invite_info.get("role", None) != UserRole.STUDENT:
            raise HTTPException(status_code=400, detail="Неверный invite_id")

        setattr(register_schema, "group_id", invite_info.get("group_id"))

        created_student: StudentModel = await self.student_service.create(
            request, register_schema
        )
        return StudentResponseSchema.model_validate(
            created_student, from_attributes=True
        )


class InviteUseCase:
    def __init__(self, invite_service: InviteService):
        self.invite_service = invite_service

    async def __call__(self, request: Request, invite_schema: InviteSchema) -> str | None:
        return await self.invite_service.invite(request, invite_schema)


class InviteInfoUseCase:
    def __init__(self, invite_service: InviteService):
        self.invite_service = invite_service

    async def __call__(self, invite_id: str):
        return await self.invite_service.get_invite_info(invite_id)
