from typing import Any, Tuple

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.university.models import DepartmentModel
from src.core.exceptions import NotFoundException, OperationFailedException
from src.core.repositories import BaseRepository


class DepartmentRepository(BaseRepository[DepartmentModel]):
    model = DepartmentModel

    async def get_detail(self, id: int, session: AsyncSession) -> DepartmentModel:
        stmt = (
            select(self.model)
            .options(
                # при выборке сразу подтягиваем институт
                selectinload(self.model.institute)
            ).where(self.model.id == id)
        )
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFoundException(self.model.__name__, {"id": id}) from e

    async def list(
            self,
            limit: int,
            skip: int,
            session: AsyncSession,
            filters: Filter | None = None,
            **service_filters: Any,
    ) -> Tuple[list[DepartmentModel], int]:
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
            stmt = select(self.model).options(selectinload(self.model.institute))


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
