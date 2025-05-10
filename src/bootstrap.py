from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka, DishkaRoute

from src.apps.auth.depends import container as dishka_container
from src.middleware import apply_middleware
from src.router import apply_routes


def create_app() -> FastAPI:
    app = FastAPI(debug=True, route_class=DishkaRoute)

    setup_dishka(container=dishka_container, app=app)
    app = apply_middleware(app)
    app = apply_routes(app)

    return app
