import asyncio
from uuid import uuid4

__all__ = ("FutureManager",)


class FutureManager:
    def __init__(self):
        self.futures = {}

    def create_future(self):
        request_id = str(uuid4())
        future = asyncio.Future()
        self.futures[request_id] = future
        return request_id

    def get_future(self, request_id):
        return self.futures.get(request_id, None)

    def set_future_result(self, request_id, result):
        if request_id in self.futures:
            self.futures[request_id].set_result(result)
            del self.futures[request_id]

    async def wait_for(self, request_id, timeout):
        future = self.get_future(request_id)
        if future is None:
            raise ValueError(f"No future found for request_id {request_id}")
        result = await asyncio.wait_for(future, timeout)
        return result
