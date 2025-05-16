from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.core.depends import core_provider
from src.apps.university.depends import university_provider
from src.apps.user.repositories import UserRepository, TeacherRepository, StudentRepository, UniversityAdminRepository
from src.apps.user.services import UserService, TeacherService, StudentService
from src.apps.auth.repositories import RefreshTokenRepository, InviteRedisRepository
from src.apps.auth.services import RefreshTokenService, JWTService, InviteService
from src.apps.auth.use_cases import (
    AuthUseCase,
    RotationTokenUseCase,
    UniversityRegisterUseCase,
    TeacherRegisterUseCase,
    StudentRegisterUseCase, InviteUseCase, InviteInfoUseCase,
)

# Провайдер для модуля "auth"
auth_provider = Provider(scope=Scope.REQUEST)

# Регистрация зависимостей модуля User
auth_provider.provide(UserRepository)
auth_provider.provide(UserService)
auth_provider.provide(TeacherRepository)
auth_provider.provide(TeacherService)
auth_provider.provide(StudentRepository)
auth_provider.provide(StudentService)
# auth_provider.provide(UniversityAdminRepository)

# Регистрация репозиториев и сервисов модуля Auth
auth_provider.provide(RefreshTokenRepository)
auth_provider.provide(RefreshTokenService)
auth_provider.provide(InviteRedisRepository)
auth_provider.provide(InviteService)
auth_provider.provide(JWTService)

# Регистрация use-case'ов аутентификации и регистрации пользователей
auth_provider.provide(AuthUseCase)
auth_provider.provide(RotationTokenUseCase)
auth_provider.provide(UniversityRegisterUseCase)
auth_provider.provide(TeacherRegisterUseCase)
auth_provider.provide(StudentRegisterUseCase)
auth_provider.provide(InviteUseCase)
auth_provider.provide(InviteInfoUseCase)

# Сборка контейнера Dishka (core + university + auth)
container = make_async_container(
    core_provider,
    university_provider,
    auth_provider,
    FastapiProvider(),
)

__all__ = ["container"]
