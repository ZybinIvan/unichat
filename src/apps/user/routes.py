from fastapi import APIRouter, Request

from src.apps.user.depends import UserServiceDepends
from src.apps.user.schemas import UserRegisterSchema, UserResponseSchema

user_routes = APIRouter()


@user_routes.post("/register")
async def create(request: Request, register_schema: UserRegisterSchema, service: UserServiceDepends) -> UserResponseSchema:
    return await service.create(request, register_schema)
