from typing import Protocol

__all__ = ("IBrokerManager",)


class IBrokerManager(Protocol):
    @property
    def broker(self):
        ...

    @property
    def app(self):
        ...
        
    def add_event(self, name: str, event) -> None:
        ...

    async def send(self, name: str, dto):
        ...
        
    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

