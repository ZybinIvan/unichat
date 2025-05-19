from fastapi import FastAPI, APIRouter
from dishka.integrations.fastapi import DishkaRoute

from src.apps.auth.routes import auth_routes
from src.apps.university.routes import university_router
from src.apps.user.routes import user_routes


def apply_routes(app: FastAPI) -> FastAPI:
    router = APIRouter(prefix="/api", route_class=DishkaRoute)

    router.include_router(auth_routes, prefix="/auth", tags=["auth"])
    # router.include_router(user_routes)
    router.include_router(university_router, prefix="/university", tags=["university"])
    router.include_router(user_routes, prefix="/users", tags=["user"])

    app.include_router(router)

    return app
