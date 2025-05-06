from fastapi import FastAPI, APIRouter

from src.apps.auth.routes import auth_routes
from src.apps.university.routes import university_router


def apply_routes(app: FastAPI) -> FastAPI:
    router = APIRouter(prefix="/api")

    router.include_router(auth_routes, prefix="/auth", tags=["auth"])
    # router.include_router(user_routes)
    router.include_router(university_router, prefix="/university", tags=["university"])

    app.include_router(router)

    return app
