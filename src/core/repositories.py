from typing import TypeVar, Generic, Type, Any, Dict, Optional
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
