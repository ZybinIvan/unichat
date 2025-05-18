from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.user.enums import UserRole
from src.core.db import Model, TimestampMixin

if TYPE_CHECKING:
    from src.apps.university.models import DepartmentModel, GroupModel, UniversityModel


class UserModel(Model, TimestampMixin):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_path: Mapped[str] = mapped_column(String(255), nullable=True)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole, name="role"), nullable=False,
                                           default=UserRole.USER)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role,
    }


class TeacherModel(UserModel):
    __tablename__ = "teacher"

    id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id", ondelete="SET NULL"), nullable=True
    )

    department: Mapped["DepartmentModel"] = relationship(back_populates="teachers")

    __mapper_args__ = {
        'polymorphic_identity': UserRole.TEACHER.value,
    }

    @hybrid_property
    def university_id(self) -> int:
        return self.department.institute.university.id


class StudentModel(UserModel):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True
    )

    record_book_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    student_card: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="SET NULL"), nullable=True
    )

    group: Mapped["GroupModel"] = relationship(back_populates="students")

    __mapper_args__ = {
        'polymorphic_identity': UserRole.STUDENT.value,
    }

    @hybrid_property
    def university_id(self) -> int:
        return self.group.department.institute.university.id


class UniversityAdminModel(UserModel):
    __tablename__ = "university_admin"
    id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    university_id: Mapped[int] = mapped_column(
        ForeignKey("university.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    university: Mapped["UniversityModel"] = relationship(back_populates="admin")

    __mapper_args__ = {
        "polymorphic_identity": UserRole.UNIVERSITY_ADMIN.value,
    }
