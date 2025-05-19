from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, ForeignKey, Text, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Model, TimestampMixin

if TYPE_CHECKING:
    from src.apps.university.models import GroupModel

classroom_group_association = Table(
    "classroom_group",
    Model.metadata,
    Column(
        "classroom_id",
        ForeignKey("classroom.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "group_id",
        ForeignKey("group.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ClassroomModel(Model, TimestampMixin):
    __tablename__ = "classroom"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    groups: Mapped[list["GroupModel"]] = relationship(
        "GroupModel",
        secondary=classroom_group_association,
        back_populates="classrooms",
    )

    tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        back_populates="classroom",
        cascade="all, delete-orphan",
    )


class TaskModel(Model, TimestampMixin):
    __tablename__ = "task"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    points: Mapped[int] = mapped_column(Integer, nullable=True)
    deadline: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classroom.id", ondelete="CASCADE"),
        nullable=False,
    )
    classroom: Mapped["ClassroomModel"] = relationship(
        "ClassroomModel",
        back_populates="tasks",
    )

    # связь с файлами-заданиями
    file_tasks: Mapped[list["FileTaskModel"]] = relationship(
        "FileTaskModel",
        back_populates="task",
        cascade="all, delete-orphan",
    )


class FileTaskModel(Model, TimestampMixin):
    __tablename__ = "file_task"

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)

    task_id: Mapped[int] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE"),
        nullable=False,
    )
    task: Mapped["TaskModel"] = relationship(
        "TaskModel",
        back_populates="file_tasks",
    )
