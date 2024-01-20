
class AsyncioWorker:
    def __init__(self):
        self.futures = {}
 
    def create_future(self):
        request_id = str(uuid.uuid4())
        future = asyncio.Future()
        self.futures[request_id] = future
        return request_id    
 
    def set_future_result(self, request_id, result):
        if request_id in self.futures:
            self.futures[request_id].set_result(result)            
    
    
    
        
    