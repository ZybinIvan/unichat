from typing import Union

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request

from src.apps.user.schemas import UserDetailResponseSchema, TeacherDetailResponseSchema, StudentDetailResponseSchema
from src.apps.user.use_cases import GetUserUseCase
from src.middleware import AuthMiddlewareDepends

user_routes = APIRouter(route_class=DishkaRoute)


@user_routes.get("", response_model=Union[
    TeacherDetailResponseSchema, StudentDetailResponseSchema, UserDetailResponseSchema],
                 dependencies=[AuthMiddlewareDepends])
async def get(request: Request, use_case: FromDishka[GetUserUseCase]):
    return await use_case(request)
