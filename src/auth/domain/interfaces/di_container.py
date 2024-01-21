from typing import Protocol

__all__ = ("IDIContainer",)


class IDIContainer(Protocol):
    def register(self, interface: type, implementation: type) -> None:
        ...

    def resolve(self, interface: type) -> type:
        ...
