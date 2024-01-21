from propan import Message, Route

from src.auth.domain.interfaces import (IBrokerManager, IEventManager,
                                        IFutureManager,)
from  src.auth.domain.entities import UserEntity
from src.auth.infrastructure.di_container import di_container
from src.auth.infrastructure.dto.user import UserCreateDTO
__all__ = ("CreateUser",)


broker_manager = di_container.resolve(IBrokerManager)  # pyright: ignore
future_manager = di_container.resolve(IFutureManager)  # pyright: ignore
event_manager = di_container.resolve(IEventManager)  # pyright: ignore
user_service = di_container.resolve(IUserService) # pyright: ignore

@broker_manager.app.route("create_user")
class CreateUser(Route):
    broker = broker_manager.broker

    async def on_message(self, message: Message):
        request_id = message.payload["request_id"]
        data = message.payload["data"]        
        user: UserAggregate = await user_service.create_user(UserCreateDTO(**data))
        future_manager.set_future_result(request_id, user.model_dump())


event_manager.add_event(CreateUser)
