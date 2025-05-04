from typing import Annotated

from fastapi.params import Depends

from src.apps.user.repositories import UserRepository, TeacherRepository, StudentRepository
from src.apps.user.services import UserService, TeacherService, StudentService


# ------- РЕПОЗИТОРИИ --------

async def get_user_repository() -> UserRepository:
    return UserRepository()


UserRepositoryDepends = Annotated[UserRepository, Depends(get_user_repository)]


async def get_teacher_repository() -> TeacherRepository:
    return TeacherRepository()


TeacherRepositoryDepends = Annotated[TeacherRepository, Depends(get_teacher_repository)]


async def get_student_repository() -> StudentRepository:
    return StudentRepository()


StudentRepositoryDepends = Annotated[StudentRepository, Depends(get_student_repository)]


# -------- СЕРВИСЫ --------


async def get_user_service(repository: UserRepositoryDepends) -> UserService:
    return UserService(repository)


UserServiceDepends = Annotated[UserService, Depends(get_user_service)]


async def get_teacher_service(repository: TeacherRepositoryDepends) -> TeacherService:
    return TeacherService(repository)


TeacherServiceDepends = Annotated[TeacherService, Depends(get_teacher_service)]


async def get_student_service(repository: StudentRepositoryDepends) -> StudentService:
    return StudentService(repository)


StudentServiceDepends = Annotated[StudentService, Depends(get_student_service)]
