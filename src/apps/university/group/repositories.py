import logging
from typing import Any, Tuple

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.apps.university.models import GroupModel, DepartmentModel
from src.core.exceptions import NotFoundException, OperationFailedException
from src.core.repositories import BaseRepository

logger = logging.getLogger(__name__)


class GroupRepository(BaseRepository[GroupModel]):
    model = GroupModel

    async def get_detail(self, id: int, session: AsyncSession) -> GroupModel:
        stmt = (
            select(self.model)
            .options(
                # при выборке сразу подтягиваем институт
                selectinload(self.model.department)
                .selectinload(DepartmentModel.institute)
            )
            .where(self.model.id == id)
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
    ) -> Tuple[list[GroupModel], int]:
        """
        Жадно подгружаем department → institute, чтобы Pydantic мог достать их
        без ленивого I/O.
        """
        try:
            # 1) Общее количество (с учётом service_filters + filters, если нужно)
            total_stmt = select(func.count()).select_from(self.model)
            for key, val in service_filters.items():
                total_stmt = total_stmt.where(self._build_filter(self.model, key, val))
            if filters:
                total_stmt = filters.filter(total_stmt)
            total = (await session.execute(total_stmt)).scalar_one()

            # 2) Сам запрос за объектами с eager-loading
            stmt = select(self.model).options(
                selectinload(self.model.department)
                .selectinload(DepartmentModel.institute)
            )
            for key, val in service_filters.items():
                stmt = stmt.where(self._build_filter(self.model, key, val))
            if filters:
                stmt = filters.filter(stmt)
                stmt = filters.sort(stmt)

            stmt = stmt.limit(limit).offset(skip)
            items = (await session.execute(stmt)).scalars().all()

            return items, total

        except Exception as e:
            raise OperationFailedException("list_groups", str(e)) from e