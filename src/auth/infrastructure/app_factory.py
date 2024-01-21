"""App factory.

Creates FastAPI app with:
1. meta info
2. routers
3. di container factory
"""
from typing import Callable, Iterable

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse

from src.auth.domain.interfaces import (IBrokerManager,
                                        IStorageManagerWithContext,
                                        IStorageManagerWithoutContext,)

__all__ = ("create",)


def create(
    *,
    title: str,
    version: str,
    docs_url: str,
    openapi_url: str,
    routers: Iterable[APIRouter],
    di_container_factory: Callable,
) -> FastAPI:
    """Creates instance of FastAPI app."""
    app = FastAPI(
        title=title,
        version=version,
        docs_url=docs_url,
        openapi_url=openapi_url,
        default_response_class=ORJSONResponse,
    )

    for router in routers:
        app.include_router(router)

    @app.on_event("startup")
    async def startup():
        di_container_factory.di_container = di_container_factory.create()

        db_manager = di_container_factory.di_container.resolve(
            IStorageManagerWithContext
        )
        await db_manager.connect()

        cache_manager = di_container_factory.di_container.resolve(
            IStorageManagerWithoutContext
        )
        await cache_manager.connect()

        broker_manager = di_container_factory.di_container.resolve(
            IBrokerManager
        )
        await broker_manager.connect()

    @app.on_event("shutdown")
    async def shutdown():
        db_manager = di_container_factory.di_container.resolve(
            IStorageManagerWithContext
        )
        await db_manager.disconnect()

        cache_manager = di_container_factory.di_container.resolve(
            IStorageManagerWithoutContext
        )
        await cache_manager.disconnect()

        broker_manager = di_container_factory.di_container.resolve(
            IBrokerManager
        )
        await broker_manager.disconnect()

    return app
