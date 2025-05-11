# src/core/exceptions.py

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, entity: str, params: dict):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} с параметрами {params} не найден",
        )


class MultipleObjectsFoundException(HTTPException):
    def __init__(self, entity: str, params: dict):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Найдено несколько {entity} с параметрами {params}",
        )


class AlreadyExistsException(HTTPException):
    def __init__(self, entity: str, params: dict):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity} с параметрами {params} уже существует",
        )


class OperationFailedException(HTTPException):
    def __init__(self, operation: str, reason: str | None = None):
        detail = f"Не удалось выполнить операцию: {operation}"
        if reason:
            detail += f". Причина: {reason}"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
