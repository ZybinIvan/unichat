from fastapi import FastAPI, APIRouter

from src.apps.auth.routes import auth_routes
from src.apps.user.routes import user_routes


def apply_routes(app: FastAPI) -> FastAPI:
    router = APIRouter(prefix="/api")

    router.include_router(auth_routes)
    router.include_router(user_routes)

    app.include_router(router)

    return app
