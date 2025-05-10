from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from src.config import Settings
from src.core.db import SQLALCHEMY_DATABASE_URL, get_session as get_db_session

# Провайдер для "core" модуля
core_provider = Provider(scope=Scope.REQUEST)

# Фабрика для Settings
# Используем отдельную функцию, чтобы Dishka не пытался инжектить параметры конструктора Settings


def provide_settings() -> Settings:
    return Settings()


core_provider.provide(provide_settings, scope=Scope.APP)

# Создание движка БД
async_engine: AsyncEngine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# Фабрика для AsyncEngine


def provide_async_engine() -> AsyncEngine:
    return async_engine


core_provider.provide(provide_async_engine, scope=Scope.APP)

# Создание sessionmaker для AsyncSession
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Фабрика для sessionmaker


def provide_async_sessionmaker() -> async_sessionmaker:
    return async_session


core_provider.provide(provide_async_sessionmaker, scope=Scope.APP)

# Регистрация фабрики сессий для инъекции AsyncSession в use-case'ы
# get_db_session: async def get_db_session() -> AsyncGenerator[AsyncSession, None]
core_provider.provide(get_db_session)

# Сборка контейнера с интеграцией FastAPI
container = make_async_container(
    core_provider,
    FastapiProvider(),
)

__all__ = [
    "container",
]
