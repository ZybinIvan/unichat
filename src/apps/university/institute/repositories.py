import logging
from typing import Tuple, Any

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing_extensions import override

from src.apps.university.models import InstituteModel, DepartmentModel
from src.core.exceptions import OperationFailedException
from src.core.repositories import BaseRepository

logger = logging.getLogger(__name__)

class InstituteRepository(BaseRepository[InstituteModel]):
    model = InstituteModel

    async def list(
            self,
            limit: int,
            skip: int,
            session: AsyncSession,
            filters: Filter | None = None,
            **service_filters: Any,
    ) -> Tuple[list[InstituteModel], int]:
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
            stmt = (
                select(self.model)
                .options(selectinload(self.model.university))
            )

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

