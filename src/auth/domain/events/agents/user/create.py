from src.auth.databases import broker
from src.auth.events.worker import worker


user_topic = broker.topic('users', value_type=User)
user_created_topic = broker.topic('users_created', value_type=User)


         
@broker.agent(user_topic)
async def process_user(users):
    async for request_id, user in users.items():        
        await self.user_created_topic.send(key=request_id, value=user)
            
@broker.agent(user_created_topic)
async def process_confirmation(confirmations):
    async for request_id, user in confirmations.items():        
        if request_id in futures:
            await worker.set_future_result(request_id, user)            
                
@cached
def get_user_topic():
    return user_topic
 