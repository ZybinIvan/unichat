from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.exceptions import AlreadyExistsException, MultipleObjectsFoundException, NotFoundException, OperationFailedException


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def multiple_found_exception_handler(
    request: Request, exc: MultipleObjectsFoundException
):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def already_exists_exception_handler(
    request: Request, exc: AlreadyExistsException
):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def operation_failed_exception_handler(
    request: Request, exc: OperationFailedException
):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
