class ICreateUserUsecase(Protocol):
    async def create_user(self, dto: UserCreateDTO):
        ...

@dataclass
class CreateUserUsecase:    
    message_broker: IMessageBroker,
    future_manager: IFutureManager    
    
    async def create_user(self, dto: UserCreateDTO):        
        future, request_id = await future_manager.create_future()
        await message_broker.send(key=request_id, value=user)
        new_user = await future_manager.wait_for(future, timeout=10.0)        
        return new_user
    
@cached   
def get_create_user_usecase(
    message_broker: IMessageBroker = Depends(get_create_user_topic),
    worker: IWorker = Depends(get_worker),
) -> ICreateUserUsecase:
    return CreateUserUsecase(message_broker, worker)
    
        