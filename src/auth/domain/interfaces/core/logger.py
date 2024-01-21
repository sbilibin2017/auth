from typing import Protocol

__all__ = ("ILogger",)


class ILogger(Protocol):
    async def info(self, msg: str) -> None:
        ...

    async def error(self, msg: str) -> None:
        ...

    async def close(self) -> None:
        ...
