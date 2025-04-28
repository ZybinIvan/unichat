from typing import TypeVar, Generic, Type, Any, Dict, Optional

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Базовый репозиторий для наследования"""

    model: Type[T]

    async def get(self, id: Any, session: AsyncSession) -> Optional[T]:
        """Получить объект по ID"""
        return await session.get(self.model, id)

    async def list(self, limit: int, skip: int, session: AsyncSession) -> list[T]:
        """Получить все объекты"""
        stmt = select(self.model)
        stmt = stmt.limit(limit).offset(skip)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: T, session: AsyncSession) -> T:
        """Добавить новый объект в базу"""
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(self, obj: T, session: AsyncSession) -> T:
        """Обновить уже существующий объект"""
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def delete(self, id: Any, session: AsyncSession) -> Optional[T]:
        """Удалить объект по ID"""
        obj = await self.get(session, id)
        if obj is None:
            return None
        await session.delete(obj)
        await session.commit()
        return obj

    async def get_by(
            self,
            session: AsyncSession,
            **kwargs: Any
    ) -> T:
        """
        Получить один объект по любому полю(ям), аналогично Django ORM .get().
        Бросает NoResultFound, если не найдено,
        MultipleResultsFound, если найдено больше одного.
        """
        stmt = select(self.model).filter_by(**kwargs)
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise sqlalchemy.exc.NoResultFound(f"{self.model.__name__} с параметрами {kwargs} не найден")
        except sqlalchemy.exc.MultipleResultsFound:
            raise sqlalchemy.exc.MultipleResultsFound(f"Найдено несколько {self.model.__name__} с параметрами {kwargs}")
