import json
import logging
from datetime import timedelta
from typing import TypeVar, Generic, Type, Any, Tuple

import sqlalchemy.exc
from fastapi_filter.contrib.sqlalchemy import Filter
from redis.asyncio import Redis
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from src.core.exceptions import (
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
            **service_filters: Any,
    ) -> Tuple[list[T], int]:
        """
        Универсальный list:
        - service_filters: «вшитые» фильтры (например university_id или цепочки через __)
        - filters: fastapi-filter для полей самой модели
        Возвращает:
          - items: список моделей limit/skip с учётом всех фильтров
          - total: общее число записей, где применены **все** фильтры (service + user), но без пагинации
        """
        try:
            # 1) Считаем total с учётом service_filters + filters
            total_stmt = select(func.count()).select_from(self.model)

            # 1.1) «вшитые» фильтры
            for key, val in service_filters.items():
                total_stmt = total_stmt.where(self._build_filter(self.model, key, val))
            # 1.2) фильтры из fastapi-filter
            if filters:
                total_stmt = filters.filter(total_stmt)

            total: int = (await session.execute(total_stmt)).scalar_one()

            # 2) Основной запрос за записями
            stmt = select(self.model)

            # 2.1) service_filters
            for key, val in service_filters.items():
                stmt = stmt.where(self._build_filter(self.model, key, val))
            # 2.2) user-filters + сортировка
            if filters:
                stmt = filters.filter(stmt)
                stmt = filters.sort(stmt)

            # 2.3) пагинация
            stmt = stmt.limit(limit).offset(skip)
            items = (await session.execute(stmt)).scalars().all()

            return items, total

        except Exception as e:
            raise OperationFailedException("list", str(e)) from e

    def _build_filter(
            self,
            model_cls: type,
            key: str,
            value: Any,
    ):
        """
        Рекурсивно строит условие:
        - для простого ключа 'field': model_cls.field == value
        - для вложенного 'rel1__rel2__...__field':
          model_cls.rel1.has(... rel2.has(field=value))
        """
        parts = key.split("__")
        if len(parts) == 1:
            attr = getattr(model_cls, parts[0], None)
            if not isinstance(attr, InstrumentedAttribute):
                raise AttributeError(f"{model_cls.__name__} has no column {parts[0]}")
            return attr == value

        # вложенные отношения
        *rels, field = parts

        def nest(cls, path: list[str]):
            rel_name = path[0]
            rel_attr = getattr(cls, rel_name, None)
            if not isinstance(rel_attr, InstrumentedAttribute):
                raise AttributeError(f"{cls.__name__} has no relationship {rel_name}")
            # если следующий элемент — последний (поле)
            if len(path) == 2:
                return rel_attr.has(**{path[1]: value})
            # иначе — продолжаем вглубь
            next_cls = rel_attr.property.mapper.class_
            return rel_attr.has(nest(next_cls, path[1:]))

        return nest(model_cls, parts)

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


class BaseRedisRepository:
    key_prefix: str

    def __init__(self, client: Redis):
        self.client = client

    def _full_key(self, key: str) -> str:
        return f"{self.key_prefix}:{key}"

    async def get(self, key: str) -> dict | None:
        full_key = self._full_key(key)
        try:
            data = await self.client.get(full_key)
            return json.loads(data)
        except Exception as e:
            logger.exception(e)

    async def set(self, key: str, value: dict, ttl: timedelta) -> bool:
        full_key = self._full_key(key)
        try:
            return await self.client.set(full_key, json.dumps(value), ex=ttl)
        except Exception as e:
            logger.exception(e)
