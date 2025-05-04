from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.core.db import Model

if TYPE_CHECKING:
    from src.apps.user.models import TeacherModel, StudentModel


class UniversityModel(Model):
    __tablename__ = "university"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    institutes: Mapped[list["InstituteModel"]] = relationship(
        back_populates="university", cascade="all, delete-orphan"
    )


class InstituteModel(Model):
    __tablename__ = "institute"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("university.id", ondelete="CASCADE"), nullable=False
    )

    # __table_args__ = (
    #     UniqueConstraint("university_id", "name", name="uq_institute_in_university"),
    # )

    university: Mapped["UniversityModel"] = relationship(back_populates="institutes")
    departments: Mapped[list["DepartmentModel"]] = relationship(
        back_populates="institute", cascade="all, delete-orphan"
    )


class DepartmentModel(Model):
    __tablename__ = "department"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    institute_id: Mapped[int] = mapped_column(
        ForeignKey("institute.id", ondelete="CASCADE"), nullable=False
    )

    # __table_args__ = (
    #     UniqueConstraint("institute_id", "name", name="uq_department_in_institute"),
    # )

    institute: Mapped["InstituteModel"] = relationship(back_populates="departments")
    teachers: Mapped[list["TeacherModel"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )
    groups: Mapped[list["GroupModel"]] = relationship(
        back_populates="department", cascade="all, delete-orphan"
    )


class GroupModel(Model):
    __tablename__ = "group"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.id", ondelete="CASCADE"), nullable=False
    )

    # __table_args__ = (
    #     UniqueConstraint("department_id", "name", name="uq_group_in_department"),
    # )

    department: Mapped["DepartmentModel"] = relationship(back_populates="groups")
    students: Mapped[list["StudentModel"]] = relationship(
        back_populates="group", cascade="all, delete-orphan"
    )
