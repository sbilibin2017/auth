from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as AsyncRedis

from src.auth.domain.interfaces import ILogger, ISettings

__all__ = ("CacheManager",)


class CacheManager:
    __engine: AsyncRedis

    def __init__(
        self,
        settings: ISettings,
        logger: ILogger,
    ):
        self.settings = settings
        self.logger = logger
        self.__engine = None

    async def get_session(self):
        return self.__engine

    async def connect(self):
        self.__engine = AsyncRedis(
            connection_pool=ConnectionPool.from_url(
                self.settings.get_cache_uri()
            ),
            decode_responses=True,
        )

    async def disconnect(self):
        await self.__engine.aclose()
