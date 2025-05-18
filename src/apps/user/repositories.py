from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import with_polymorphic, selectinload

from src.apps.university.models import GroupModel, DepartmentModel, InstituteModel
from src.apps.user.models import UserModel, TeacherModel, StudentModel, UniversityAdminModel
from src.core.repositories import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    model = UserModel

    async def get_by(self, session: AsyncSession, **kwargs) -> UserModel:
        # Создаём «полиморфный» выбор: UserModel + все подклассы
        user_poly = with_polymorphic(
            UserModel,
            [StudentModel, TeacherModel, UniversityAdminModel],
            flat=True,
        )

        stmt = (
            select(user_poly)
            .filter_by(**kwargs)
            .options(
                # Для студентов: group → department → institute → university
                selectinload(user_poly.StudentModel.group)
                .selectinload(GroupModel.department)
                .selectinload(DepartmentModel.institute)
                .selectinload(InstituteModel.university),
                # Для преподавателей: department → institute → university
                selectinload(user_poly.TeacherModel.department)
                .selectinload(DepartmentModel.institute)
                .selectinload(InstituteModel.university),
                # Для админов: прямая связь university
                selectinload(user_poly.UniversityAdminModel.university),
            )
        )

        result = await session.execute(stmt)
        # scalar_one() бросит, если не найден или найдено >1
        user: UserModel = result.scalar_one()
        return user


class TeacherRepository(BaseRepository[TeacherModel]):
    model = TeacherModel


class StudentRepository(BaseRepository[StudentModel]):
    model = StudentModel


class UniversityAdminRepository(BaseRepository[UniversityAdminModel]):
    model = UniversityAdminModel
