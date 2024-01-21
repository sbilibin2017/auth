# from typing import Protocol


# class ICreateUserUsecase(Protocol):
#     async def create_user(self, event: IEvent, dto: UserCreateDTO):
#         ...

# class EventDTO(BaseModel):
#     request_id: str
#     data: BaseModel


# class CreateUserUsecase:
#     def __init__(
#         self,
#         future_manager: IFutureManager,
#         broker_manager: IBrokerManager,
#     ):
#         self.future_manager = future_manager
#         self.broker_manager = event_mabroker_managernager

#     async def create_user(self, dto: UserCreateDTO):
#         request_id = self.future_manager.create_future()
#         await self.broker_manager.send(
#             "create_user", 
#             EventDTO(request_id=request_id, data=dto)
            
#         )
#         created_user = await future_manager.wait_for(request_id, timeout=60.0)
#         return created_user
