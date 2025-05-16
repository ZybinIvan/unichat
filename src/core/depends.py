from dishka import Provider, Scope, make_async_container
from dishka.integrations.fastapi import FastapiProvider
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from src.config import Settings
from src.core.db import SQLALCHEMY_DATABASE_URL, get_session as get_db_session
from fastapi import BackgroundTasks


core_provider = Provider(scope=Scope.REQUEST)


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


def provide_redis_client(settings: Settings) -> Redis:
    return Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        username=settings.redis.username,
        password=settings.redis.password,
        decode_responses=True,  # если нужно сразу получать str вместо bytes
    )


core_provider.provide(provide_redis_client, scope=Scope.APP)


# Сборка контейнера с интеграцией FastAPI
container = make_async_container(
    core_provider,
    FastapiProvider(),
)

__all__ = [
    "container",
]
