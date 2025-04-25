import logging

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import PostgresSettings

SQLALCHEMY_DATABASE_URL = PostgresSettings().url

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Model(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True, unique=True
    )


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
