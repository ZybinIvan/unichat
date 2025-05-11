from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka, DishkaRoute

from src.core.exception_handlers import already_exists_exception_handler, multiple_found_exception_handler, not_found_exception_handler, operation_failed_exception_handler
from src.core.exceptions import AlreadyExistsException, MultipleObjectsFoundException, NotFoundException, OperationFailedException
from src.apps.auth.depends import container as dishka_container
from src.middleware import apply_middleware
from src.router import apply_routes


def create_app() -> FastAPI:
    app = FastAPI(debug=True, route_class=DishkaRoute)

    setup_dishka(container=dishka_container, app=app)
    app = apply_middleware(app)
    app = apply_routes(app)

    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(MultipleObjectsFoundException, multiple_found_exception_handler)
    app.add_exception_handler(AlreadyExistsException, already_exists_exception_handler)
    app.add_exception_handler(OperationFailedException, operation_failed_exception_handler)

    return app
