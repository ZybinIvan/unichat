from fastapi import APIRouter, Request

from src.apps.user.depends import UserServiceDepends
from src.apps.user.schemas import UserRegisterSchema, UserResponseSchema
from src.core.depends import SessionDepends

user_routes = APIRouter()


@user_routes.post("/register")
async def create(request: Request, register_schema: UserRegisterSchema, service: UserServiceDepends,
                 session: SessionDepends) -> UserResponseSchema:
    return await service.create(register_schema, session)
