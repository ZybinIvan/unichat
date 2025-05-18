import logging
import os

import jwt
from dishka.integrations.starlette import inject
from dishka import provide, Scope, FromDishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.apps.auth.schemas import AccessTokenPayloadSchema
from src.apps.auth.services import JWTService
from src.core.db import async_session

SECRET_KEY = os.getenv("SECRET_KEY")

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next, ) -> Response:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            try:
                payload_data = jwt.decode(
                    jwt=token, key=SECRET_KEY, algorithms=['HS256']
                )
                payload_data["id"] = payload_data["user_id"]
                # Валидируем через Pydantic — тут и проверка наличия university_id
                payload = AccessTokenPayloadSchema.model_validate(payload_data)
                # Убеждаемся, что в state.user есть объект
                if not hasattr(request.state, "user"):
                    class _User: ...

                    request.state.user = _User()
                # Кладём university_id
                request.state.user.university_id = payload.university_id

                logger.error("payload.university_id %s", payload.university_id)
            except (PyJWTError, ValidationError):
                logger.exception("JWT validation error")
                # Если токен некорректен, просрочен или нет поля university_id — молча пропускаем
                pass

        return await call_next(request)


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)

        async with async_session() as session:
            request.state.session = session
            response = await call_next(request)
            await request.state.session.commit()
        return response


def apply_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(DBSessionMiddleware)  # type: ignore

    app.add_middleware(AuthMiddleware)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
