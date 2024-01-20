from typing import Iterable

from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from faust import App as FaustApp
from redis.asyncio import ConnectionPool
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
from src.auth.core import logger, settings
from src.auth.databases import cache, db
from src.auth.events import broker


def create(
    *,
    title: str,
    version: str,
    docs_url: str,
    openapi_url: str,
    routers: Iterable[APIRouter]
) -> FastAPI:
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
        logger.info("Connecting to cache ...")
        cache.cache = AsyncRedis(
            connection_pool=ConnectionPool.from_url(settings.get_cache_uri()),
            decode_responses=True,
        )
        logger.info("Connected to cache ...")
        logger.info("Connecting to db ...")
        db.db = create_async_engine(
            settings.get_db_uri(),
            echo=True,
        )
        logger.info("Connected to db ...")
        logger.info("Connecting to broker ...")
        broker.broker = FaustApp(
            "broker",
            broker=settings.get_broker_uri(),
        )
        asyncio.create_task(
            broker.broker.start()
        )
        logger.info("Connected to broker ...")
        

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Closing cache connection ...")
        await cache.cache.close()  # pyright: ignore
        logger.info("Closing db connection ...")
        await db.db.dispose()  # pyright: ignore
        logger.info("Closing broker connection ...")
        await broker.broker.stop()  # pyright: ignore

    return app
