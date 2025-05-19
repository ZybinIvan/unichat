from typing import Union

from starlette.requests import Request

from src.apps.user.schemas import UserDetailResponseSchema, TeacherDetailResponseSchema, StudentDetailResponseSchema
from src.apps.user.services import UserService


class GetUserUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def __call__(self, request: Request) -> Union[
        TeacherDetailResponseSchema, StudentDetailResponseSchema, UserDetailResponseSchema]:
        user = await self.user_service.get_by_field(request, id=request.user.id)
        return user
        # if user.role == UserRole.STUDENT:
        #     return StudentDetailResponseSchema(
        #         first_name=user.first_name,
        #         last_name=user.last_name,
        #         patronymic=user.patronymic,
        #         email=user.email,
        #         institute_name=user.group.department.
        #     )
