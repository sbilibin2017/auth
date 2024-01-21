from typing import Protocol

__all__ = ("ISettings",)


class ISettings(Protocol):
    def get_db_uri(self) -> str:
        ...

    def get_cache_uri(self) -> str:
        ...

    def get_broker_uri(self) -> str:
        ...
