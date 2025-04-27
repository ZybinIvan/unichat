from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Model


class RefreshTokenModel(Model):
    __tablename__ = "refresh_token"

    refresh_token: Mapped[str] = mapped_column(String(length=512), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
