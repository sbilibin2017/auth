from typing import Any, Protocol

from src.auth.domain.interfaces.core import ILogger, ISettings

__all__ = ("IStorageManagerWithoutContext",)


class IStorageManagerWithoutContext(Protocol):
    @property
    def settings(self) -> ISettings:
        ...

    @property
    def logger(self) -> ILogger:
        ...

    def get_session(self) -> Any:
        ...

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...
