"""DI container factory.

On application start inject di container created with factory
Example FastAPI:

|_infrastructure
    |_app_factory.py
    |_di_container_factory.py

app_factory.py
@app.on_event("startup")
async def startup():
    di_container.di_container = di_container.di_container.create()    
"""

from punq import Container as DIContainer

from src.auth.domain.interfaces import (IBrokerManager, IDIContainer,
                                        IFutureManager, ILogger, ISettings,
                                        IStorageManagerWithoutContext,
                                        IStorageManagerWithContext,)
from src.auth.infrastructure import (BrokerManager, CacheManager,
                                     DatabaseManager, FutureManager, Logger,
                                     Settings,)

__all__ = (
    "create",
    "di_container",
)


def create() -> IDIContainer:
    """Creates instance of di container with all needed dependencies."""
    di_container = DIContainer()
    di_container.register(ISettings, Settings)
    di_container.register(ILogger, Logger)
    di_container.register(IStorageManagerWithContext, DatabaseManager)
    di_container.register(IStorageManagerWithoutContext, CacheManager)
    di_container.register(IBrokerManager, BrokerManager)
    di_container.register(IFutureManager, FutureManager)   
    return di_container


di_container: IDIContainer | None = None
