from functools import cache
from uuid import uuid4
import asyncio
from typing import Protocol

__all__ = ("IWorker", "worker", "get_worker", )

class IFutureManager(Protocol):
    async def create_future(self):
        ...
        
 
    async def set_future_result(self, request_id, result):
        ...
         
            
    async def wait_for(self, future, timeout):
        ...
    
    
class FutureManager:
    def __init__(self):
        self.futures = {}
 
    async def create_future(self):
        request_id = str(uuid.uuid4())
        future = asyncio.Future()
        self.futures[request_id] = future
        return future, request_id
 
    async def set_future_result(self, request_id, result):
        if request_id in self.futures:
            self.futures[request_id].set_result(result)   
            del self.futures[request_id]
            
    async def wait_for(self, future, timeout):
        result = await asyncio.wait_for(future, timeout)        
        return result
    
future_manager: IFutureManager = FutureManager()


@cache
def get_future_manager():
    return worker