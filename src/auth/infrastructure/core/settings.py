from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.auth.infrastructure.utils import singleton

__all__ = ("Settings",)


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="postgres_",
        frozen=True,
    )

    version: str = Field(alias="version")
    db: str = Field(alias="db")
    schema_name: str = Field(alias="schema_name")
    user: str = Field(alias="user")
    password: str = Field(alias="password")
    host: str = Field(alias="host")
    port: int = Field(alias="port")


class CacheSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="redis_",
        frozen=True,
    )

    version: str = Field(alias="version")
    db: str = Field(alias="db")
    user: str = Field(alias="user")
    password: str = Field(alias="password")
    host: str = Field(alias="host")
    port: int = Field(alias="port")
    ttl: int = Field(alias="ttl")


class BrokerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="kafka_",
        frozen=True,
    )

    host: str = Field(alias="host")
    port: int = Field(alias="port")
    external_port: int = Field(alias="external_port")


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="app_",
        frozen=True,
    )

    host: str = Field(alias="host")
    port: int = Field(alias="port")
    debug: bool = Field(alias="debug")
    n_threads: int = Field(alias="n_threads")


class DockerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="docker_",
        frozen=True,
    )

    db_host: str = Field(alias="db_host")
    cache_host: str = Field(alias="cache_host")
    app_host: str = Field(alias="app_host")
    broker_host: str = Field(alias="broker_host")


@singleton
class Settings:
    db: DBSettings = DBSettings()  # pyright: ignore
    cache: CacheSettings = CacheSettings()  # pyright: ignore
    broker: BrokerSettings = BrokerSettings()  # pyright: ignore
    app: AppSettings = AppSettings()  # pyright: ignore
    docker: DockerSettings = DockerSettings()  # pyright: ignore

    def get_db_uri(self) -> str:
        return (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
                user=self.db.user,
                password=self.db.password,
                host=self.docker.db_host,
                port=self.db.port,
                db=self.db.db,
            )
        )

    def get_cache_uri(self) -> str:
        return "redis://{host}:{port}/{db}".format(
            host=self.docker.cache_host,
            port=self.cache.port,
            db=self.cache.db,
        )

    def get_broker_uri(self) -> str:
        return "{host}:{port}".format(
            host=self.docker.broker_host,
            port=self.broker.port,
        )
