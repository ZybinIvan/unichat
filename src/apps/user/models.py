from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Model, TimestampMixin

if TYPE_CHECKING:
    from src.apps.university.models import DepartmentModel, GroupModel


class UserModel(Model, TimestampMixin):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_path: Mapped[str] = mapped_column(String(255), nullable=True)


class TeacherModel(Model, TimestampMixin):
    __tablename__ = "teacher"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id", ondelete="SET NULL"), nullable=True
    )

    department: Mapped["DepartmentModel"] = relationship(back_populates="teachers")


class StudentModel(Model, TimestampMixin):
    __tablename__ = "student"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    record_book_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    student_card: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    group_id: Mapped[int] = mapped_column(
        ForeignKey("group.id", ondelete="SET NULL"), nullable=True
    )

    group: Mapped["GroupModel"] = relationship(back_populates="students")
