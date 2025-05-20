import logging
import os
from typing import Annotated

import jwt
from aiohttp import payload_type
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.apps.university.schemas import UserAuthSchema
from src.core.db import async_session

SECRET_KEY = os.getenv("SECRET_KEY")

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False
)


def auth_middleware(request: Request, token: Annotated[str, Depends(oauth2_scheme)], ):
    payload_data = jwt.decode(
        jwt=token, key=SECRET_KEY, algorithms=['HS256']
    )

    request.scope['user'] = UserAuthSchema(
        id=payload_data["user_id"],
        university_id=payload_data["university_id"],
        role=payload_data["role"]
    )


AuthMiddlewareDepends = Depends(auth_middleware)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next, ) -> Response:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
            try:
                payload_data = jwt.decode(
                    jwt=token, key=SECRET_KEY, algorithms=['HS256']
                )

                request.scope['user'] = UserAuthSchema(
                    id=payload_data["user_id"],
                    university_id=payload_data["university_id"]
                )

                logger.info("AuthMiddleware", request.user)
            except (PyJWTError, ValidationError):
                logger.exception("JWT validation error")
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

    # app.add_middleware(AuthMiddleware)

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
