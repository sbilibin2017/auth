from aiologger.loggers.json import JsonLogger

from src.auth.infrastructure.utils import singleton

__all__ = ("Logger",)


@singleton
class Logger:
    def __init__(self):
        self.logger = JsonLogger.with_default_handlers()

    async def info(self, msg: str) -> None:
        await self.logger.info(msg)

    async def error(self, msg: str) -> None:
        await self.logger.error(msg)

    async def close(self):
        await self.logger.shutdown()
