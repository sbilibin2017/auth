from propan import KafkaBroker, PropanApp

from src.auth.domain.interfaces import ILogger, ISettings

__all__ = ("BrokerManager",)


class BrokerManager:
    __broker: KafkaBroker
    __app: PropanApp
    
    def __init__(
        self,
        settings: ISettings,
        logger: ILogger,
    ):
        self.settings = settings
        self.__broker = None 
        self.__app = None 
        self.__events = {}

    @property
    def broker(self) -> KafkaBroker:
        return self.__broker

    @property
    def app(self) -> PropanApp:
        return self.__app
    
    def add_event(self, name, event):
        self.__events[name] = event

    async def send(self, name: str, dto):
        event = self.__events.get(name, None)
        if event is None:
            raise ValueError(f"No event found with name {name}")
        await event.broker.send(name, dto.model_dump())

    async def connect(self):
        self.__broker = KafkaBroker(
            bootstrap_servers=self.settings.get_broker_uri()
        )
        self.__app = PropanApp(self.__broker)
        await self.__broker.start()

    async def disconnect(self):
        await self.__broker.stop()        