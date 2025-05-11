from typing import TypeVar, Generic, Type, Any
import logging
from asyncpg import ForeignKeyViolationError
from fastapi import HTTPException, status
import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_filter.contrib.sqlalchemy import Filter

from src.core.exceptions import (
    AlreadyExistsException,
    MultipleObjectsFoundException,
    NotFoundException,
    OperationFailedException,
)

T = TypeVar("T")

logger = logging.getLogger(__name__)

class BaseRepository(Generic[T]):
    """Базовый репозиторий для наследования"""

    model: Type[T]

    async def get_or_none(self, id: Any, session: AsyncSession) -> T | None:
        """Получить объект по ID"""
        try:
            return await session.get(self.model, id)
        except Exception as e:
            raise OperationFailedException("get_or_none", str(e)) from e

    async def list(
        self,
        limit: int,
        skip: int,
        session: AsyncSession,
        filters: Filter | None = None,
    ) -> list[T]:
        """Получить все объекты"""
        try:
            stmt = select(self.model)
            if filters:
                stmt = filters.filter(stmt)
                stmt = filters.sort(stmt)
            stmt = stmt.limit(limit).offset(skip)
            result = await session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise OperationFailedException("list", str(e)) from e

    async def create(self, obj: T, session: AsyncSession) -> T:
        """Добавить новый объект в базу"""
        try:
            session.add(obj)
            await session.flush()
            return obj
        except Exception as e:
            logger.exception(e)
            raise OperationFailedException("create", str(e)) from e

    async def update(self, obj: T, session: AsyncSession) -> T:
        """Обновить уже существующий объект"""
        try:
            session.add(obj)
            await session.refresh(obj)
            return obj
        except Exception as e:
            raise OperationFailedException("update", str(e)) from e

    async def delete(self, id: Any, session: AsyncSession) -> bool:
        """Удалить объект по ID"""
        try:
            obj = await self.get_or_none(id, session)
            if obj is None:
                raise NotFoundException(self.model.__name__, {"id": id})
            await session.delete(obj)
            return True
        except NotFoundException:
            raise
        except Exception as e:
            raise OperationFailedException("delete", str(e)) from e

    async def get_by(self, session: AsyncSession, **kwargs: Any) -> T:
        """
        Получить один объект по любому полю(ям)
        """
        stmt = select(self.model).filter_by(**kwargs)
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except sqlalchemy.exc.NoResultFound as e:
            raise NotFoundException(self.model.__name__, kwargs) from e
        except sqlalchemy.exc.MultipleResultsFound as e:
            raise MultipleObjectsFoundException(self.model.__name__, kwargs) from e
        except Exception as e:
            raise OperationFailedException("get_by", str(e)) from e
