from fastapi_mail import ConnectionConfig
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    user: str = 'postgres'
    password: str = 'password'
    db: str = 'db'
    host: str = "localhost"
    port: str = "5432"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    host: str = "localhost"
    port: int = 6379
    username: str | None = "default"
    password: str | None = None


class JWTSettings(BaseSettings):
    access_token_expiration_minutes: int = Field(default=5)
    refresh_token_expiration_days: int = Field(default=30)
    secret_key: str = Field('SECRET_KEY')
    algorithms: list[str] = Field(default=["HS256"])


class Settings(BaseSettings):
    dev: bool = True

    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()

    jwt: JWTSettings = JWTSettings()
    email: ConnectionConfig = ConnectionConfig()
