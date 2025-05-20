import logging

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select
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