from typing import TYPE_CHECKING

from src.core.db import Model, TimestampMixin
from sqlalchemy import String, Table, Column, Integer, ForeignKey, JSON, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from src.apps.user.models import UserModel

chat_participants = Table(
    'chat_participants', Model.metadata,
    Column('chat_id', Integer, ForeignKey('chats.id', ondelete='CASCADE')),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'))
)


class Chat(Model):
    __tablename__ = 'chat'

    name: Mapped[str | None] = mapped_column(String, nullable=True)
    participants: Mapped[list[UserModel]] = relationship('User', secondary=chat_participants, backref='chats')


class Message(Model, TimestampMixin):
    __tablename__ = 'messages'

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    content: Mapped[dict] = mapped_column(JSON)
