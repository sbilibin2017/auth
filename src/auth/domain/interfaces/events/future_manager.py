from typing import Protocol

__all__ = ("IFutureManager",)


class IFutureManager(Protocol):
    async def create_future(self):
        ...

    def check_future_by_request_id(self, request_id):
        ...

    async def set_future_result(self, request_id, result):
        ...

    async def wait_for(self, future, timeout):
        ...
