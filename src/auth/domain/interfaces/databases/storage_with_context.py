from typing import Any, Protocol

from src.auth.domain.interfaces.databases.storage_without_context import \
    IStorageManagerWithoutContext

__all__ = ("IStorageManagerWithContext",)


class IStorageManagerWithContext(IStorageManagerWithoutContext, Protocol):
    def set_context(self) -> Any:
        ...

    def get_context(self) -> Any:
        ...
