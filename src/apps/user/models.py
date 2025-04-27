from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Model, TimestampMixin


class UserModel(Model, TimestampMixin):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_path: Mapped[str] = mapped_column(String(255), nullable=True)
