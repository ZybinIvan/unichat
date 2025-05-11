from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.repositories import BaseRepository
from .models import UniversityModel, DepartmentModel, GroupModel, InstituteModel
from ...core.exceptions import NotFoundException


class UniversityRepository(BaseRepository[UniversityModel]):
    model = UniversityModel


class InstituteRepository(BaseRepository[InstituteModel]):
    model = InstituteModel


class DepartmentRepository(BaseRepository[DepartmentModel]):
    model = DepartmentModel

    async def get_detail(self, id: int, session: AsyncSession) -> DepartmentModel:
        stmt = (
            select(self.model)
            .options(
                # при выборке сразу подтягиваем институт
                selectinload(self.model.institute)
            )
        )
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFoundException(self.model.__name__, {"id": id}) from e


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
        )
        result = await session.execute(stmt)
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise NotFoundException(self.model.__name__, {"id": id}) from e
