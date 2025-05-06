from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import PostgresSettings


class SessionProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: PostgresSettings()) -> AsyncEngine:
        return create_async_engine(settings.url, )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, sessionmake: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        ...
