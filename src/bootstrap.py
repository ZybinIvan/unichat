from fastapi import FastAPI

from src.middleware import apply_middleware
from src.router import apply_routes


def create_app() -> FastAPI:
    app = FastAPI(debug=True)
    app = apply_middleware(app)
    app = apply_routes(app)

    return app
