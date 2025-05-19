from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from src.apps.user.repositories import UserRepository, TeacherRepository, StudentRepository, UniversityAdminRepository
from src.apps.user.services import UserService, StudentService, TeacherService
from src.apps.user.use_cases import GetUserUseCase

user_provider = Provider(scope=Scope.REQUEST)

user_provider.provide(UserRepository)
user_provider.provide(TeacherRepository)
user_provider.provide(StudentRepository)
user_provider.provide(UniversityAdminRepository)

user_provider.provide(UserService)
user_provider.provide(TeacherService)
user_provider.provide(StudentService)

user_provider.provide(GetUserUseCase)
