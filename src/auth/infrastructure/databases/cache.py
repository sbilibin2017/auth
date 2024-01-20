from redis.asyncio import Redis as AsyncRedis

__all__ = ("cache",)

cache: AsyncRedis | None = None
