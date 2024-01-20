class MessageBus:
    def __init__(self, worker: AsyncioWorker):       
        self.worker = worker
 
    async def produce(self, topic, message):        
        request_id = self.worker.create_future() 
        await topic.send(key=request_id, value=message)    
        return request_id
 
    async def consume(self, topic):
        async for request_id, user in topic.items():            
            self.worker.set_future_result(request_id, user)
            
    async def wait_for(self, request_id, timeout):
        try:
            result = await asyncio.wait_for(self.futures[request_id], timeout)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=500, detail="Operation failed")
        return result